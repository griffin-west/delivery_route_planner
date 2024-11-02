from ortools.constraint_solver import pywrapcp
import src.models as models


def solve_vehicle_routing_problem(
    data: models.DataModel,
    scenario: models.RoutingScenario,
    settings: models.SearchSettings,
) -> models.Solution | None:

    manager = pywrapcp.RoutingIndexManager(
        len(data.nodes), len(data.vehicles), models.Node.origin_id
    )
    router = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index) -> int:
        from_node = data.nodes[manager.IndexToNode(from_index)]
        to_node = data.nodes[manager.IndexToNode(to_index)]
        return data.distance_map.cost_map[from_node.address][to_node.address]

    distance_callback_index = router.RegisterTransitCallback(distance_callback)
    router.SetArcCostEvaluatorOfAllVehicles(distance_callback_index)
    router.AddDimension(
        distance_callback_index,
        0,
        settings.max_mileage_per_vehicle * models.MILEAGE_SCALE_FACTOR,
        True,
        "Distance",
    )
    distance_dimension = router.GetDimensionOrDie("Distance")
    distance_dimension.SetGlobalSpanCostCoefficient(
        settings.distance_span_cost_coefficient
    )

    day_duration = scenario.day_start.duration_until(scenario.day_end)

    time_callback_indices = []
    for vehicle in data.vehicles.values():
        vehicle_travel_costs = vehicle.duration_map.cost_map

        def time_callback_closure(vehicle_travel_costs):
            def time_callback(from_index, to_index) -> int:
                from_node = data.nodes[manager.IndexToNode(from_index)]
                to_node = data.nodes[manager.IndexToNode(to_index)]
                return vehicle_travel_costs[from_node.address][to_node.address]

            return time_callback

        time_callback_indices.append(
            router.RegisterTransitCallback(time_callback_closure(vehicle_travel_costs))
        )
    router.AddDimensionWithVehicleTransits(
        time_callback_indices, day_duration, day_duration, False, "Time"
    )
    time_dimension = router.GetDimensionOrDie("Time")
    for vehicle in data.vehicles.values():
        index = router.Start(vehicle.index)
        time_dimension.CumulVar(index).SetRange(0, day_duration)
        router.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(router.Start(vehicle.index))
        )
        router.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(router.End(vehicle.index))
        )

    for node_index, node in enumerate(data.nodes):
        if node.kind == models.NodeKind.ORIGIN or not node.package:
            continue

        index = manager.NodeToIndex(node_index)
        start_time = node.package.shipping_availability or scenario.day_start
        end_time = node.package.delivery_deadline or scenario.day_end
        start_seconds = start_time.duration_after(scenario.day_start)
        end_seconds = end_time.duration_after(scenario.day_start)
        time_dimension.CumulVar(index).SetRange(start_seconds, end_seconds)
        node_drop_penalty = settings.base_penalty
        node_drop_penalty *= day_duration / (end_seconds - start_seconds)
        req_vehicle_index = node.package.required_vehicle_index

        if req_vehicle_index:
            router.SetAllowedVehiclesForIndex([req_vehicle_index], index)
            node_drop_penalty *= settings.penalty_scale_req_vehicle

        if node.kind == models.NodeKind.PICKUP:
            node_drop_penalty *= settings.penalty_scale_pickups
            paired_index = manager.NodeToIndex(
                node.package.delivery_node_index(data.nodes)
            )
            router.AddPickupAndDelivery(index, paired_index)
            router.solver().Add(
                router.VehicleVar(index) == router.VehicleVar(paired_index)
            )
            router.solver().Add(
                distance_dimension.CumulVar(index)
                <= distance_dimension.CumulVar(paired_index)
            )
            for bundled_package in node.package.bundled_packages:
                linked_index = manager.NodeToIndex(
                    bundled_package.pickup_node_index(data.nodes)
                )
                router.solver().Add(
                    router.VehicleVar(index) == router.VehicleVar(linked_index)
                )

        router.AddDisjunction([index], int(node_drop_penalty))

    def capacity_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data.nodes[from_node].kind.capacity_impact

    router.AddDimensionWithVehicleCapacity(
        router.RegisterUnaryTransitCallback(capacity_callback),
        0,
        [vehicle.package_capacity for vehicle in data.vehicles.values()],
        True,
        "Capacity",
    )

    search = pywrapcp.DefaultRoutingSearchParameters()
    search.first_solution_strategy = settings.first_solution_strategy
    search.local_search_metaheuristic = settings.local_search_metaheuristic
    search.use_full_propagation = settings.use_full_propagation
    if settings.solver_time_limit_seconds:
        search.time_limit.seconds = settings.solver_time_limit_seconds
    if settings.solver_solution_limit:
        search.solution_limit = settings.solver_solution_limit
    search.log_search = settings.use_search_logging

    assignments = router.SolveWithParameters(search)

    if assignments:
        return models.Solution.save_solution(
            data, scenario, settings, manager, router, assignments
        )

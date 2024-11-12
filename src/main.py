from ortools.constraint_solver.routing_enums_pb2 import FirstSolutionStrategy as Fss
from ortools.constraint_solver.routing_enums_pb2 import LocalSearchMetaheuristic as Lsm

from delivery_route_planner import models, routing


def main() -> None:

    data = models.DataModel.with_defaults()
    scenario = models.RoutingScenario()
    settings = models.SearchSettings()

    """
    Enter the time in seconds you would like the solver to search.
    At least 60 seconds recommended, but more time may be needed on slower machines.
    In my experience, there are diminishing returns past 300 seconds.
    """
    settings.solver_time_limit_seconds = 60

    """
    The first solution strategy is the algorithm used to find an initial solution.
    Not all algorithms may find a solution, depending on time given to search.
    Some solutions may not utilize both vehicles, as total mileage is minimized.
    More information can be found at:
    <https://developers.google.com/optimization/routing/routing_options>

    Uncomment one line at a time for the option you would like to try.
    """
    # settings.first_solution_strategy = Fss.LOCAL_CHEAPEST_INSERTION
    settings.first_solution_strategy = Fss.LOCAL_CHEAPEST_COST_INSERTION
    # settings.first_solution_strategy = Fss.SEQUENTIAL_CHEAPEST_INSERTION
    # settings.first_solution_strategy = Fss.PARALLEL_CHEAPEST_INSERTION
    # settings.first_solution_strategy = Fss.BEST_INSERTION

    """
    The local search strategy is the metaheuristic algorithm used in the search.
    These algorithms are more advanced, allowing the solver to escape local minima.
    More information can be found at:
    <https://developers.google.com/optimization/routing/routing_options>

    Uncomment one line at a time for the option you would like to try.
    """
    # settings.local_search_metaheuristic = Lsm.SIMULATED_ANNEALING
    settings.local_search_metaheuristic = Lsm.GUIDED_LOCAL_SEARCH
    # settings.local_search_metaheuristic = Lsm.GREEDY_DESCENT
    # settings.local_search_metaheuristic = Lsm.TABU_SEARCH
    # settings.local_search_metaheuristic = Lsm.GENERIC_TABU_SEARCH

    solution = routing.solve_vehicle_routing_problem(data, scenario, settings)

    if solution:
        solution.print_solution()
    else:
        print("No solution found. Please adjust settings and try again.")


if __name__ == "__main__":
    main()

import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner import models, routing


def main(page: ft.Page) -> None:

    data = models.DataModel.with_defaults()
    scenario = models.RoutingScenario()
    settings = models.SearchSettings()

    def solve_button_clicked(e: ft.ControlEvent) -> None:

        if first_solution_strategy_dropdown.value:
            settings.first_solution_strategy = getattr(
                FirstSolutionStrategy,
                first_solution_strategy_dropdown.value,
            )

        if local_search_metaheuristic_dropdown.value:
            settings.local_search_metaheuristic = getattr(
                LocalSearchMetaheuristic,
                local_search_metaheuristic_dropdown.value,
            )

        if time_limit_slider.value:
            settings.solver_time_limit_seconds = int(time_limit_slider.value)

        solution = routing.solve_vehicle_routing_problem(data, scenario, settings)

        if solution:
            for route in solution.routes:
                results_content.controls.append(
                    ft.Text(f"Route for Vehicle {route.vehicle.id}")
                )

                route_rows = []
                route_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Package ID"), numeric=True),
                        ft.DataColumn(ft.Text("Activity")),
                        ft.DataColumn(ft.Text("Address")),
                        ft.DataColumn(ft.Text("Load"), numeric=True),
                        ft.DataColumn(ft.Text("Mileage"), numeric=True),
                        ft.DataColumn(ft.Text("Time")),
                    ],
                    rows=route_rows,
                )

                for stop in route.stops:
                    package_id = stop.node.package.id if stop.node.package else None
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(package_id))),
                            ft.DataCell(ft.Text(stop.node.kind.description)),
                            ft.DataCell(ft.Text(stop.node.address)),
                            ft.DataCell(ft.Text(str(stop.vehicle_load))),
                            ft.DataCell(ft.Text(str(round(stop.mileage, 1)))),
                            ft.DataCell(ft.Text(str(stop.visit_time))),
                        ],
                    )
                    route_rows.append(row)

                results_content.controls.append(route_table)

            results_content.controls.append(
                ft.Text(f"Total mileage: {round(solution.mileage, 1)}")
            )
            results_content.controls.append(
                ft.Text(f"Packages delivered: {solution.delivered_packages_count}")
            )
            results_content.controls.append(
                ft.Text(f"Packages missed: {solution.missed_packages_count}")
            )
            results_content.controls.append(
                ft.Text(f"Missed packages: {solution.missed_package_ids}")
            )
            results_content.controls.append(
                ft.Text(f"Delivery percentage: {solution.delivery_percentage}")
            )

        else:
            print("Solution not found.")

        page.update()

    solve_button = ft.FilledTonalButton(
        text="Solve",
        on_click=solve_button_clicked,
    )

    first_solution_strategy_dropdown = ft.Dropdown(
        label="First solution strategy",
        options=[
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_INSERTION",
                text="Local cheapest inserstion",
            ),
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_COST_INSERTION",
                text="Local cheapest cost insertion",
            ),
            ft.dropdown.Option(
                key="SEQUENTIAL_CHEAPEST_INSERTION",
                text="Sequential cheapest insertion",
            ),
            ft.dropdown.Option(
                key="PARALLEL_CHEAPEST_INSERTION",
                text="Parallel cheapest insertion",
            ),
            ft.dropdown.Option(
                key="BEST_INSERTION",
                text="Best insertion",
            ),
        ],
    )

    local_search_metaheuristic_dropdown = ft.Dropdown(
        label="Local search metaheuristic",
        options=[
            ft.dropdown.Option(
                key="SIMULATED_ANNEALING",
                text="Simulated annealing",
            ),
            ft.dropdown.Option(
                key="GUIDED_LOCAL_SEARCH",
                text="Guided local search",
            ),
            ft.dropdown.Option(
                key="GREEDY_DESCENT",
                text="Greedy descent",
            ),
            ft.dropdown.Option(
                key="TABU_SEARCH",
                text="Tabu search",
            ),
            ft.dropdown.Option(
                key="GENERIC_TABU_SEARCH",
                text="Generic tabu search",
            ),
        ],
    )

    time_limit_heading = ft.Text("Time limit in seconds:")
    time_limit_slider = ft.Slider(
        value=60,
        min=30,
        max=600,
        divisions=19,
        label="{value}",
    )

    setup_content = ft.Column(
        [
            first_solution_strategy_dropdown,
            local_search_metaheuristic_dropdown,
            time_limit_heading,
            time_limit_slider,
            solve_button,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    results_content = ft.Column(scroll=ft.ScrollMode.AUTO)

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(
                text="Setup",
                content=setup_content,
            ),
            ft.Tab(
                text="Results",
                content=results_content,
            ),
        ],
        expand=True,
    )

    page.add(tabs)


if __name__ == "__main__":
    ft.app(main)

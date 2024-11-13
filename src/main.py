import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner import models, routing


def _create_solution_charts(solution: models.Solution, charts_page: ft.Column) -> None:
    pass

def _create_solution_tables(
    solution: models.Solution, results_page: ft.Column,
) -> None:
    for route in solution.routes:
        results_page.controls.append(
            ft.Text(f"Route for Vehicle {route.vehicle.id}"),
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
            route_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(package_id))),
                        ft.DataCell(ft.Text(stop.node.kind.description)),
                        ft.DataCell(ft.Text(stop.node.address)),
                        ft.DataCell(ft.Text(str(stop.vehicle_load))),
                        ft.DataCell(ft.Text(str(round(stop.mileage, 1)))),
                        ft.DataCell(ft.Text(str(stop.visit_time))),
                    ],
                ),
            )

        results_page.controls.append(route_table)

    results_page.controls.extend(
        [
            ft.Text(f"Total mileage: {round(solution.mileage, 1)}"),
            ft.Text(f"Packages delivered: {solution.delivered_packages_count}"),
            ft.Text(f"Packages missed: {solution.missed_packages_count}"),
            ft.Text(f"Missed packages: {solution.missed_package_ids}"),
            ft.Text(f"Delivery percentage: {solution.delivery_percentage}"),
        ],
    )


def _create_setup_page(
    page: ft.Page,
    results_page: ft.Column,
    charts_page: ft.Column,
    data: models.DataModel,
    scenario: models.RoutingScenario,
    settings: models.SearchSettings,
) -> ft.Column:

    def _first_solution_strategy_selected(_e: ft.ControlEvent) -> None:
        if first_solution_strategy_dropdown.value:
            settings.first_solution_strategy = getattr(
                FirstSolutionStrategy,
                first_solution_strategy_dropdown.value,
            )

    def _local_search_metaheuristic_selected(_e: ft.ControlEvent) -> None:
        if local_search_metaheuristic_dropdown.value:
            settings.local_search_metaheuristic = getattr(
                LocalSearchMetaheuristic,
                local_search_metaheuristic_dropdown.value,
            )

    def _time_limit_slider_changed(_e: ft.ControlEvent) -> None:
        if time_limit_slider.value:
            settings.solver_time_limit_seconds = int(time_limit_slider.value)

    def _solve_button_clicked(_e: ft.ControlEvent) -> None:
        results_page.controls.clear()

        solution = routing.solve_vehicle_routing_problem(data, scenario, settings)

        if solution:
            _create_solution_tables(solution, results_page)
            _create_solution_charts(solution, charts_page)
        else:
            results_page.controls.append(
                ft.Text("Solution not found. Please adjust settings and try again."),
            )

        page.update()

    solve_button = ft.FilledTonalButton(
        text="Solve",
        on_click=_solve_button_clicked,
    )

    first_solution_strategy_dropdown = ft.Dropdown(
        label="First solution strategy",
        on_change=_first_solution_strategy_selected,
        options=[
            ft.dropdown.Option("LOCAL_CHEAPEST_INSERTION"),
            ft.dropdown.Option("LOCAL_CHEAPEST_COST_INSERTION"),
            ft.dropdown.Option("SEQUENTIAL_CHEAPEST_INSERTION"),
            ft.dropdown.Option("PARALLEL_CHEAPEST_INSERTION"),
            ft.dropdown.Option("BEST_INSERTION"),
        ],
    )

    local_search_metaheuristic_dropdown = ft.Dropdown(
        label="Local search metaheuristic",
        on_change=_local_search_metaheuristic_selected,
        options=[
            ft.dropdown.Option("SIMULATED_ANNEALING"),
            ft.dropdown.Option("GUIDED_LOCAL_SEARCH"),
            ft.dropdown.Option("GREEDY_DESCENT"),
            ft.dropdown.Option("TABU_SEARCH"),
            ft.dropdown.Option("GENERIC_TABU_SEARCH"),
        ],
    )

    time_limit_heading = ft.Text("Time limit in seconds:")
    time_limit_slider = ft.Slider(
        value=120,
        min=30,
        max=600,
        divisions=19,
        label="{value}",
        on_change=_time_limit_slider_changed,
    )

    return ft.Column(
        [
            first_solution_strategy_dropdown,
            local_search_metaheuristic_dropdown,
            time_limit_heading,
            time_limit_slider,
            solve_button,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

def main(page: ft.Page) -> None:

    data = models.DataModel.with_defaults()
    scenario = models.RoutingScenario()
    settings = models.SearchSettings()

    results_page = ft.Column(scroll=ft.ScrollMode.AUTO)
    charts_page = ft.Column(scroll=ft.ScrollMode.AUTO)

    setup_page = _create_setup_page(page, results_page, charts_page, data, scenario, settings)

    page_tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Setup", content=setup_page),
            ft.Tab(text="Results", content=results_page),
            ft.Tab(text="Charts", content=charts_page),
        ],
        expand=True,
    )

    page.add(page_tabs)


if __name__ == "__main__":
    ft.app(main)

import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner import models, routing


def _create_solution_charts(solution: models.Solution, charts_content: ft.Column) -> None:
    for route in solution.routes:
        charts_content.controls.append(
            ft.Text(f"Package Load vs Capacity for Vehicle {route.vehicle.id}"),
        )
        bar_groups = []
        capacity_chart = ft.BarChart(
            bar_groups = bar_groups,
            left_axis=ft.ChartAxis(
                title=ft.Text("Number of packages"), 
                title_size=40,
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Stops along route"),
                show_labels=False,
            ),
            max_y=route.vehicle.package_capacity + 2,
            border=ft.border.all(1, ft.colors.GREY_400),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=route.vehicle.package_capacity,
                color=ft.colors.ERROR_CONTAINER,
                width=1,
                dash_pattern=[3, 3],
            ),
        )
        for i, stop in enumerate(route.stops):
            if stop.node.kind == models.NodeKind.ORIGIN:
                continue
            package_id = stop.node.package.id if stop.node.package else None
            activity = stop.node.kind.description
            bar = ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        to_y=stop.vehicle_load,
                        tooltip=f"Package {package_id}: {activity}",
                    ),
                ],
            )
            bar_groups.append(bar)
        charts_content.controls.append(capacity_chart)


def _create_solution_tables(solution: models.Solution, results_content: ft.Column) -> None:
    for route in solution.routes:
        results_content.controls.append(
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

        results_content.controls.append(route_table)

    results_content.controls.extend(
        [
            ft.Text(f"Total mileage: {round(solution.mileage, 1)}"),
            ft.Text(f"Packages delivered: {solution.delivered_packages_count}"),
            ft.Text(f"Packages missed: {solution.missed_packages_count}"),
            ft.Text(f"Missed packages: {solution.missed_package_ids}"),
            ft.Text(f"Delivery percentage: {solution.delivery_percentage}"),
        ],
    )


def create_setup_content(
    page: ft.Page,
    results_content: ft.Column,
    charts_content: ft.Column,
    data: models.DataModel,
) -> ft.Column:

    def _solve_button_clicked(_e: ft.ControlEvent) -> None:
        results_content.controls.clear()
        charts_content.controls.clear()

        loading_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Searching for routes..."),
            content=ft.ProgressBar(width=400),
        )
        page.open(loading_dialog)

        data.solution = routing.solve_vehicle_routing_problem(data)

        page.close(loading_dialog)

        if data.solution:
            _create_solution_tables(data.solution, results_content)
            _create_solution_charts(data.solution, charts_content)
        else:
            results_content.controls.append(
                ft.Text("Solution not found. Please adjust settings and try again."),
            )
            charts_content.controls.append(
                ft.Text("Solution not found. Please adjust settings and try again."),
            )

        page.update()

    def _first_solution_strategy_selected(_e: ft.ControlEvent) -> None:
        if first_solution_strategy_dropdown.value:
            data.settings.first_solution_strategy = getattr(
                FirstSolutionStrategy,
                first_solution_strategy_dropdown.value,
            )

    def _local_search_metaheuristic_selected(_e: ft.ControlEvent) -> None:
        if local_search_metaheuristic_dropdown.value:
            data.settings.local_search_metaheuristic = getattr(
                LocalSearchMetaheuristic,
                local_search_metaheuristic_dropdown.value,
            )

    def _time_limit_slider_changed(_e: ft.ControlEvent) -> None:
        limit = int(time_limit_slider.value)
        data.settings.solver_time_limit_seconds = limit
        time_limit_heading.value = f"Time limit in seconds: {limit}"
        page.update()

    solve_button = ft.FloatingActionButton(
        text="Solve",
        icon=ft.icons.AUTO_AWESOME_ROUNDED,
        on_click=_solve_button_clicked,
    )

    first_solution_strategy_dropdown = ft.Dropdown(
        label="First solution strategy",
        on_change=_first_solution_strategy_selected,
        width=350,
        border_color=ft.colors.SURFACE_VARIANT,
        fill_color=ft.colors.ON_INVERSE_SURFACE,
        content_padding=10,
        border_radius=10,
        options=[
            ft.dropdown.Option(key="LOCAL_CHEAPEST_INSERTION", text="Local cheapest insertion"),
            ft.dropdown.Option(key="LOCAL_CHEAPEST_COST_INSERTION", text="Local cheapest cost insertion"),
            ft.dropdown.Option(key="SEQUENTIAL_CHEAPEST_INSERTION", text="Sequential cheapest insertion"),
            ft.dropdown.Option(key="PARALLEL_CHEAPEST_INSERTION", text="Parallel cheapest insertion"),
            ft.dropdown.Option(key="BEST_INSERTION", text="Best insertion"),
        ],
    )

    local_search_metaheuristic_dropdown = ft.Dropdown(
        label="Local search metaheuristic",
        on_change=_local_search_metaheuristic_selected,
        width=350,
        border_color=ft.colors.SURFACE_VARIANT,
        fill_color=ft.colors.ON_INVERSE_SURFACE,
        content_padding=10,
        border_radius=10,
        options=[
            ft.dropdown.Option("SIMULATED_ANNEALING"),
            ft.dropdown.Option("GUIDED_LOCAL_SEARCH"),
            ft.dropdown.Option("GREEDY_DESCENT"),
            ft.dropdown.Option("TABU_SEARCH"),
            ft.dropdown.Option("GENERIC_TABU_SEARCH"),
        ],
    )

    time_limit_heading = ft.Text("Time limit in seconds: 120")
    time_limit_slider = ft.Slider(
        value=120,
        min=15,
        max=300,
        divisions=19,
        label="{value}",
        width=400,
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
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner import models, routing


def _create_solution_charts(
    solution: models.Solution, charts_content: ft.Column,
) -> None:

    charts_content.controls.append(ft.Container(height=10))

    for route in solution.routes:
        chart_title = ft.Text(
            f"Package Load vs Capacity for Vehicle {route.vehicle.id}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )
        bar_groups = []
        capacity_chart = ft.BarChart(
            bar_groups=bar_groups,
            left_axis=ft.ChartAxis(
                title=ft.Text(
                    "Number of packages",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                labels_size=30,
                title_size=30,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text(
                    "Route steps",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                labels_size=30,
                title_size=30,
            ),
            max_y=route.vehicle.package_capacity + 2,
            tooltip_fit_inside_horizontally=False,
            tooltip_bgcolor=ft.colors.ON_INVERSE_SURFACE,
            border=ft.border.all(1, ft.colors.GREY_400),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=route.vehicle.package_capacity,
                color=ft.colors.ERROR,
                width=2,
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
                        color=ft.colors.PRIMARY,
                        width=15,
                        border_radius=5,
                        tooltip=f"{activity}: package {package_id}",
                    ),
                ],
            )
            bar_groups.append(bar)


        charts_content.controls.append(
            ft.Card(
                ft.Container(
                    ft.Column(
                        [
                            chart_title,
                            capacity_chart,
                        ],
                        spacing=20,
                    ),
                    padding=30,
                ),
                color=ft.colors.SURFACE,
                elevation=2,
            ),
        )

    charts_content.controls.append(ft.Container(height=10))

def _create_solution_tables(
    solution: models.Solution, results_content: ft.Column,
) -> None:

    results_content.controls.append(ft.Container(height=10))

    results_stats = ft.Column(
        [
            ft.Text(
                f"Total mileage: {round(solution.mileage, 1)}",
                theme_style=ft.TextThemeStyle.TITLE_LARGE,
            ),
            ft.Text(
                f"Delivery percentage: {solution.delivery_percentage}",
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            ),
            ft.Text(f"Packages delivered: {solution.delivered_packages_count}"),
            ft.Text(f"Packages missed: {solution.missed_packages_count}"),
        ],
    )
    if solution.missed_packages_count > 0:
        results_stats.controls.append(
            ft.Text(f"Missed packages: {solution.missed_package_ids}"),
        )

    results_content.controls.append(
        ft.Card(
            ft.Container(results_stats, padding=30),
            width=500,
            color=ft.colors.SURFACE,
            elevation=2,
        ),
    )

    for route in solution.routes:
        results_content.controls.append(
            ft.Text(
                f"Route for Vehicle {route.vehicle.id}",
                theme_style=ft.TextThemeStyle.TITLE_LARGE,
            ),
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
            bgcolor=ft.colors.SURFACE,
            border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
            border_radius=15,
            vertical_lines=ft.BorderSide(1, ft.colors.SURFACE_VARIANT),
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

    results_content.controls.append(ft.Container(height=10))

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
        time_limit_value_callout.value = f"{limit} seconds"
        if limit < 60:
            time_limit_slider.active_color = ft.colors.ERROR
            time_limit_value_callout.color = ft.colors.ERROR
        else:
            time_limit_slider.active_color = None
            time_limit_value_callout.color = None
        page.update()

    solve_button = ft.FloatingActionButton(
        text="Solve",
        icon=ft.icons.AUTO_AWESOME_ROUNDED,
        on_click=_solve_button_clicked,
        bgcolor=ft.colors.SURFACE,
        elevation=2,
    )

    first_solution_strategy_dropdown = ft.Dropdown(
        label="First solution strategy",
        on_change=_first_solution_strategy_selected,
        width=500,
        border_color=ft.colors.OUTLINE_VARIANT,
        fill_color=ft.colors.SURFACE,
        content_padding=10,
        border_radius=10,
        focused_border_width=0,
        options=[
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_INSERTION", text="Local cheapest insertion"
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
                key="PARALLEL_CHEAPEST_INSERTION", text="Parallel cheapest insertion"
            ),
            ft.dropdown.Option(key="BEST_INSERTION", text="Best insertion"),
        ],
    )

    local_search_metaheuristic_dropdown = ft.Dropdown(
        label="Local search metaheuristic",
        on_change=_local_search_metaheuristic_selected,
        width=500,
        border_color=ft.colors.OUTLINE_VARIANT,
        fill_color=ft.colors.SURFACE,
        content_padding=10,
        border_radius=10,
        focused_border_width=0,
        options=[
            ft.dropdown.Option(key="SIMULATED_ANNEALING", text="Simulated annealing"),
            ft.dropdown.Option(key="GUIDED_LOCAL_SEARCH", text="Guided local search"),
            ft.dropdown.Option(key="GREEDY_DESCENT", text="Greedy descent"),
            ft.dropdown.Option(key="TABU_SEARCH", text="Tabu search"),
            ft.dropdown.Option(key="GENERIC_TABU_SEARCH", text="Generic tabu search"),
        ],
    )

    time_limit_slider = ft.Slider(
        value=120,
        min=15,
        max=300,
        divisions=19,
        label=" {value} seconds ",
        on_change=_time_limit_slider_changed,
    )

    time_limit_value_callout = ft.Text(
        "120 seconds", theme_style=ft.TextThemeStyle.HEADLINE_SMALL
    )
    time_limit_card = ft.Card(
        ft.Container(
            ft.Column(
                [
                    ft.ListTile(
                        title=ft.Text("Time limit"),
                        subtitle=ft.Text(
                            "Longer searches will yield better results.\nAt least 120 seconds recommended."
                        ),
                        trailing=time_limit_value_callout,
                    ),
                    time_limit_slider,
                ],
            ),
            padding=10,
        ),
        width=500,
        color=ft.colors.SURFACE,
        elevation=2,
    )

    return ft.Column(
        [
            first_solution_strategy_dropdown,
            local_search_metaheuristic_dropdown,
            time_limit_card,
            solve_button,
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

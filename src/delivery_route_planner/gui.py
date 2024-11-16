import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner import models, routing


def _create_pie_chart(
    solution: models.Solution,
    charts_content: ft.Column,
) -> None:

    pie_chart_title = ft.Text(
        "Mileage per Vehicle",
        theme_style=ft.TextThemeStyle.TITLE_LARGE,
    )

    pie_chart_sections = []
    for route in solution.routes:
        if route.vehicle.id == 1:
            color = ft.colors.PRIMARY
        elif route.vehicle.id == 2:
            color = ft.colors.TERTIARY
        else:
            color = ft.colors.random_color()
        mileage_percentage = route.mileage / solution.mileage
        pie_chart_sections.append(
            ft.PieChartSection(
                value=mileage_percentage,
                color=color,
                title=f"Vehicle {route.vehicle.id}: {round(mileage_percentage * 100, 2)}%",
                title_style=ft.TextStyle(color=ft.colors.WHITE),
                radius=150,
            ),
        )

    pie_chart = ft.PieChart(
        sections=pie_chart_sections,
        center_space_radius=0,
    )

    charts_content.controls.append(
        ft.Card(
            ft.Container(
                ft.Column(
                    [
                        pie_chart_title,
                        pie_chart,
                    ],
                    spacing=20,
                ),
                padding=30,
            ),
            color=ft.colors.SURFACE,
            elevation=2,
        ),
    )

def _create_line_chart(
    solution: models.Solution,
    charts_content: ft.Column,
) -> None:

    mileage_chart_title = ft.Text(
        "Mileage Along Routes",
        theme_style=ft.TextThemeStyle.TITLE_LARGE,
    )

    line_chart_data = []
    for route in solution.routes:
        data_points = [
            ft.LineChartDataPoint(
                x=i,
                y=round(stop.mileage, 1),
                tooltip=f"Vehicle {route.vehicle.id}: {round(stop.mileage, 1)}",
            )
            for i, stop in enumerate(route.stops)
        ]
        if route.vehicle.id == 1:
            color = ft.colors.PRIMARY
        elif route.vehicle.id == 2:
            color = ft.colors.TERTIARY
        else:
            color = ft.colors.random_color()
        line_chart_data.append(
            ft.LineChartData(
                data_points,
                stroke_width=5,
                curved=True,
                color=color,
                stroke_cap_round=True,
            ),
        )

    mileage_chart = ft.LineChart(
        data_series=line_chart_data,
        left_axis=ft.ChartAxis(
            title=ft.Text(
                "Mileage",
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            ),
            labels_size=40,
            title_size=40,
            labels_interval=5,
        ),
        bottom_axis=ft.ChartAxis(
            title=ft.Text(
                "Route Steps",
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            ),
            labels_size=30,
            title_size=30,
        ),
        tooltip_bgcolor=ft.colors.ON_INVERSE_SURFACE,
        tooltip_fit_inside_horizontally=False,
        tooltip_fit_inside_vertically=False,
        border=ft.border.all(1, ft.colors.GREY_400),
    )
    charts_content.controls.append(
        ft.Card(
            ft.Container(
                ft.Column(
                    [
                        mileage_chart_title,
                        mileage_chart,
                    ],
                    spacing=20,
                ),
                padding=30,
            ),
            color=ft.colors.SURFACE,
            elevation=2,
        ),
    )


def _create_bar_charts(
    solution: models.Solution,
    charts_content: ft.Column,
) -> None:

    for route in solution.routes:
        capacity_chart_title = ft.Text(
            f"Package Load vs Capacity: Vehicle {route.vehicle.id}",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )
        bar_groups = []
        capacity_chart = ft.BarChart(
            bar_groups=bar_groups,
            left_axis=ft.ChartAxis(
                title=ft.Text(
                    "Number of Packages",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                labels_size=30,
                title_size=30,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text(
                    "Route Steps",
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                labels_size=30,
                title_size=30,
            ),
            max_y=route.vehicle.package_capacity + 2,
            tooltip_bgcolor=ft.colors.ON_INVERSE_SURFACE,
            border=ft.border.all(1, ft.colors.GREY_400),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=route.vehicle.package_capacity,
                color=ft.colors.ERROR,
                width=2,
                dash_pattern=[6, 3],
            ),
        )
        for i, stop in enumerate(route.stops):
            bar = ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        to_y=stop.vehicle_load,
                        color=ft.colors.PRIMARY,
                        width=10,
                        border_radius=5,
                    ),
                ],
            )
            bar_groups.append(bar)

        charts_content.controls.append(
            ft.Card(
                ft.Container(
                    ft.Column(
                        [
                            capacity_chart_title,
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


def _create_solution_tables(
    solution: models.Solution,
    results_content: ft.Column,
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
                ft.DataColumn(ft.Text("Step"), numeric=True),
                ft.DataColumn(ft.Text("Activity")),
                ft.DataColumn(ft.Text("Package ID"), numeric=True),
                ft.DataColumn(ft.Text("Address")),
                ft.DataColumn(ft.Text("Load"), numeric=True),
                ft.DataColumn(ft.Text("Mileage"), numeric=True),
                ft.DataColumn(ft.Text("Time")),
            ],
            rows=route_rows,
            bgcolor=ft.colors.SURFACE,
            border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.colors.SURFACE_VARIANT),
        )

        for i, stop in enumerate(route.stops):
            package_id = stop.node.package.id if stop.node.package else None
            activity = stop.node.kind.description
            if stop.node.kind == models.NodeKind.ORIGIN:
                activity = "Start" if i == 0 else "End"
            route_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(i))),
                        ft.DataCell(ft.Text(activity)),
                        ft.DataCell(ft.Text(str(package_id))),
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

        def close_results_dialog(_e: ft.ControlEvent) -> None:
            page.close(results_dialog)

        results_dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text("Routing complete!"),
            content=ft.Text(
                "Please see the Routes and Charts tabs to view the results.",
            ),
            actions=[ft.FilledTonalButton("Okay", on_click=close_results_dialog)],
        )

        if data.solution:
            _create_solution_tables(data.solution, results_content)

            charts_content.controls.append(ft.Container(height=10))
            _create_line_chart(data.solution, charts_content)
            _create_pie_chart(data.solution, charts_content)
            _create_bar_charts(data.solution, charts_content)
            charts_content.controls.append(ft.Container(height=10))

            page.open(results_dialog)

        else:
            results_content.controls.append(
                ft.Text(
                    "Solution could not be found. Please adjust settings and try again."
                ),
            )
            charts_content.controls.append(
                ft.Text(
                    "Solution could not be found. Please adjust settings and try again."
                ),
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
        label="First Solution Strategy",
        on_change=_first_solution_strategy_selected,
        width=600,
        border_color=ft.colors.OUTLINE_VARIANT,
        fill_color=ft.colors.SURFACE,
        content_padding=10,
        border_radius=10,
        focused_border_width=0,
        options=[
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_INSERTION", text="Local Cheapest Insertion"
            ),
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_COST_INSERTION",
                text="Local Cheapest Cost Insertion",
            ),
            ft.dropdown.Option(
                key="SEQUENTIAL_CHEAPEST_INSERTION",
                text="Sequential Cheapest Insertion",
            ),
            ft.dropdown.Option(
                key="PARALLEL_CHEAPEST_INSERTION",
                text="Parallel Cheapest Insertion",
            ),
            ft.dropdown.Option(key="BEST_INSERTION", text="Best Insertion"),
        ],
    )

    local_search_metaheuristic_dropdown = ft.Dropdown(
        label="Local Search Metaheuristic",
        on_change=_local_search_metaheuristic_selected,
        width=600,
        border_color=ft.colors.OUTLINE_VARIANT,
        fill_color=ft.colors.SURFACE,
        content_padding=10,
        border_radius=10,
        focused_border_width=0,
        options=[
            ft.dropdown.Option(key="GUIDED_LOCAL_SEARCH", text="Guided Local Search"),
            ft.dropdown.Option(key="GREEDY_DESCENT", text="Greedy Descent"),
            ft.dropdown.Option(key="SIMULATED_ANNEALING", text="Simulated Annealing"),
            ft.dropdown.Option(key="TABU_SEARCH", text="Tabu Search"),
            ft.dropdown.Option(key="GENERIC_TABU_SEARCH", text="Generic Tabu Search"),
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
                        title=ft.Text("Time Limit"),
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
        width=600,
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

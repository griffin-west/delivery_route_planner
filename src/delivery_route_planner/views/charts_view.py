import flet as ft

from delivery_route_planner.models import models


class ChartsView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.solution = None
        self.title = "Charts"
        self.icon = ft.icons.INSERT_CHART_OUTLINED_ROUNDED
        self.selected_icon = ft.icons.INSERT_CHART_ROUNDED
        self.disabled = True

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        save_as_file_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.SAVE_AS_ROUNDED),
            title=ft.Text("Save charts as file", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Text("This feature is not yet available."),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(save_as_file_dialog),
                ),
            ],
        )
        save_as_file_button = ft.FilledTonalButton(
            "Save as file",
            ft.icons.SAVE_AS_OUTLINED,
            on_click=lambda _: self.page.open(save_as_file_dialog),
        )
        header = ft.Container(
            ft.Row(
                [title, save_as_file_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            controls=[
                self.build_pie_charts(),
                self.build_bar_charts(),
                self.build_line_chart(),
                ft.Container(),
            ],
            spacing=30,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        return ft.Column(
            [header, body],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def set_solution(self, solution: models.Solution) -> None:
        self.solution = solution

    def build_pie_charts(self) -> ft.Container:
        if not self.solution:
            return ft.Container()

        mileage_pie = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    (route.mileage / self.solution.mileage * 100),
                    title=f"Vehicle {route.vehicle.id}\n"
                    f"{round(route.mileage / self.solution.mileage * 100, 1)}%\n"
                    f"{round(route.mileage, 1)} miles",
                    title_style=ft.TextStyle(color=ft.colors.ON_PRIMARY),
                    color=(
                        ft.colors.PRIMARY
                        if route.vehicle.id == 1
                        else (
                            ft.colors.TERTIARY
                            if route.vehicle.id == 2
                            else ft.colors.SECONDARY
                        )
                    ),
                    radius=150,
                )
                for route in self.solution.routes
            ],
            center_space_radius=0,
            start_degree_offset=180,
        )

        def time_label(seconds: int) -> str:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            hour_str = "hour" if hours == 1 else "hours"
            minute_str = "minute" if minutes == 1 else "minutes"
            return f"{hours} {hour_str} and\n{minutes} {minute_str}"

        time_pie = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    (route.time_used_seconds / self.solution.time_used_seconds * 100),
                    title=f"Vehicle {route.vehicle.id}\n"
                    f"{round(route.time_used_seconds / self.solution.time_used_seconds * 100, 1)}%\n"
                    f"{time_label(route.time_used_seconds)}",
                    title_style=ft.TextStyle(color=ft.colors.ON_PRIMARY),
                    color=(
                        ft.colors.PRIMARY
                        if route.vehicle.id == 1
                        else (
                            ft.colors.TERTIARY
                            if route.vehicle.id == 2
                            else ft.colors.SECONDARY
                        )
                    ),
                    radius=150,
                )
                for route in self.solution.routes
            ],
            center_space_radius=0,
            start_degree_offset=180,
        )

        mileage_pie_card = ft.Card(
            content=ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "Vehicle Utilization by Mileage",
                            style=ft.TextThemeStyle.TITLE_MEDIUM,
                        ),
                        mileage_pie,
                    ],
                    spacing=20,
                ),
                padding=20,
                width=400,
            ),
            variant=ft.CardVariant.FILLED,
        )

        time_pie_card = ft.Card(
            content=ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            "Vehicle Utilization by Time",
                            style=ft.TextThemeStyle.TITLE_MEDIUM,
                        ),
                        time_pie,
                    ],
                    spacing=20,
                ),
                padding=20,
                width=400,
            ),
            variant=ft.CardVariant.FILLED,
        )

        return ft.Container(
            content=ft.Row(
                [
                    mileage_pie_card,
                    time_pie_card,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=30,
                wrap=True,
                run_spacing=30,
            ),
            padding=ft.padding.only(30, 0, 0, 0),
        )

    def build_bar_charts(self) -> ft.Container:
        if not self.solution:
            return ft.Container()

        capacity_charts = []
        for route in self.solution.routes:
            bars = []
            capacity_chart = ft.BarChart(
                bar_groups=bars,
                left_axis=ft.ChartAxis(
                    title=ft.Text("Number of Packages"),
                    title_size=30,
                    labels_size=30,
                    show_labels=True,
                    labels_interval=4,
                ),
                bottom_axis=ft.ChartAxis(
                    title=ft.Text("Route Steps"),
                    title_size=30,
                    labels_size=30,
                    show_labels=True,
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                    interval=route.vehicle.package_capacity,
                    color=ft.colors.ERROR,
                    dash_pattern=[3, 3],
                ),
                max_y=route.vehicle.package_capacity + 2,
                tooltip_bgcolor=ft.colors.SURFACE,
            )

            step = 1
            for this_stop, next_stop in zip(route.stops[1:], route.stops[2:]):
                if (
                    next_stop
                    and this_stop.node.kind == next_stop.node.kind
                    and this_stop.node.address == next_stop.node.address
                ):
                    continue
                bars.append(
                    ft.BarChartGroup(
                        x=step,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=this_stop.vehicle_load,
                                color=(
                                    ft.colors.PRIMARY
                                    if route.vehicle.id == 1
                                    else (
                                        ft.colors.TERTIARY
                                        if route.vehicle.id == 2
                                        else ft.colors.SECONDARY
                                    )
                                ),
                                width=25,
                                border_radius=5,
                            ),
                        ],
                    ),
                )
                step = step + 1

            capacity_chart.width = max(300, (step * 30))

            capacity_chart_card = ft.Card(
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Text(
                                f"Load vs Capacity: Vehicle {route.vehicle.id}",
                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                            ),
                            capacity_chart,
                        ],
                        spacing=30,
                    ),
                    padding=20,
                ),
                variant=ft.CardVariant.FILLED,
            )
            capacity_charts.append(
                ft.Row(
                    [capacity_chart_card],
                    scroll=ft.ScrollMode.AUTO,
                ),
            )

        return ft.Container(
            content=ft.Row(
                controls=capacity_charts,
                spacing=30,
                wrap=True,
                run_spacing=30,
            ),
            padding=ft.padding.only(30, 0, 0, 0),
        )

    def build_line_chart(self) -> ft.Container:
        if not self.solution:
            return ft.Container()

        data_series = []
        for route in self.solution.routes:
            data_points = []
            step = 1
            for this_stop, next_stop in zip(route.stops[1:], route.stops[2:] + [None]):
                if (
                    next_stop
                    and this_stop.node.kind == next_stop.node.kind
                    and this_stop.node.address == next_stop.node.address
                ):
                    continue
                data_points.append(
                    ft.LineChartDataPoint(
                        x=this_stop.visit_time.seconds,
                        y=round(this_stop.mileage, 1),
                        point=ft.ChartCirclePoint(radius=5),
                    ),
                )
                step = step + 1
            data_series.append(
                ft.LineChartData(
                    data_points=data_points,
                    stroke_width=5,
                    stroke_cap_round=True,
                    curved=True,
                    color=(
                        ft.colors.PRIMARY
                        if route.vehicle.id == 1
                        else (
                            ft.colors.TERTIARY
                            if route.vehicle.id == 2
                            else ft.colors.SECONDARY
                        )
                    ),
                ),
            )

        line_chart = ft.LineChart(
            data_series=data_series,
            left_axis=ft.ChartAxis(
                title=ft.Text("Mileage"),
                title_size=30,
                labels_size=30,
                show_labels=True,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Time"),
                title_size=30,
                labels_size=30,
                show_labels=True,
                labels_interval=1800,
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Text(models.RoutingTime.from_seconds(i).short_str),
                    )
                    for i in range(
                        self.solution.data.scenario.day_start.seconds,
                        self.solution.end_time.seconds,
                        1800,
                    )
                ],
            ),
            width=1200,
            tooltip_bgcolor=ft.colors.SURFACE,
            horizontal_grid_lines=ft.ChartGridLines(10),
            vertical_grid_lines=ft.ChartGridLines(900),
            max_y=round(
                (max(route.mileage for route in self.solution.routes) * 1.1), 0
            ),
        )

        vehicle_labels = ft.Column(
            [
                ft.Text(
                    f"Vehicle {route.vehicle.id}",
                    color=(
                        ft.colors.PRIMARY
                        if route.vehicle.id == 1
                        else (
                            ft.colors.TERTIARY
                            if route.vehicle.id == 2
                            else ft.colors.SECONDARY
                        )
                    ),
                    font_family="Outfit-Bold",
                )
                for route in self.solution.routes
            ],
        )

        line_chart_card = ft.Card(
            content=ft.Container(
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Mileage Over Time",
                                    style=ft.TextThemeStyle.TITLE_MEDIUM,
                                ),
                                line_chart,
                            ],
                            spacing=30,
                        ),
                        vehicle_labels,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=20,
            ),
            variant=ft.CardVariant.FILLED,
        )

        return ft.Container(
            content=ft.Row(
                [
                    line_chart_card,
                    ft.Container(width=30),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.only(30, 0, 0, 0),
        )

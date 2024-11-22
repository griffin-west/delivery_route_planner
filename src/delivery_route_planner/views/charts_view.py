import flet as ft

from delivery_route_planner.models import models


class ChartsView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.solution = None
        self.title = "Charts"
        self.icon = ft.icons.BAR_CHART_ROUNDED
        self.selected_icon = ft.icons.BAR_CHART_ROUNDED
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
                self._build_bar_charts(),
            ],
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

    def _build_bar_charts(self) -> ft.Container:
        if not self.solution:
            return ft.Container()

        route_bar_charts = ft.Column(spacing=30)
        for route in self.solution.routes:
            bar_groups = []
            bottom_axis_labels = []
            route_capacity_chart = ft.BarChart(
                bar_groups=bar_groups,
                top_axis=ft.ChartAxis(
                    title=ft.Text(
                        f"Capacity vs Load: Vehicle {route.vehicle.id}",
                        style=ft.TextThemeStyle.TITLE_MEDIUM,
                    ),
                    title_size=40,
                    show_labels=False,
                ),
                left_axis=ft.ChartAxis(
                    title=ft.Text("Number of Packages"),
                    title_size=40,
                    labels_size=40,
                    labels_interval=4,
                ),
                bottom_axis=ft.ChartAxis(
                    title=ft.Text("Route Steps"),
                    title_size=40,
                    labels=bottom_axis_labels,
                    labels_size=40,
                ),
                border=ft.border.all(2, ft.colors.SECONDARY_CONTAINER),
                horizontal_grid_lines=ft.ChartGridLines(
                    interval=route.vehicle.package_capacity,
                    color=ft.colors.ERROR,
                    dash_pattern=[6, 3],
                    width=1,
                ),
                tooltip_bgcolor=ft.colors.SURFACE_VARIANT,
                max_y=route.vehicle.package_capacity + 2,
            )

            step = 1
            for this_stop, next_stop in zip(route.stops[1:], route.stops[2:]):
                if (
                    next_stop
                    and this_stop.node.kind == next_stop.node.kind
                    and this_stop.node.address == next_stop.node.address
                ):
                    continue
                bar_groups.append(
                    ft.BarChartGroup(
                        x=(step - 1),
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=this_stop.vehicle_load,
                                color=ft.colors.PRIMARY,
                                border_radius=10,
                                width=30,
                            ),
                        ],
                    ),
                )
                bottom_axis_labels.append(
                    ft.ChartAxisLabel(
                        value=(step - 1),
                        label=ft.Text(f"{step}"),
                    ),
                )
                step = step + 1

            route_bar_charts.controls.append(route_capacity_chart)

        return ft.Container(
            content=ft.Column(
                [
                    route_bar_charts,
                ],
                spacing=30,
            ),
            padding=ft.padding.only(30, 0, 30, 30),
        )

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
                self._build_charts(),
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

    def _build_charts(self) -> ft.Container:
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
                        else ft.colors.TERTIARY
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
                    ft.Container(width=30),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=30,
            ),
            padding=ft.padding.only(30, 0, 0, 30),
        )

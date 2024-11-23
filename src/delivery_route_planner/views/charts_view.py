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

        return ft.Container(
            content=ft.Row(
                [],
                scroll=ft.ScrollMode.AUTO,
                spacing=30,
            ),
            padding=ft.padding.only(30, 0, 0, 30),
        )

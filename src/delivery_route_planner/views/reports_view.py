import flet as ft

from delivery_route_planner.models import models


class ReportsView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.solution = None
        self.title = "Reports"
        self.icon = ft.icons.BAR_CHART_ROUNDED
        self.selected_icon = ft.icons.BAR_CHART_ROUNDED
        self.disabled = True

    def render(self) -> ft.Column:
        if self.page.theme:
            self.page.theme.color_scheme_seed = ft.colors.DEEP_PURPLE
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        header = ft.Container(
            ft.Row(
                [title],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        return ft.Column([header, body])

    def set_solution(self, solution: models.Solution) -> None:
        self.solution = solution

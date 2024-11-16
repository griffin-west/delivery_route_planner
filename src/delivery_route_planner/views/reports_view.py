import flet as ft


class ReportsView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title = "Reports"
        self.icon = ft.icons.BAR_CHART_ROUNDED
        self.selected_icon = ft.icons.BAR_CHART_ROUNDED
        self.disabled = True

    def render(self) -> ft.Column:
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

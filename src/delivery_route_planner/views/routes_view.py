import flet as ft


class RoutesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title = "Routes"
        self.icon = ft.icons.ROUTE_OUTLINED
        self.selected_icon = ft.icons.ROUTE_ROUNDED
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

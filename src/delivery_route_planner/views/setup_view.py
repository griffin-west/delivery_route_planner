import flet as ft


class SetupView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title = "Setup"
        self.icon = ft.icons.EDIT_OUTLINED
        self.selected_icon = ft.icons.EDIT_ROUNDED
        self.disabled = False

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        reset_button = ft.FilledTonalButton("Reset defaults", ft.icons.REFRESH_ROUNDED)
        header = ft.Container(
            ft.Row(
                [title, reset_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Column([header, body])

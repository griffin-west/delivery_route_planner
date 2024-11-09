import flet as ft


class ViewPane:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.content = ft.Column(expand=True)

    def render(self) -> ft.Container:
        return ft.Container(
            content=self.content,
            margin=ft.margin.only(0, 0, 24, 24),
            border_radius=20,
            expand=True,
            bgcolor=ft.colors.SURFACE,
            padding=30,
            border=ft.border.all(1, ft.colors.SURFACE_VARIANT),
        )

    def setup_initial_content(self) -> None:
        self.content.controls.extend(
            [
                ft.Row(
                    [
                        ft.Text(
                            value="Setup",
                            style=ft.TextThemeStyle.HEADLINE_LARGE,
                        ),
                        ft.FilledTonalButton(
                            text="Reset values",
                            icon=ft.icons.UNDO_ROUNDED,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
        )
        self.page.update()

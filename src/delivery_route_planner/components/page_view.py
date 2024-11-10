import flet as ft


class PageView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title = ft.Text(style=ft.TextThemeStyle.HEADLINE_MEDIUM)
        self.action_button = ft.OutlinedButton()
        self.body = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=30,
        )

    def render(self) -> ft.Container:
        header = ft.Row(
            [self.title],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        if self.action_button.icon is not None:
            header.controls.append(self.action_button)

        return ft.Container(
            content=ft.Column(
                [header, self.body],
                expand=True,
                spacing=30,
            ),
            expand=True,
        )

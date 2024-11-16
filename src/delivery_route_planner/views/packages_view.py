import flet as ft


class PackagesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.title = "Packages"
        self.icon = ft.icons.INVENTORY_2_OUTLINED
        self.selected_icon = ft.icons.INVENTORY_2_ROUNDED
        self.disabled = False

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        add_package_button = ft.FilledTonalButton(
            "Add package", ft.icons.INVENTORY_2_OUTLINED,
        )
        header = ft.Container(
            ft.Row(
                [title, add_package_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        return ft.Column([header, body])

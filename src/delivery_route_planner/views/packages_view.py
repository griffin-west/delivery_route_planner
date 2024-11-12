import flet as ft

from delivery_route_planner.components.view_base import ViewBase


class PackagesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = ViewBase(page)
        self.title = "Packages"
        self.icon = ft.icons.INVENTORY_2_OUTLINED
        self.selected_icon = ft.icons.INVENTORY_2_ROUNDED
        self.disabled = False

    def render(self) -> ft.Container:
        self.view.title.value = self.title
        self.view.action_button.text = "Add package"
        self.view.action_button.icon = ft.icons.INVENTORY_2_OUTLINED

        self.view.body.controls = [
            ft.Row(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("First name")),
                            ft.DataColumn(ft.Text("Last name")),
                            ft.DataColumn(ft.Text("Age"), numeric=True),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Griffin")),
                                    ft.DataCell(ft.Text("West")),
                                    ft.DataCell(ft.Text("26")),
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Griffin")),
                                    ft.DataCell(ft.Text("West")),
                                    ft.DataCell(ft.Text("26")),
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Griffin")),
                                    ft.DataCell(ft.Text("West")),
                                    ft.DataCell(ft.Text("26")),
                                ],
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Griffin")),
                                    ft.DataCell(ft.Text("West")),
                                    ft.DataCell(ft.Text("26")),
                                ],
                            ),
                        ],
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        ]

        return self.view.render()

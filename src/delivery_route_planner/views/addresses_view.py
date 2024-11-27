import flet as ft

from delivery_route_planner.models import models


class AddressesView:
    def __init__(self, page: ft.Page, data: models.DataModel) -> None:
        self.page = page
        self.data = data
        self.title = "Addresses"
        self.icon = ft.icons.LOCATION_ON_OUTLINED
        self.selected_icon = ft.icons.LOCATION_ON
        self.disabled = False

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        add_address_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.LOCATION_ON),
            title=ft.Text("Enter address details", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Text("This feature is not yet available."),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(add_address_dialog),
                ),
            ],
        )
        add_address_button = ft.FilledTonalButton(
            "Add address",
            ft.icons.LOCATION_ON_OUTLINED,
            on_click=lambda _: self.page.open(add_address_dialog),
        )
        header = ft.Container(
            ft.Row(
                [title, add_address_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            controls=[self.build_address_table()],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        return ft.Column(
            [header, body],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def build_address_table(self) -> ft.Container:
        address_rows = []
        address_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Name")),
                ft.DataColumn(label=ft.Text("Street")),
                ft.DataColumn(label=ft.Text("City")),
                ft.DataColumn(label=ft.Text("State")),
                ft.DataColumn(label=ft.Text("Zip Code")),
            ],
            rows=address_rows,
            border_radius=15,
            border=ft.border.all(2, ft.colors.OUTLINE_VARIANT),
            vertical_lines=ft.BorderSide(1, ft.colors.OUTLINE_VARIANT),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            show_checkbox_column=True,
        )

        def row_selected(e: ft.ControlEvent) -> None:
            e.control.selected = not e.control.selected
            self.page.update()

        address_rows.extend(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(address.name)),
                    ft.DataCell(ft.Text(address.street)),
                    ft.DataCell(ft.Text(address.city)),
                    ft.DataCell(ft.Text(address.state)),
                    ft.DataCell(ft.Text(address.zip_code)),
                ],
                on_select_changed=row_selected,
                selected=True,
            )
            for address in self.data.addresses.values()
        )
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [address_table, ft.Container(width=30)],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    ft.Text(
                        "*Work in progress. Row selection currently has no effect.",
                    ),
                ],
            ),
            padding=ft.padding.only(30, 0, 0, 30),
        )

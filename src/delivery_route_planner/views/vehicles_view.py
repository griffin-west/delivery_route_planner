import flet as ft

from delivery_route_planner.models import models


class VehiclesView:
    def __init__(self, page: ft.Page, data: models.DataModel) -> None:
        self.page = page
        self.data = data

        self.title = "Vehicles"
        self.icon = ft.icons.LOCAL_SHIPPING_OUTLINED
        self.selected_icon = ft.icons.LOCAL_SHIPPING_ROUNDED
        self.disabled = False

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        add_vehicle_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.LOCAL_SHIPPING_ROUNDED),
            title=ft.Text("Enter vehicle details", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                [
                    ft.TextField(
                        label="Vehicle ID",
                        icon=ft.icons.NUMBERS_ROUNDED,
                        value="3",
                        disabled=True,
                    ),
                    ft.TextField(
                        label="Speed (mph)",
                        icon=ft.icons.SPEED_ROUNDED,
                        value="18",
                        disabled=True,
                    ),
                    ft.TextField(
                        label="Package capacity",
                        icon=ft.icons.SCALE_ROUNDED,
                        value="16",
                        disabled=True,
                    ),
                    ft.Text("This feature is not yet available."),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(add_vehicle_dialog),
                ),
                ft.FilledTonalButton(
                    "Create",
                    on_click=lambda _: self.page.close(add_vehicle_dialog),
                    disabled=True,
                ),
            ],
        )
        add_vehicle_button = ft.FilledTonalButton(
            "Add vehicle",
            ft.icons.LOCAL_SHIPPING_OUTLINED,
            on_click=lambda _: self.page.open(add_vehicle_dialog),
        )
        header = ft.Container(
            ft.Row(
                [title, add_vehicle_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            controls=[
                self.create_vehicle_table(),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        return ft.Column(
            [
                header,
                body,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def create_vehicle_table(self) -> ft.Container:

        vehicle_rows = []
        vehicle_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Vehicle ID"), numeric=True),
                ft.DataColumn(label=ft.Text("Speed (mph)"), numeric=True),
                ft.DataColumn(label=ft.Text("Package capacity"), numeric=True),
            ],
            rows=vehicle_rows,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            border_radius=15,
            border=ft.border.all(2, ft.colors.OUTLINE_VARIANT),
            vertical_lines=ft.BorderSide(1, ft.colors.OUTLINE_VARIANT),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            show_checkbox_column=True,
        )
        vehicle_rows.extend(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(vehicle.id))),
                    ft.DataCell(ft.Text(str(round(vehicle.speed_mph, 1)))),
                    ft.DataCell(ft.Text(str(vehicle.package_capacity))),
                ],
                on_select_changed=lambda _: _,
                selected=True,
            )
            for vehicle in self.data.vehicles.values()
        )

        return ft.Container(
            content=vehicle_table,
            padding=ft.padding.only(30, 0, 30, 30),
        )
import flet as ft

from delivery_route_planner.models import models


class VehiclesView:
    def __init__(
        self,
        page: ft.Page,
        view_pane: ft.Card,
        data: models.DataModel,
    ) -> None:
        self.page = page
        self.view_pane = view_pane
        self.data = data

        self.title = "Vehicles"
        self.icon = ft.icons.LOCAL_SHIPPING_OUTLINED
        self.selected_icon = ft.icons.LOCAL_SHIPPING_ROUNDED
        self.disabled = False

        self.new_vehicle_speed = 18.0
        self.new_vehicle_capacity = 16
        self.new_vehicle_dialog = self.create_new_vehicle_dialog()

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        add_vehicle_button = ft.FilledTonalButton(
            "Add vehicle",
            ft.icons.LOCAL_SHIPPING_OUTLINED,
            on_click=lambda _: self.page.open(self.new_vehicle_dialog),
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

    def create_new_vehicle_dialog(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            icon=ft.Icon(ft.icons.LOCAL_SHIPPING_ROUNDED),
            title=ft.Text("Enter vehicle details", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                [
                    ft.TextField(
                        label="Speed (mph)",
                        icon=ft.icons.SPEED_ROUNDED,
                        value=str(self.new_vehicle_speed),
                        on_change=self.validate_speed_input,
                    ),
                    ft.TextField(
                        label="Package capacity",
                        icon=ft.icons.SCALE_ROUNDED,
                        value=str(self.new_vehicle_capacity),
                        on_change=self.validate_capacity_input,
                    ),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(self.new_vehicle_dialog),
                ),
                ft.FilledTonalButton(
                    "Create",
                    on_click=self.create_vehicle,
                ),
            ],
        )

    def validate_speed_input(self, e: ft.ControlEvent) -> None:
        try:
            self.new_vehicle_speed = float(e.control.value.strip())
            e.control.error_text = None
        except ValueError:
            e.control.error_text = "Enter a number."
        self.page.update()

    def validate_capacity_input(self, e: ft.ControlEvent) -> None:
        try:
            self.new_vehicle_capacity = int(e.control.value.strip())
            e.control.error_text = None
        except ValueError:
            e.control.error_text = "Enter a whole number."
        self.page.update()

    def create_vehicle(self, _e: ft.ControlEvent) -> None:
        self.page.close(self.new_vehicle_dialog)
        new_vehicle_id = models.Vehicle.find_max_vehicle_id(self.data.vehicles) + 1
        models.Vehicle.add_to_fleet(
            self.data,
            new_vehicle_id,
            self.new_vehicle_speed,
            self.new_vehicle_capacity,
        )
        self.view_pane.content = self.render()
        self.page.update()

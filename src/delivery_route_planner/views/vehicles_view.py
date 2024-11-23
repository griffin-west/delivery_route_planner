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
            content=ft.Text("This feature is not yet available."),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(add_vehicle_dialog),
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
            controls=[self.create_vehicle_table()],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        return ft.Column(
            [header, body],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def create_vehicle_table(self) -> ft.Container:

        vehicle_rows = []
        vehicle_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Vehicle ID"), numeric=True),
                ft.DataColumn(label=ft.Text("Speed (mph)")),
                ft.DataColumn(label=ft.Text("Package capacity")),
            ],
            rows=vehicle_rows,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            border_radius=15,
            border=ft.border.all(2, ft.colors.OUTLINE_VARIANT),
            vertical_lines=ft.BorderSide(1, ft.colors.OUTLINE_VARIANT),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            show_checkbox_column=True,
        )

        def row_selected(e: ft.ControlEvent) -> None:
            e.control.selected = not e.control.selected
            self.page.update()

        vehicle_rows.extend(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(vehicle.id))),
                    ft.DataCell(
                        content=ft.Text(str(round(vehicle.speed_mph, 1))),
                        show_edit_icon=True,
                        on_tap=self.speed_cell_selected,
                        data=vehicle.id,
                    ),
                    ft.DataCell(
                        content=ft.Text(str(vehicle.package_capacity)),
                        show_edit_icon=True,
                        on_tap=self.capacity_cell_selected,
                        data=vehicle.id,
                    ),
                ],
                on_select_changed=row_selected,
                selected=True,
            )
            for vehicle in self.data.vehicles.values()
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [vehicle_table, ft.Container(width=30)],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    ft.Text(
                        "*Work in progress. Row selection currently has no effect.",
                    ),
                ],
            ),
            padding=ft.padding.only(30, 0, 0, 30),
        )

    def speed_cell_selected(self, e: ft.ControlEvent) -> None:

        def save_new_speed(_e: ft.ControlEvent) -> None:
            if entry.value is None:
                return
            new_speed = float(entry.value.strip())
            vehicle = self.data.vehicles[e.control.data]
            e.control.content.value = new_speed
            vehicle.speed_mph = new_speed
            vehicle.duration_map = models.TravelCostMap.with_duration(
                self.data.addresses, new_speed,
            )
            self.page.close(edit_speed_dialog)
            self.page.update()

        def validate_speed_input(e: ft.ControlEvent) -> None:
            try:
                float(e.control.value.strip())
                e.control.error_text = None
                edit_speed_dialog.actions[1].disabled = False
            except ValueError:
                e.control.error_text = "Enter a number."
                edit_speed_dialog.actions[1].disabled = True
            self.page.update()

        entry = ft.TextField(
            value=e.control.content.value,
            label="Vehicle speed (mph)",
            on_change=validate_speed_input,
        )
        edit_speed_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.SPEED_ROUNDED),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                [
                    entry,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    text="Cancel",
                    on_click=lambda _: self.page.close(edit_speed_dialog),
                ),
                ft.FilledTonalButton(
                    text="Save",
                    on_click=save_new_speed,
                ),
            ],
        )
        self.page.open(edit_speed_dialog)

    def capacity_cell_selected(self, e: ft.ControlEvent) -> None:

        def save_new_capacity(_e: ft.ControlEvent) -> None:
            if entry.value is None:
                return
            new_capacity = int(entry.value.strip())
            vehicle = self.data.vehicles[e.control.data]
            e.control.content.value = new_capacity
            vehicle.package_capacity = new_capacity
            self.page.close(edit_capacity_dialog)
            self.page.update()

        def validate_capacity_input(e: ft.ControlEvent) -> None:
            try:
                int(e.control.value.strip())
                e.control.error_text = None
                edit_capacity_dialog.actions[1].disabled = False
            except ValueError:
                e.control.error_text = "Enter a number."
                edit_capacity_dialog.actions[1].disabled = True
            self.page.update()

        entry = ft.TextField(
            value=e.control.content.value,
            label="Package capacity",
            on_change=validate_capacity_input,
        )
        edit_capacity_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.SCALE_ROUNDED),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                [entry],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    text="Cancel",
                    on_click=lambda _: self.page.close(edit_capacity_dialog),
                ),
                ft.FilledTonalButton(
                    text="Save",
                    on_click=save_new_capacity,
                ),
            ],
        )
        self.page.open(edit_capacity_dialog)

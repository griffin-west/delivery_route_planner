from typing import Callable

import flet as ft

from delivery_route_planner.models import models

RESERVED_VEHICLE_IDS = 2

class VehiclesView:
    def __init__(
        self,
        page: ft.Page,
        data: models.DataModel,
        navigation_callback: Callable,
    ) -> None:
        self.page = page
        self.data = data
        self.rerender = navigation_callback
        self.title = "Vehicles"
        self.icon = ft.icons.LOCAL_SHIPPING_OUTLINED
        self.selected_icon = ft.icons.LOCAL_SHIPPING_ROUNDED
        self.disabled = False
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
                ft.DataColumn(label=ft.Text("Delete")),
            ],
            rows=vehicle_rows,
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
                        data=vehicle,
                    ),
                    ft.DataCell(
                        content=ft.Text(str(vehicle.package_capacity)),
                        show_edit_icon=True,
                        on_tap=self.capacity_cell_selected,
                        data=vehicle,
                    ),
                    ft.DataCell(
                        content=ft.Icon(
                            ft.icons.DELETE_OUTLINE_ROUNDED,
                            color=(
                                ft.colors.PRIMARY
                                if vehicle.id > RESERVED_VEHICLE_IDS
                                else ft.colors.OUTLINE_VARIANT
                            ),
                        ),
                        on_tap=self.delete_cell_selected,
                        data=vehicle,
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

    def delete_cell_selected(self, e: ft.ControlEvent) -> None:

        def delete_vehicle(_e: ft.ControlEvent) -> None:
            self.data.vehicles.pop(vehicle_id_to_remove)
            rebuilt_vehicle_dict = {}
            for key, vehicle in self.data.vehicles.items():
                if vehicle.id > vehicle_id_to_remove:
                    vehicle.id -= 1
                    rebuilt_vehicle_dict[key - 1] = vehicle
                else:
                    rebuilt_vehicle_dict[key] = vehicle
            self.data.vehicles = rebuilt_vehicle_dict
            self.page.close(delete_vehicle_dialog)
            self.rerender("vehicles")
            self.page.update()

        delete_vehicle_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.DELETE_FOREVER_ROUNDED),
            actions_alignment=ft.MainAxisAlignment.END,
            title=ft.Text("Are you sure?"),
            content=ft.Column(
                [
                    ft.Text(f"Vehicle {e.control.data.id} will be deleted."),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    text="Cancel",
                    on_click=lambda _: self.page.close(delete_vehicle_dialog),
                ),
                ft.FilledTonalButton(
                    text="Delete",
                    on_click=delete_vehicle,
                ),
            ],
        )
        vehicle_id_to_remove = e.control.data.id
        if vehicle_id_to_remove > RESERVED_VEHICLE_IDS:
            self.page.open(delete_vehicle_dialog)

    def speed_cell_selected(self, e: ft.ControlEvent) -> None:

        def save_new_speed(_e: ft.ControlEvent) -> None:
            if entry.value is None or not self.is_speed_valid(entry.value.strip()):
                return
            new_speed = float(entry.value.strip())
            vehicle = e.control.data
            e.control.content.value = new_speed
            vehicle.speed_mph = new_speed
            vehicle.duration_map = models.TravelCostMap.with_duration(
                self.data.addresses, new_speed,
            )
            self.page.close(edit_speed_dialog)
            self.page.update()

        entry = ft.TextField(
            value=e.control.content.value,
            label="Vehicle speed (mph)",
            on_change=self.validate_speed_input,
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
            if entry.value is None or not self.is_capacity_valid(entry.value.strip()):
                return
            new_capacity = int(entry.value.strip())
            vehicle = e.control.data
            e.control.content.value = new_capacity
            vehicle.package_capacity = new_capacity
            self.page.close(edit_capacity_dialog)
            self.page.update()

        entry = ft.TextField(
            value=e.control.content.value,
            label="Package capacity",
            on_change=self.validate_capacity_input,
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

    def is_speed_valid(self, value: str) -> bool:
        try:
            self.new_vehicle_speed = float(value)
        except ValueError:
            return False
        else:
            return True

    def is_capacity_valid(self, value: str) -> bool:
        try:
            self.new_vehicle_speed = int(value)
        except ValueError:
            return False
        else:
            return True

    def validate_speed_input(self, e: ft.ControlEvent) -> None:
        if self.is_speed_valid(e.control.value.strip()):
            e.control.error_text = None
        else:
            e.control.error_text = "Enter a number."
        self.page.update()

    def validate_capacity_input(self, e: ft.ControlEvent) -> None:
        if self.is_capacity_valid(e.control.value.strip()):
            e.control.error_text = None
        else:
            e.control.error_text = "Enter a whole number."
        self.page.update()

    def create_new_vehicle_dialog(self) -> ft.AlertDialog:

        def create_vehicle(_e: ft.ControlEvent) -> None:
            if (
                speed_entry.value is None
                or not self.is_speed_valid(speed_entry.value.strip())
                or capacity_entry.value is None
                or not self.is_capacity_valid(capacity_entry.value.strip())
            ):
                return
            next_id = models.Vehicle.find_max_vehicle_id(self.data.vehicles) + 1
            models.Vehicle.add_to_fleet(
                vehicles=self.data.vehicles,
                addresses=self.data.addresses,
                vehicle_id=next_id,
                speed_mph=float(speed_entry.value.strip()),
                package_capacity=int(capacity_entry.value.strip()),
            )
            self.page.close(self.new_vehicle_dialog)
            self.rerender("vehicles")
            self.page.update()

        speed_entry = ft.TextField(
            label="Speed (mph)",
            icon=ft.icons.SPEED_ROUNDED,
            value="18.0",
            on_change=self.validate_speed_input,
        )

        capacity_entry = ft.TextField(
            label="Package capacity",
            icon=ft.icons.SCALE_ROUNDED,
            value="16",
            on_change=self.validate_capacity_input,
        )

        return ft.AlertDialog(
            icon=ft.Icon(ft.icons.LOCAL_SHIPPING_ROUNDED),
            title=ft.Text("Enter vehicle details", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                [
                    speed_entry,
                    capacity_entry,
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
                    on_click=create_vehicle,
                ),
            ],
        )

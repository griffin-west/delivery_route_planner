import flet as ft

from delivery_route_planner.models import models


class PackagesView:
    def __init__(self, page: ft.Page, data: models.DataModel) -> None:
        self.page = page
        self.data = data
        self.title = "Packages"
        self.icon = ft.icons.INVENTORY_2_OUTLINED
        self.selected_icon = ft.icons.INVENTORY_2_ROUNDED
        self.disabled = False

    def render(self) -> ft.Column:
        if self.page.theme:
            self.page.theme.color_scheme_seed = ft.colors.ORANGE
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        add_package_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.INVENTORY_2_ROUNDED),
            title=ft.Text("Enter package details", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Text("This feature is not yet available."),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(add_package_dialog),
                ),
            ],
        )
        add_package_button = ft.FilledTonalButton(
            "Add package",
            ft.icons.INVENTORY_2_OUTLINED,
            on_click=lambda _: self.page.open(add_package_dialog),
        )
        header = ft.Container(
            ft.Row(
                [title, add_package_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            controls=[self.create_package_table()],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        return ft.Column(
            [header, body],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def create_package_table(self) -> ft.Container:

        package_rows = []
        package_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Package ID"), numeric=True),
                ft.DataColumn(label=ft.Text("Address")),
                ft.DataColumn(label=ft.Text("Weight (kg)"), numeric=True),
                ft.DataColumn(label=ft.Text("Availability")),
                ft.DataColumn(label=ft.Text("Deadline")),
                ft.DataColumn(label=ft.Text("Vehicle ID"), numeric=True),
                ft.DataColumn(label=ft.Text("Linked packages")),
            ],
            rows=package_rows,
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

        for package in self.data.packages.values():
            vehicle_requirement = (
                package.vehicle_requirement.id if package.vehicle_requirement else None
            )
            bundled_packages = (
                [bundled_package.id for bundled_package in package.bundled_packages]
                if len(package.bundled_packages) > 0
                else None
            )
            package_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(package.id))),
                        ft.DataCell(ft.Text(package.address.street)),
                        ft.DataCell(ft.Text(str(package.weight_kg))),
                        ft.DataCell(
                            ft.Text(str(package.shipping_availability)),
                            placeholder=package.shipping_availability is None,
                        ),
                        ft.DataCell(
                            ft.Text(str(package.delivery_deadline)),
                            placeholder=package.delivery_deadline is None,
                        ),
                        ft.DataCell(
                            ft.Text(str(vehicle_requirement)),
                            placeholder=vehicle_requirement is None,
                        ),
                        ft.DataCell(
                            ft.Text(str(bundled_packages)),
                            placeholder=bundled_packages is None,
                        ),
                    ],
                    on_select_changed=row_selected,
                    selected=True,
                ),
            )

        return ft.Container(
            content=ft.Column(
                [
                    package_table,
                    ft.Text(
                        "*Work in progress. Row selection currently has no effect.",
                    ),
                ],
            ),
            padding=ft.padding.only(30, 0, 30, 30),
        )

import flet as ft

from delivery_route_planner.models import models


class ValidationView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.solution = None
        self.title = "Validation"
        self.icon = ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED
        self.selected_icon = ft.icons.CHECK_CIRCLE_ROUNDED
        self.disabled = True

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        save_as_file_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.SAVE_AS_ROUNDED),
            title=ft.Text("Save as file", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Text("This feature is not yet available."),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: self.page.close(save_as_file_dialog),
                ),
            ],
        )
        save_as_file_button = ft.FilledTonalButton(
            "Save as file",
            ft.icons.SAVE_AS_OUTLINED,
            on_click=lambda _: self.page.open(save_as_file_dialog),
        )
        header = ft.Container(
            ft.Row(
                [title, save_as_file_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            controls=[self._build_validation_table()],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        return ft.Column(
            [header, body],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def set_solution(self, solution: models.Solution) -> None:
        self.solution = solution

    def _build_validation_table(self) -> ft.Container:
        if not self.solution:
            return ft.Container()

        package_rows = []
        package_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Package ID"), numeric=True),
                ft.DataColumn(label=ft.Text("Status")),
                ft.DataColumn(label=ft.Text("Availability")),
                ft.DataColumn(label=ft.Text("Shipped")),
                ft.DataColumn(label=ft.Text("Deadline")),
                ft.DataColumn(label=ft.Text("Delivered")),
                ft.DataColumn(label=ft.Text("Vehicle ID Required"), numeric=True),
                ft.DataColumn(label=ft.Text("Vehicle ID Used"), numeric=True),
                ft.DataColumn(label=ft.Text("Linked packages")),
            ],
            rows=package_rows,
            border_radius=15,
            border=ft.border.all(2, ft.colors.OUTLINE_VARIANT),
            vertical_lines=ft.BorderSide(1, ft.colors.OUTLINE_VARIANT),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        for package in self.solution.data.packages.values():
            vehicle_requirement = (
                package.vehicle_requirement.id if package.vehicle_requirement else None
            )
            bundled_packages = (
                [bundled_package.id for bundled_package in package.bundled_packages]
                if len(package.bundled_packages) > 0
                else None
            )
            vehicle_used = package.vehicle_used.id if package.vehicle_used else None
            if package.delivered_time:
                status = "Delivered"
                status_color = ft.colors.PRIMARY
            else:
                status = "Missed"
                status_color = ft.colors.ERROR
            package_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(package.id))),
                        ft.DataCell(
                            ft.Text(
                                status,
                                color=status_color,
                                font_family="Outfit-Bold",
                            ),
                        ),
                        ft.DataCell(
                            ft.Text(str(package.shipping_availability)),
                            placeholder=package.shipping_availability is None,
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(package.shipped_time),
                                font_family=(
                                    "Outfit-Bold"
                                    if package.shipping_availability
                                    else None
                                ),
                                color=(
                                    status_color
                                    if package.shipping_availability
                                    else None
                                ),
                            ),
                            placeholder=package.shipping_availability is None,
                        ),
                        ft.DataCell(
                            ft.Text(str(package.delivery_deadline)),
                            placeholder=package.delivery_deadline is None,
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(package.delivered_time),
                                font_family=(
                                    "Outfit-Bold" if package.delivery_deadline else None
                                ),
                                color=(
                                    status_color if package.delivery_deadline else None
                                ),
                            ),
                            placeholder=package.delivery_deadline is None,
                        ),
                        ft.DataCell(
                            ft.Text(str(vehicle_requirement)),
                            placeholder=vehicle_requirement is None,
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(vehicle_used),
                                font_family=(
                                    "Outfit-Bold" if vehicle_requirement else None
                                ),
                                color=status_color if vehicle_requirement else None,
                            ),
                            placeholder=vehicle_requirement is None,
                        ),
                        ft.DataCell(
                            ft.Text(str(bundled_packages)),
                            placeholder=bundled_packages is None,
                        ),
                    ],
                    selected=package.delivered_time is not None,
                ),
            )

        return ft.Container(
            content=ft.Row(
                [package_table, ft.Container(width=30)],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.only(30, 0, 0, 30),
        )

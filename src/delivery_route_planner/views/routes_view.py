import flet as ft

from delivery_route_planner.models import models


class RoutesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.solution = None
        self.title = "Routes"
        self.icon = ft.icons.ROUTE_OUTLINED
        self.selected_icon = ft.icons.ROUTE_ROUNDED
        self.disabled = True

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        save_as_file_dialog = ft.AlertDialog(
            icon=ft.Icon(ft.icons.SAVE_AS_ROUNDED),
            title=ft.Text("Save routes as file", text_align=ft.TextAlign.CENTER),
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
            controls=[self._build_route_tables()],
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

    def _build_route_tables(self) -> ft.Container:
        if not self.solution:
            return ft.Container()

        route_tables = ft.Column()
        for route in self.solution.routes:
            route_steps = []
            route_table = ft.DataTable(
                columns=[
                    ft.DataColumn(label=ft.Text("Step"), numeric=True),
                    ft.DataColumn(label=ft.Text("Address")),
                    ft.DataColumn(label=ft.Text("Activity")),
                    ft.DataColumn(label=ft.Text("Package ID(s)")),
                    ft.DataColumn(label=ft.Text("Load"), numeric=True),
                    ft.DataColumn(label=ft.Text("Mileage"), numeric=True),
                    ft.DataColumn(label=ft.Text("Time")),
                ],
                rows=route_steps,
                heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                border_radius=15,
                border=ft.border.all(2, ft.colors.OUTLINE_VARIANT),
                vertical_lines=ft.BorderSide(1, ft.colors.OUTLINE_VARIANT),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            )

            step = 1
            packages = []
            for this_stop, next_stop in zip(route.stops[1:], route.stops[2:] + [None]):
                if this_stop.node.package:
                    packages.append(this_stop.node.package.id)
                if (
                    next_stop
                    and this_stop.node.kind == next_stop.node.kind
                    and this_stop.node.address == next_stop.node.address
                ):
                    continue
                activity = (
                    this_stop.node.kind.description
                    if this_stop.node.kind != models.NodeKind.ORIGIN
                    else "End"
                )
                packages_str = str(packages)[1:-1]
                if len(packages_str) == 0:
                    packages_str = "None"
                route_steps.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(step))),
                            ft.DataCell(ft.Text(this_stop.node.address)),
                            ft.DataCell(ft.Text(activity)),
                            ft.DataCell(
                                ft.Text(packages_str),
                                placeholder=packages_str == "None",
                            ),
                            ft.DataCell(ft.Text(str(this_stop.vehicle_load))),
                            ft.DataCell(ft.Text(str(round(this_stop.mileage, 2)))),
                            ft.DataCell(ft.Text(str(this_stop.visit_time))),
                        ],
                        selected=this_stop.node.kind != models.NodeKind.DELIVERY,
                    ),
                )
                step = step + 1
                packages.clear()

            unused_vehicle_message = ft.Card(
                ft.Container(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.INFO_ROUNDED),
                        title=ft.Text("This is not an error."),
                        subtitle=ft.Text(
                            "It is possible for the algorithm to optimize "
                            "total mileage by utilizing only one vehicle.",
                        ),
                        content_padding=0,
                    ),
                    padding=ft.padding.symmetric(0, 20),
                ),
                variant=ft.CardVariant.FILLED,
                width=650,
                visible=route.mileage == 0,
            )

            route_tables.controls.extend(
                [
                    ft.Text(
                        f"Route for Vehicle {route.vehicle.id}",
                        style=ft.TextThemeStyle.TITLE_MEDIUM,
                    ),
                    route_table,
                    unused_vehicle_message,
                    ft.Container(height=30),
                ],
            )

        total_mileage_card = ft.Card(
            ft.Container(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SPEED_ROUNDED),
                    title=ft.Text("Total mileage"),
                    subtitle=ft.Column(
                        [
                            ft.Text(
                                f"Vehicle {route.vehicle.id}: "
                                f"{round(route.mileage, 1)} miles",
                            )
                            for route in self.solution.routes
                        ],
                        spacing=0,
                    ),
                    trailing=ft.Text(
                        f"{round(self.solution.mileage, 1)} miles",
                        style=ft.TextThemeStyle.TITLE_LARGE,
                    ),
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

        delivered_count = self.solution.delivered_packages_count
        missed_count = self.solution.missed_packages_count
        missed_packages = str(self.solution.missed_packages)[1:-1]

        delivery_success_card = ft.Card(
            ft.Container(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.INVENTORY_2_OUTLINED),
                    title=ft.Text("Delivery success"),
                    subtitle=ft.Column(
                        [
                            ft.Text(f"Packages delivered: {delivered_count}"),
                            ft.Text(f"Packages missed: {missed_count}"),
                            ft.Text(
                                f"Missed packages: {missed_packages}",
                                visible=missed_count > 0,
                            ),
                        ],
                        spacing=0,
                    ),
                    trailing=ft.Text(
                        self.solution.delivery_percentage,
                        style=ft.TextThemeStyle.TITLE_LARGE,
                    ),
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

        card_row = ft.Container(
            ft.Row(
                [
                    total_mileage_card,
                    delivery_success_card,
                ],
                wrap=True,
                spacing=30,
                run_spacing=30,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )

        return ft.Container(
            content=ft.Column(
                [
                    card_row,
                    route_tables,
                ],
                spacing=30,
            ),
            padding=ft.padding.symmetric(0, 30),
        )

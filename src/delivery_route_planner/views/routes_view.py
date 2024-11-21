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
        route_tables = []
        
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

            step = 0
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
                route_steps.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(step))),
                            ft.DataCell(ft.Text(this_stop.node.address)),
                            ft.DataCell(ft.Text(activity)),
                            ft.DataCell(ft.Text(str(packages)[1:-1])),
                            ft.DataCell(ft.Text(str(this_stop.vehicle_load))),
                            ft.DataCell(ft.Text(str(round(this_stop.mileage, 1)))),
                            ft.DataCell(ft.Text(str(this_stop.visit_time))),
                        ],
                        selected=this_stop.node.kind != models.NodeKind.DELIVERY,
                    ),
                )
                step = step + 1
                packages.clear()

            route_tables.extend(
                [
                    ft.Text(
                        f"Route for Vehicle {route.vehicle.id}",
                        style=ft.TextThemeStyle.TITLE_LARGE,
                    ),
                    route_table,
                    ft.Container(height=30),
                ],
            )
        return ft.Container(
            content=ft.Column(route_tables),
            padding=ft.padding.symmetric(0, 30),
        )

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
        header = ft.Container(title, padding=30)
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
        route_stops = []
        route_table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Vehicle ID")),
                ft.DataColumn(label=ft.Text("Route Stop")),
                ft.DataColumn(label=ft.Text("State")),
                ft.DataColumn(label=ft.Text("Zip Code")),
            ],
            rows=route_stops,
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

        address_rows.extend(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(address.street),
                        placeholder=address.street == "Depot",
                    ),
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
                    address_table,
                    ft.Text(
                        "*Work in progress. Row selection currently has no effect.",
                    ),
                ],
            ),
            padding=ft.padding.only(30, 0, 30, 30),
        )


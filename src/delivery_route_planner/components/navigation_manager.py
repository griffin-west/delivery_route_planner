import flet as ft


class NavigationManager:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.views = {}
        self.view_names = []
        self.destinations = []
        self.navigation_rail = ft.NavigationRail()
        self.view_container = ft.Container(
            margin=ft.margin.only(0, 0, 24, 24),
            bgcolor=ft.colors.SURFACE,
            border_radius=15,
            border=ft.border.all(1, ft.colors.SURFACE_VARIANT),
            expand=True,
        )

    def render(self) -> ft.Row:
        return ft.Row(
            controls=[self.navigation_rail, self.view_container],
            expand=True,
            spacing=0,
        )

    def set_views(self, views: dict) -> None:
        self.views = views
        self.view_names = list(views.keys())
        self.view_container.content = self.views["setup"].render()
        self.navigation_rail = self._build_navigation_rail(views)

    def navigate_from_view_name(self, view_name: str) -> None:
        if view_name in self.views:
            self.view_container.content = self.views[view_name].render()
            self.page.update()

    def _navigate_from_selection(self, e: ft.ControlEvent) -> None:
        selected_view_name = self.view_names[e.control.selected_index]
        self.view_container.content = self.views[selected_view_name].render()
        self.page.update()

    def _build_navigation_rail(self, views: dict) -> ft.NavigationRail:
        solve_button = ft.FloatingActionButton(
            icon=ft.icons.AUTO_AWESOME_ROUNDED,
            bgcolor=ft.colors.PRIMARY,
            foreground_color=ft.colors.ON_PRIMARY,
            elevation=2,
            hover_elevation=4,
        )
        solve_button_container = ft.Container(
            ft.Column(
                controls=[solve_button, ft.Text("Solve")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
        destinations = [
            ft.NavigationRailDestination(
                label=view.title,
                icon=view.icon,
                selected_icon=view.selected_icon,
                disabled=view.disabled,
            )
            for view in views.values()
        ]
        return ft.NavigationRail(
            leading=solve_button_container,
            destinations=destinations,
            selected_index=0,
            group_alignment=-0.2,
            label_type=ft.NavigationRailLabelType.SELECTED,
            indicator_color=ft.colors.INVERSE_PRIMARY,
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self._navigate_from_selection,
        )

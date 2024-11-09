import flet as ft


class NavigationPane:
    def __init__(self, page: ft.Page) -> None:
        self.page = page

    def render(self) -> ft.Column:
        navigation_rail = ft.NavigationRail(
            destinations=[
                ft.NavigationRailDestination(
                    label="Setup",
                    icon=ft.icons.EDIT_OUTLINED,
                    selected_icon=ft.icons.EDIT_ROUNDED,
                ),
                ft.NavigationRailDestination(
                    label="Packages",
                    icon=ft.icons.INVENTORY_2_OUTLINED,
                    selected_icon=ft.icons.INVENTORY_2_ROUNDED,
                ),
                ft.NavigationRailDestination(
                    label="Vehicles",
                    icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
                    selected_icon=ft.icons.LOCAL_SHIPPING_ROUNDED,
                ),
                ft.NavigationRailDestination(
                    label="Addresses",
                    icon=ft.icons.LOCATION_ON_OUTLINED,
                    selected_icon=ft.icons.LOCATION_ON,
                ),
                ft.NavigationRailDestination(
                    label="Routes",
                    icon=ft.icons.ROUTE_OUTLINED,
                    selected_icon=ft.icons.ROUTE_ROUNDED,
                    disabled=True,
                ),
                ft.NavigationRailDestination(
                    label="Reports",
                    icon=ft.icons.INSERT_CHART_OUTLINED_ROUNDED,
                    selected_icon=ft.icons.INSERT_CHART_ROUNDED,
                    disabled=True,
                ),
            ],
            expand=True,
            extended=True,
            selected_index=0,
            group_alignment=0,
            min_extended_width=170,
            bgcolor=ft.colors.TRANSPARENT,
            label_type=ft.NavigationRailLabelType.NONE,
            leading=ft.Container(
                ft.FloatingActionButton(
                    text="Solve",
                    icon=ft.icons.AUTO_AWESOME_ROUNDED,
                    bgcolor=ft.colors.INVERSE_PRIMARY,
                    width=120,
                    elevation=1,
                    hover_elevation=4,
                ),
                padding=ft.padding.symmetric(20, 0),
            ),
        )

        dark_mode_button = ft.IconButton(
            icon=ft.icons.DARK_MODE_ROUNDED,
            on_click=self._toggle_dark_mode,
        )

        color_button = ft.IconButton(
            icon=ft.icons.COLOR_LENS_ROUNDED,
            on_click=self._randomize_colors,
        )

        return ft.Column(
            [
                navigation_rail,
                ft.Row([dark_mode_button, color_button]),
                ft.Container(height=10),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _toggle_dark_mode(self, e: ft.ControlEvent) -> None:
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.DARK_MODE_ROUNDED
        self.page.update()

    def _randomize_colors(self, e: ft.ControlEvent) -> None:
        _ = e
        if self.page.theme is None:
            self.page.theme = ft.Theme()
        self.page.theme.color_scheme_seed = ft.colors.random_color()
        self.page.update()

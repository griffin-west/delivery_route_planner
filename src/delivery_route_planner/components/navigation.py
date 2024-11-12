from __future__ import annotations

import flet as ft


class Navigation:
    def __init__(self, page: ft.Page, views):
        self.page = page
        self.views = views

    def render(self) -> ft.Row:
        navigation_pane = self.create_navigation_pane(self.views)
        view_pane = self.create_view_pane()

        return ft.Row(
            [
                navigation_pane,
                view_pane,
            ],
            spacing=0,
            expand=True,
        )

    def create_navigation_pane(self, views) -> ft.Container:
        destinations = [
            ft.NavigationRailDestination(
                label_content=ft.Text(view.title, size=14),
                icon=view.icon,
                selected_icon=view.selected_icon,
                disabled=view.disabled,
            )
            for view in views
        ]
        floating_action_button = ft.Container(
            ft.FloatingActionButton(
                text="  Solve",
                icon=ft.icons.AUTO_AWESOME_ROUNDED,
                bgcolor=ft.colors.TERTIARY_CONTAINER,
                foreground_color=ft.colors.ON_TERTIARY_CONTAINER,
                elevation=2,
                hover_elevation=4,
                width=130,
            ),
            padding=ft.padding.symmetric(20, 0),
        )
        navigation_rail = ft.NavigationRail(
            destinations=destinations,
            extended=True,
            expand=True,
            selected_index=0,
            group_alignment=-0.8,
            min_extended_width=170,
            indicator_color=ft.colors.INVERSE_PRIMARY,
            bgcolor=ft.colors.TRANSPARENT,
            leading=floating_action_button,
            on_change=self.change_view,
        )
        dark_mode_button = ft.IconButton(
            icon=(
                ft.icons.DARK_MODE_OUTLINED
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else ft.icons.LIGHT_MODE_OUTLINED
            ),
            on_click=self._toggle_dark_mode,
            icon_color=ft.colors.ON_SURFACE,
        )
        color_button = ft.IconButton(
            icon=ft.icons.COLOR_LENS_OUTLINED,
            on_click=self._randomize_colors,
            icon_color=ft.colors.ON_SURFACE,
        )

        return ft.Container(
            ft.Column(
                [
                    navigation_rail,
                    ft.Row([dark_mode_button, color_button]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(20, 0),
        )

    def create_view_pane(self) -> ft.Container:
        self.content_switcher = ft.AnimatedSwitcher(
            content=self.views[0].render(),
            duration=300,
            reverse_duration=300,
            transition=ft.AnimatedSwitcherTransition.FADE,
            expand=True,
        )

        return ft.Container(
            content=self.content_switcher,
            expand=True,
            border_radius=20,
            bgcolor=ft.colors.SURFACE,
            margin=ft.margin.only(0, 0, 24, 24),
            padding=ft.padding.only(30, 30, 30, 0),
            border=ft.border.all(1, ft.colors.SURFACE_VARIANT),
            theme=ft.Theme(
                scrollbar_theme=ft.ScrollbarTheme(
                    main_axis_margin=15,
                    cross_axis_margin=-20,
                ),
            ),
        )

    def change_view(self, e: ft.ControlEvent) -> None:
        self.content_switcher.content = self.views[e.control.selected_index].render()
        self.page.update()

    def _toggle_dark_mode(self, e: ft.ControlEvent) -> None:
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.LIGHT_MODE_OUTLINED
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.DARK_MODE_OUTLINED
        self.page.update()

    def _randomize_colors(self, e: ft.ControlEvent) -> None:
        _ = e
        new_color = ft.colors.random_color()
        self.page.theme.color_scheme_seed = new_color
        self.page.dark_theme.color_scheme_seed = new_color
        self.page.update()

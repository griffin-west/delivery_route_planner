from typing import Callable

import flet as ft
from page_view import PageView


class NavigationPane(ft.Column):
    def __init__(
        self,
        page_views: list[PageView],
        page_switcher_callback: Callable[[ft.ControlEvent], None],
        color_scheme_callback: Callable[[None], None],
        dark_mode_callback: Callable[[ft.ControlEvent], None],
    ) -> None:
        super().__init__()
        self.macos_buttons_background = ft.Container(
            width=68,
            height=28,
            bgcolor=ft.colors.ON_TERTIARY,
            border_radius=ft.border_radius.only(0, 0, 0, 10),
            visible=False,
        )
        self.navigation_rail = self._create_navigation_rail(
            page_views,
            page_switcher_callback,
        )
        self.footer_buttons = self._create_footer_buttons(
            color_scheme_callback,
            dark_mode_callback,
        )
        self.controls = [
            self.macos_buttons_background,
            ft.Column(
                [
                    self.navigation_rail,
                    self.footer_buttons,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ]
        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.START

    def _create_navigation_rail(
        self,
        page_views: list[PageView],
        page_switcher_callback: Callable[[ft.ControlEvent], None],
    ) -> ft.NavigationRail:
        return ft.NavigationRail(
            selected_index=0,
            bgcolor=ft.colors.TERTIARY_CONTAINER,
            label_type=ft.NavigationRailLabelType.SELECTED,
            group_alignment=-1,
            expand=True,
            indicator_color=ft.colors.ON_TERTIARY,
            destinations=[
                page_view.navigation_rail_destination for page_view in page_views
            ],
            on_change=page_switcher_callback,
        )

    def _create_footer_buttons(
        self,
        color_scheme_callback: Callable[[None], None],
        dark_mode_callback: Callable[[ft.ControlEvent], None],
    ) -> ft.Column:
        color_randomizer_button = ft.IconButton(
            icon=ft.icons.COLOR_LENS_ROUNDED,
            icon_color=ft.colors.ON_TERTIARY_CONTAINER,
            tooltip="Change color scheme",
            on_click=color_scheme_callback,
        )
        dark_mode_button = ft.IconButton(
            icon=ft.icons.DARK_MODE_ROUNDED,
            icon_color=ft.colors.ON_TERTIARY_CONTAINER,
            tooltip="Dark mode",
            on_click=dark_mode_callback,
        )

        return ft.Column(
            [
                color_randomizer_button,
                dark_mode_button,
            ],
        )

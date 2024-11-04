from __future__ import annotations

import time
from typing import Callable

import flet as ft
from page_view import PageView


class NavigationPane(ft.Column):

    def __init__(
        self,
        views: list[PageView],
        navigation_callback: Callable[[ft.ControlEvent], None],
        color_scheme_callback: Callable[[ft.ControlEvent], None],
        light_switch_callback: Callable[[ft.ControlEvent], None],
    ) -> None:

        super().__init__()

        self.header = self._create_header()
        self.footer = self._create_footer(color_scheme_callback, light_switch_callback)
        self.navigation_rail = self._create_navigation_rail(views, navigation_callback)

        self.controls = [
            self.header,
            self.navigation_rail,
            self.footer,
        ]

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def _create_header(self) -> ft.Container:
        menu_button = ft.IconButton(
            icon=ft.icons.MENU_ROUNDED,
            icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            on_click=lambda _: self._extend_navigation_rail(),
        )
        return ft.Container(
            content=menu_button,
        )

    def _create_footer(
            self,
            color_scheme_callback: Callable[[ft.ControlEvent], None],
            dark_mode_callback: Callable[[ft.ControlEvent], None],
    ) -> ft.Container:
        color_button = ft.IconButton(
            icon=ft.icons.COLOR_LENS_ROUNDED,
            icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            on_click=color_scheme_callback,
        )
        light_switch = ft.IconButton(
            icon=ft.icons.DARK_MODE_ROUNDED,
            icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            on_click=dark_mode_callback,
        )
        return ft.Container(
            content=ft.Column(
                [
                    color_button,
                    light_switch,
                ],
            ),
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            padding=ft.padding.only(25, 10, 25, 25),
        )

    def _create_navigation_rail(
        self,
        views: list[PageView],
        navigation_callback: Callable[[ft.ControlEvent], None],
    ) -> ft.NavigationRail:

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.AUTO_AWESOME_ROUNDED,
            bgcolor=ft.colors.INVERSE_PRIMARY,
            elevation=5,
            hover_elevation=8,
        )

        return ft.NavigationRail(
            selected_index=0,
            group_alignment=0,
            label_type=ft.NavigationRailLabelType.SELECTED,
            bgcolor=ft.colors.TRANSPARENT,
            on_change=navigation_callback,
            destinations=[
                view.navigation_rail_destination for view in views
            ],
            leading=ft.Container(
                self.floating_action_button,
                margin=ft.margin.only(0,0,0,10),
            ),
            expand=True,
            indicator_color=ft.colors.INVERSE_PRIMARY,
        )

    def _extend_navigation_rail(self) -> None:

        self.update()

from __future__ import annotations

from typing import Callable

import flet as ft
from page_view import PageView


class NavigationPane(ft.Column):

    def __init__(
        self,
        views: list[PageView],
        navigation_callback: Callable[[ft.ControlEvent], None],
        dark_mode_callback: Callable[[ft.ControlEvent], None],
    ) -> None:

        super().__init__()

        self.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.AUTO_AWESOME_OUTLINED,
            elevation=0,
            hover_elevation=2,
            bgcolor=ft.colors.INVERSE_PRIMARY,
        )

        self.navigation_rail = ft.NavigationRail(
            destinations=[
                view.nav_rail_button for view in views
            ],
            selected_index=0,
            expand=True,
            min_width=100,
            label_type=ft.NavigationRailLabelType.SELECTED,
            group_alignment=0,
            on_change=navigation_callback,
            leading=ft.Container(
                self.floating_action_button,
                padding=ft.padding.symmetric(20,0),
            ),
            bgcolor=ft.colors.TRANSPARENT,
        )

        self.dark_mode_button = ft.IconButton(
            icon=ft.icons.DARK_MODE_OUTLINED,
            on_click=dark_mode_callback,
            icon_color=ft.colors.ON_SURFACE,
            style=ft.ButtonStyle(side=ft.BorderSide(1,ft.colors.ON_SURFACE)),
        )

        self.controls = [
            self.navigation_rail,
            ft.Container(
                self.dark_mode_button,
                margin=ft.margin.symmetric(25,0),
            ),
        ]

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def _extend_navigation_rail(self) -> None:
        self.navigation_rail.extended = not self.navigation_rail.extended
        self.update()

from __future__ import annotations

import flet as ft


class PageView(ft.Column):
    def __init__(
        self,
        name: str,
        navigation_icon: str,
        selected_navigation_icon: str,
    ) -> None:

        super().__init__()

        self.name = name
        self.navigation_icon = ft.Icon(navigation_icon)
        self.selected_navigation_icon = ft.Icon(selected_navigation_icon)
        self.nav_rail_button = self._create_navigation_rail_destination()

        self.header = ft.Text(value=self.name, style=ft.TextThemeStyle.HEADLINE_SMALL)

        self.scrolling_content = ft.ListView(expand=True)

        self.controls = [
            ft.Container(height=20),
            self.header,
            self.scrolling_content,
        ]

        self.spacing=20
        self.expand = True
        self.horizontal_alignment=ft.CrossAxisAlignment.STRETCH

    def _create_navigation_rail_destination(self) -> ft.NavigationRailDestination:
        return ft.NavigationRailDestination(
            label=self.name,
            icon_content=ft.Badge(
                self.navigation_icon,
                label_visible=False,
            ),
            selected_icon_content=ft.Badge(
                self.selected_navigation_icon,
                label_visible=False,
            ),
        )

    def update_badge_value(self, value: int) -> None:
        self.nav_rail_button.icon_content = ft.Badge(
            self.navigation_icon,
            text=str(value),
            label_visible=(value > 0),
        )
        self.nav_rail_button.selected_icon_content = ft.Badge(
            self.selected_navigation_icon,
            text=str(value),
            label_visible=(value > 0),
        )

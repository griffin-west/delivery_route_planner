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
        self.navigation_icon = ft.Icon(navigation_icon, color=ft.colors.ON_PRIMARY_CONTAINER)
        self.selected_navigation_icon = ft.Icon(selected_navigation_icon, color=ft.colors.ON_PRIMARY_CONTAINER)
        self.navigation_rail_destination = self._create_navigation_rail_destination()

        self.header = ft.Container(
            ft.Text(value=self.name, size=28),
            padding=ft.padding.only(0, 20, 0, 0),
        )

        self.scrolling_content = ft.ListView(expand=True)

        self.controls = [
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
        self.navigation_rail_destination.icon_content = ft.Badge(
            self.navigation_icon,
            text=str(value),
            label_visible=(value > 0),
        )
        self.navigation_rail_destination.selected_icon_content = ft.Badge(
            self.selected_navigation_icon,
            text=str(value),
            label_visible=(value > 0),
        )

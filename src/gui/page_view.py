from __future__ import annotations

import flet as ft


class PageView(ft.Column):
    def __init__(
        self,
        name: str,
        navigation_icon: str,
        navigation_icon_selected: str,
        floating_action_icon: str | None = None,
        floating_action_text: str | None = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.navigation_icon = ft.Icon(navigation_icon)
        self.navigation_icon_selected = ft.Icon(navigation_icon_selected)
        self.navigation_rail_destination = self._create_navigation_rail_destination()
        header = ft.Text(self.name, size=28, color=ft.colors.ON_SECONDARY_CONTAINER)
        row = ft.Row([header], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        if floating_action_icon and floating_action_text:
            self.floating_action_button = ft.FloatingActionButton(
                text=floating_action_text, icon=floating_action_icon,
            )
            row.controls.append(self.floating_action_button)
        self.controls = [row]
        self.expand = True
        self.horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        self.spacing=20

    def _create_navigation_rail_destination(self) -> ft.NavigationRailDestination:
        return ft.NavigationRailDestination(
            label=self.name,
            icon_content=ft.Badge(
                self.navigation_icon,
                bgcolor=ft.colors.PRIMARY,
                label_visible=False,
            ),
            selected_icon_content=ft.Badge(
                self.navigation_icon_selected,
                bgcolor=ft.colors.PRIMARY,
                label_visible=False,
            ),
        )

    def update_badge_value(self, value: int) -> None:
        self.navigation_rail_destination.icon_content = ft.Badge(
            self.navigation_icon,
            bgcolor=ft.colors.PRIMARY,
            text=str(value),
            label_visible=(value > 0),
        )

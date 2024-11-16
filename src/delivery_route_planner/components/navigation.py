from __future__ import annotations

import flet as ft


class Navigation:
    def __init__(self, page: ft.Page, views) -> None:  # noqa: ANN001
        self.page = page
        self.views = views
        self.view_pane = ft.Card(
            content=ft.Container(border_radius=15),
            margin=ft.margin.only(0, 0, 24, 24),
            expand=True,
            elevation=4,
        )

    def render(self) -> ft.Row:
        navigation_pane = self.create_navigation_pane(self.views)
        self.view_pane.content = self.views[0].render()

        return ft.Row(
            [navigation_pane, self.view_pane],
            expand=True,
            spacing=0,
        )

    def create_navigation_pane(self, views) -> ft.NavigationRail:  # noqa: ANN001
        return ft.NavigationRail(
            leading=ft.Container(
                ft.FloatingActionButton(
                    icon=ft.icons.AUTO_AWESOME_ROUNDED,
                    tooltip="Create delivery routes",
                    bgcolor=ft.colors.PRIMARY,
                    foreground_color=ft.colors.ON_PRIMARY,
                    elevation=2,
                    hover_elevation=4,
                ),
                padding=20,
            ),
            destinations=[
                ft.NavigationRailDestination(
                    label=view.title,
                    icon=view.icon,
                    selected_icon=view.selected_icon,
                    disabled=view.disabled,
                )
                for view in views
            ],
            selected_index=0,
            group_alignment=-0.2,
            label_type=ft.NavigationRailLabelType.SELECTED,
            indicator_color=ft.colors.INVERSE_PRIMARY,
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self.change_view,
        )

    def change_view(self, e: ft.ControlEvent) -> None:
        self.view_pane.content = self.views[e.control.selected_index].render()
        self.page.update()
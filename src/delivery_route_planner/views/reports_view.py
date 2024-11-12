import flet as ft

from delivery_route_planner.components.view_base import ViewBase


class ReportsView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = ViewBase(page)
        self.color = ft.colors.ORANGE_100
        self.title = "Reports"
        self.icon = ft.icons.BAR_CHART_ROUNDED
        self.selected_icon = ft.icons.BAR_CHART_ROUNDED
        self.disabled = True

    def render(self) -> ft.Container:
        self.view.title.value = self.title

        self.view.body.controls = []

        return self.view.render()

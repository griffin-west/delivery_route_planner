import flet as ft

from delivery_route_planner.components.page_view import PageView


class RoutesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = PageView(page)
        self.color = ft.colors.ORANGE_100
        self.title = "Routes"
        self.icon = ft.icons.ROUTE_OUTLINED
        self.selected_icon = ft.icons.ROUTE_ROUNDED
        self.disabled = True

    def render(self) -> ft.Container:
        self.view.title.value = self.title

        self.view.body.controls = []

        return self.view.render()

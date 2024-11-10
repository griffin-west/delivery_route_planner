import flet as ft

from delivery_route_planner.components.page_view import PageView


class VehiclesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = PageView(page)
        self.title = "Vehicles"
        self.icon = ft.icons.LOCAL_SHIPPING_OUTLINED
        self.selected_icon = ft.icons.LOCAL_SHIPPING_ROUNDED
        self.disabled = False

    def render(self) -> ft.Container:
        self.view.title.value = self.title
        self.view.action_button.text = "Add vehicle"
        self.view.action_button.icon = ft.icons.LOCAL_SHIPPING_OUTLINED

        self.view.body.controls = []

        return self.view.render()

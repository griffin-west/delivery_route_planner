import flet as ft

from delivery_route_planner.components.view_base import ViewBase


class AddressesView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = ViewBase(page)
        self.title = "Addresses"
        self.icon = ft.icons.LOCATION_ON_OUTLINED
        self.selected_icon = ft.icons.LOCATION_ON
        self.disabled = False

    def render(self) -> ft.Container:
        self.view.title.value = self.title

        self.view.body.controls = []

        return self.view.render()

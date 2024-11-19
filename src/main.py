import flet as ft

from delivery_route_planner import components, views
from delivery_route_planner.models import models


class DeliveryRoutePlanner:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.data = models.DataModel.with_defaults()
        self.window_manager = components.WindowManager(page)
        self.title_bar = components.TitleBar(page)
        self.views = [
            views.SetupView(page, self.data),
            views.PackagesView(page, self.data),
            views.VehiclesView(page, self.data),
            views.AddressesView(page, self.data),
            views.RoutesView(page),
            views.ReportsView(page),
        ]
        self.navigation_layout = components.Navigation(page, self.views)
        self._render_gui()

    def _render_gui(self) -> None:
        self.page.add(self.title_bar.render())
        self.page.add(self.navigation_layout.render())

def main(page: ft.Page) -> None:
    DeliveryRoutePlanner(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="delivery_route_planner/assets")

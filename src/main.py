import flet as ft

from delivery_route_planner import components, views
from delivery_route_planner.models import models


class DeliveryRoutePlanner:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.data = models.DataModel.with_defaults()

        self.window_manager = components.WindowManager(page)
        self.title_bar = components.TitleBar(page)
        self.navigation_manager = components.NavigationManager(page)
        self.views = {
            "setup": views.SetupView(page, self.data),
            "packages": views.PackagesView(page, self.data),
            "vehicles": views.VehiclesView(page, self.data),
            "addresses": views.AddressesView(page, self.data),
            "routes": views.RoutesView(page),
            "reports": views.ReportsView(page),
        }

        self.navigation_manager.set_views(self.views)

        self._render_gui()

    def _render_gui(self) -> None:
        self.page.add(self.title_bar.render())
        self.page.add(self.navigation_manager.render())


def main(page: ft.Page) -> None:
    DeliveryRoutePlanner(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="delivery_route_planner/assets")

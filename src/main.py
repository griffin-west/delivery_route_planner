import flet as ft

from delivery_route_planner.components.navigation import Navigation
from delivery_route_planner.components.title_bar import TitleBar
from delivery_route_planner.components.window_manager import WindowManager
from delivery_route_planner.models import models
from delivery_route_planner.views.addresses_view import AddressesView
from delivery_route_planner.views.packages_view import PackagesView
from delivery_route_planner.views.reports_view import ReportsView
from delivery_route_planner.views.routes_view import RoutesView
from delivery_route_planner.views.setup_view import SetupView
from delivery_route_planner.views.vehicles_view import VehiclesView


class DeliveryRoutePlanner:
    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.data = models.DataModel.with_defaults()
        self.scenario = models.RoutingScenario()
        self.settings = models.SearchSettings()

        self.window_manager = WindowManager(page)
        self.title_bar = TitleBar(page)
        self.views = [
            SetupView(page),
            PackagesView(page, self.data),
            VehiclesView(page, self.data),
            AddressesView(page, self.data),
            RoutesView(page),
            ReportsView(page),
        ]
        self.navigation_layout = Navigation(page, self.views)

        self._render_gui()

    def _render_gui(self) -> None:
        self.page.add(self.title_bar.render())
        self.page.add(self.navigation_layout.render())


def main(page: ft.Page) -> None:
    DeliveryRoutePlanner(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="delivery_route_planner/assets")

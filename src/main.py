import logging

import flet as ft

from delivery_route_planner import components, views
from delivery_route_planner.models import models
from delivery_route_planner.routing import routing


class DeliveryRoutePlanner:

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.data = models.DataModel.with_defaults()
        self.solution = None
        self.window_manager = components.WindowManager(page)
        self.title_bar = components.TitleBar(page)
        self.navigation_manager = components.NavigationManager(
            page,
            self.data,
            solution_callback=self.create_solution,
        )
        self.views = {
            "settings": views.SettingsView(
                page,
                self.data,
                self.navigation_manager.navigate_from_view_name,
            ),
            "packages": views.PackagesView(page, self.data),
            "vehicles": views.VehiclesView(
                page,
                self.data,
                self.navigation_manager.navigate_from_view_name,
            ),
            "addresses": views.AddressesView(page, self.data),
            "routes": views.RoutesView(page),
            "validation": views.ValidationView(page),
            "charts": views.ChartsView(page),
        }
        self.navigation_manager.set_views(self.views)
        self.render_gui()

    def render_gui(self) -> None:
        self.page.add(self.title_bar.render())
        self.page.add(self.navigation_manager.render())

    def create_solution(self) -> bool:
        try:
            solution = routing.solve_vehicle_routing_problem(self.data)
        except Exception as e:
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                raise
            logging.exception("An unexpected error occurred with Google OR-Tools.")
            return False
        else:
            if solution is None or solution.delivered_packages_count == 0:
                return False
            self.solution = solution
            self.views["routes"].set_solution(self.solution)
            self.views["validation"].set_solution(self.solution)
            self.views["charts"].set_solution(self.solution)
            return True


def main(page: ft.Page) -> None:
    DeliveryRoutePlanner(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="delivery_route_planner/assets")

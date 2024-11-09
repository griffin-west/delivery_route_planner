import flet as ft

from delivery_route_planner.components.navigation_pane import NavigationPane
from delivery_route_planner.components.title_bar import TitleBar
from delivery_route_planner.components.view_pane import ViewPane
from delivery_route_planner.components.window_manager import WindowManager


class DeliveryRoutePlanner:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.window_manager = WindowManager(page)
        self.title_bar = TitleBar(page)
        self.navigation_pane = NavigationPane(page)
        self.view_pane = ViewPane(page)

        self._setup_ui()

    def _setup_ui(self) -> None:
        panes_layout = ft.Row(
            [
                self.navigation_pane.render(),
                self.view_pane.render(),
            ],
            spacing=0,
            expand=True,
        )

        self.page.add(self.title_bar.render())
        self.page.add(panes_layout)

        self.view_pane.setup_initial_content()


def main(page: ft.Page) -> None:
    DeliveryRoutePlanner(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="delivery_route_planner/assets")

import flet as ft
from app_window import AppWindow
from page_view import PageView


def main(page: ft.Page) -> None:

    setup_view = PageView(
        name="Setup",
        navigation_icon=ft.icons.DESIGN_SERVICES_OUTLINED,
        selected_navigation_icon=ft.icons.DESIGN_SERVICES_ROUNDED,
    )
    package_view = PageView(
        "Packages",
        navigation_icon=ft.icons.INVENTORY_2_OUTLINED,
        selected_navigation_icon=ft.icons.INVENTORY_2_ROUNDED,
    )
    vehicle_view = PageView(
        "Vehicles",
        navigation_icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
        selected_navigation_icon=ft.icons.LOCAL_SHIPPING_ROUNDED,
    )
    address_view = PageView(
        "Addresses",
        navigation_icon=ft.icons.LOCATION_ON_OUTLINED,
        selected_navigation_icon=ft.icons.LOCATION_ON,
    )
    route_view = PageView(
        "Routes",
        navigation_icon=ft.icons.ROUTE_OUTLINED,
        selected_navigation_icon=ft.icons.ROUTE_ROUNDED,
    )
    about_view = PageView(
        "About",
        navigation_icon=ft.icons.INFO_OUTLINE_ROUNDED,
        selected_navigation_icon=ft.icons.INFO_ROUNDED,
    )

    views = [
        setup_view,
        package_view,
        vehicle_view,
        address_view,
        route_view,
        about_view,
    ]

    AppWindow(page, views)

    setup_view.scrolling_content.controls.extend(
        [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.SCIENCE_ROUNDED),
                                title=ft.Text("Search settings"),
                                subtitle=ft.Text(
                                    "Choose an optimization strategy from several algorithms."
                                ),
                            ),
                            ft.Column(
                                [
                                    ft.Dropdown(
                                        label="Outcome preference",
                                        options=[
                                            ft.dropdown.Option("Optimize for total mileage"),
                                            ft.dropdown.Option("Optimize for total time"),
                                        ], padding=10
                                    ),
                                    ft.Dropdown(
                                        label="First solution strategy",
                                        options=[
                                            ft.dropdown.Option("Cheapest cost insertion"),
                                            ft.dropdown.Option("Parallel cheapest insertion"),
                                        ], padding=10
                                    ),
                                    ft.Dropdown(
                                        label="Local search metaheuristic",
                                        options=[
                                            ft.dropdown.Option("Local guided search"),
                                            ft.dropdown.Option("Simulated annealing"),
                                        ], padding=10
                                    ),
                                ],
                            ),
                        ],
                    ),
                    padding=10,
                ), margin=10, color=ft.colors.TERTIARY_CONTAINER, elevation=5,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.DISPLAY_SETTINGS_ROUNDED),
                                title=ft.Text("Scenario and constraints"),
                                subtitle=ft.Text(
                                    "Choose which delivery constraints to apply in the search."
                                ),
                            ),
                            ft.Column(
                                [
                                    ft.Checkbox("Testing, testing, 234"),
                                    ft.Checkbox("Testing, testing, 234"),
                                    ft.Checkbox("Testing, testing, 234"),
                                    ft.Checkbox("Testing, testing, 234"),
                                    ft.Checkbox("Testing, testing, 234"),
                                ],
                            ),
                        ],
                    ),
                    padding=10,
                ), margin=10, color=ft.colors.TERTIARY_CONTAINER, elevation=5,
            ),
        ],
    )

    package_view.update_badge_value(40)
    address_view.update_badge_value(27)

    page.update()


if __name__ == "__main__":
    ft.app(target=main)

import flet as ft
from app_window import AppWindow
from page_view import PageView


def main(page: ft.Page) -> None:

    setup_view = PageView(
        name="Setup",
        navigation_icon=ft.icons.DISPLAY_SETTINGS_OUTLINED,
        selected_navigation_icon=ft.icons.DISPLAY_SETTINGS,
    )
    package_view = PageView(
        "Packages",
        navigation_icon=ft.icons.INVENTORY_2_OUTLINED,
        selected_navigation_icon=ft.icons.INVENTORY_2,
    )
    vehicle_view = PageView(
        "Vehicles",
        navigation_icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
        selected_navigation_icon=ft.icons.LOCAL_SHIPPING,
    )
    address_view = PageView(
        "Addresses",
        navigation_icon=ft.icons.LOCATION_ON_OUTLINED,
        selected_navigation_icon=ft.icons.LOCATION_ON,
    )
    route_view = PageView(
        "Routes",
        navigation_icon=ft.icons.ROUTE_OUTLINED,
        selected_navigation_icon=ft.icons.ROUTE,
    )

    views = [
        setup_view,
        package_view,
        vehicle_view,
        address_view,
        route_view,
    ]

    AppWindow(page, views)

    route_view.nav_rail_button.disabled = True

    setup_view.scrolling_content.controls.extend(
        [
            ft.Card(
                content = ft.Container(ft.Column(
                    spacing=10,
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.CHECKLIST),
                            title=ft.Text("Scenario constraints"),
                            subtitle=ft.Text(
                                "Select the requirements that must be included in the routing plans."
                            ),
                        ),
                        ft.Row(
                            [
                                ft.Chip(
                                    label=ft.Text("Delivery deadlines"),
                                    on_select=lambda _: page.update(),
                                ),
                                ft.Chip(
                                    label=ft.Text("Shipping delays"),
                                    on_select=lambda _: page.update(),
                                ),
                                ft.Chip(
                                    label=ft.Text("Vehicle capacities"),
                                    on_select=lambda _: page.update(),
                                ),
                                ft.Chip(
                                    label=ft.Text("Vehicle requirements"),
                                    on_select=lambda _: page.update(),
                                ),
                                ft.Chip(
                                    label=ft.Text("Package bundles"),
                                    on_select=lambda _: page.update(),
                                ),
                            ],
                            wrap=True,
                        ),
                        ft.SegmentedButton(
                            [
                                ft.Segment(value="Mileage", label=ft.Text("Mileage")),
                                ft.Segment(value="Time", label=ft.Text("Time")),
                            ],
                            selected={"Mileage"},
                            width=250,
                        ),
                        ft.Slider(min=0, max=100),
                    ],
                ), padding=20),
                elevation=0,
            ),
        ],
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)

import flet as ft
from app_window import AppWindow
from page_view import PageView


def main(page: ft.Page) -> None:

    setup_page = PageView(
        name="Setup",
        navigation_icon=ft.icons.DESIGN_SERVICES_OUTLINED,
        navigation_icon_selected=ft.icons.DESIGN_SERVICES_ROUNDED,
        floating_action_icon=ft.icons.AUTO_AWESOME_ROUNDED,
        floating_action_text="Plan routes",
    )
    packages_page = PageView(
        "Packages",
        navigation_icon=ft.icons.INVENTORY_2_OUTLINED,
        navigation_icon_selected=ft.icons.INVENTORY_2_ROUNDED,
        floating_action_icon=ft.icons.INVENTORY_2_ROUNDED,
        floating_action_text="Add package",
    )
    vehicles_page = PageView(
        "Vehicles",
        navigation_icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
        navigation_icon_selected=ft.icons.LOCAL_SHIPPING_ROUNDED,
        floating_action_icon=ft.icons.LOCAL_SHIPPING_ROUNDED,
        floating_action_text="Add vehicle",
    )
    places_page = PageView(
        "Locations",
        navigation_icon=ft.icons.LOCATION_ON_OUTLINED,
        navigation_icon_selected=ft.icons.LOCATION_ON,
    )
    routes_page = PageView(
        "Routes",
        navigation_icon=ft.icons.ROUTE_OUTLINED,
        navigation_icon_selected=ft.icons.ROUTE_ROUNDED,
    )
    about_page = PageView(
        "About",
        navigation_icon=ft.icons.INFO_OUTLINE_ROUNDED,
        navigation_icon_selected=ft.icons.INFO_ROUNDED,
    )

    page_views = [
        setup_page,
        packages_page,
        vehicles_page,
        places_page,
        routes_page,
        about_page,
    ]

    AppWindow(page, page_views)

    page.update()


if __name__ == "__main__":
    ft.app(target=main)

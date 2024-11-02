import flet as ft


def main(page: ft.Page):

    page.platform = ft.PagePlatform.MACOS

    def window_event_handler(event: ft.WindowEvent) -> None:
        match event.type:
            case ft.WindowEventType.CLOSE:
                page.open(exit_alert)
            case ft.WindowEventType.ENTER_FULL_SCREEN:
                mac_system_button_border.visible = False
            case ft.WindowEventType.LEAVE_FULL_SCREEN:
                mac_system_button_border.visible = (
                    page.platform == ft.PagePlatform.MACOS
                )
        page.update()

    def maximize(event: ft.ControlEvent) -> None:
        if page.window.maximized:
            page.window.maximized = False
            event.control.tooltip = "Maximize"
        else:
            page.window.maximized = True
            event.control.tooltip = "Restore"
        page.update()

    def minimize(event: ft.ControlEvent) -> None:
        page.window.minimized = True
        page.update()

    def dark_mode(event: ft.ControlEvent) -> None:
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            event.control.icon = ft.icons.LIGHT_MODE_ROUNDED
            event.control.tooltip = "Light mode"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            event.control.icon = ft.icons.DARK_MODE_ROUNDED
            event.control.tooltip = "Dark mode"
        page.update()

    def color_scheme(event: ft.ControlEvent) -> None:
        page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())
        page.update()

    page.title = "Delivery Route Planner"
    page.window.width = 1280
    page.window.height = 720
    page.window.min_width = 500
    page.window.min_height = 500
    page.padding = 0
    page.window.center()
    page.window.shadow = True
    page.window.prevent_close = True
    page.window.title_bar_hidden = True
    if page.platform in (ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX):
        page.window.title_bar_buttons_hidden = True
    page.window.on_event = window_event_handler

    page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())
    page.theme_mode = ft.ThemeMode.LIGHT

    exit_alert = ft.AlertDialog(
        content=ft.Text("Are you sure you want to exit the app?"),
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions=[
            ft.FilledTonalButton(
                "Cancel",
                on_click=lambda _: page.close(exit_alert),
                icon=ft.icons.ARROW_BACK_ROUNDED,
                style=ft.ButtonStyle(
                    overlay_color={
                        ft.ControlState.HOVERED: ft.colors.PRIMARY,
                        ft.ControlState.PRESSED: ft.colors.ON_PRIMARY_CONTAINER,
                    },
                    color={ft.ControlState.HOVERED: ft.colors.WHITE},
                ),
            ),
            ft.FilledTonalButton(
                "Exit",
                on_click=lambda _: page.window.destroy(),
                icon=ft.icons.CLOSE_ROUNDED,
                style=ft.ButtonStyle(
                    overlay_color={
                        ft.ControlState.DEFAULT: ft.colors.ERROR_CONTAINER,
                        ft.ControlState.HOVERED: ft.colors.ERROR,
                        ft.ControlState.PRESSED: ft.colors.ON_ERROR_CONTAINER,
                    },
                    color={ft.ControlState.HOVERED: ft.colors.WHITE},
                ),
            ),
        ],
    )

    rail = ft.NavigationRail(
        selected_index=0,
        bgcolor=ft.colors.TERTIARY_CONTAINER,
        expand=True,
        label_type=ft.NavigationRailLabelType.SELECTED,
        group_alignment=-1.0,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DESIGN_SERVICES_OUTLINED,
                selected_icon=ft.icons.DESIGN_SERVICES_ROUNDED,
                label="Configs",
                indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.icons.INVENTORY_2_ROUNDED,
                label="Packages",
                indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
                selected_icon=ft.icons.LOCAL_SHIPPING_ROUNDED,
                label="Vehicles",
                indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOCATION_ON_OUTLINED,
                selected_icon=ft.icons.LOCATION_ON,
                label="Locations",
                indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ROUTE_OUTLINED,
                selected_icon=ft.icons.ROUTE_ROUNDED,
                label="Routes",
                indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INFO_OUTLINE_ROUNDED,
                selected_icon=ft.icons.INFO_ROUNDED,
                label="About",
                indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
            ),
        ],
    )

    mac_system_button_border = ft.Container(
        width=68,
        height=28,
        bgcolor=ft.colors.ON_TERTIARY,
        border_radius=ft.border_radius.only(0, 0, 0, 10),
        visible=(page.platform == ft.PagePlatform.MACOS),
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    ft.Column(
                        [
                            mac_system_button_border,
                            ft.Column(
                                [
                                    rail,
                                    ft.IconButton(
                                        ft.icons.COLOR_LENS_ROUNDED,
                                        icon_color=ft.colors.ON_TERTIARY_CONTAINER,
                                        tooltip="Change color scheme",
                                        on_click=color_scheme,
                                    ),
                                    ft.IconButton(
                                        ft.icons.DARK_MODE_ROUNDED,
                                        icon_color=ft.colors.ON_TERTIARY_CONTAINER,
                                        tooltip="Dark mode",
                                        on_click=dark_mode,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                    ),
                    padding=(
                        ft.padding.only(0, 0, 0, 15)
                        if page.platform == ft.PagePlatform.MACOS
                        else ft.padding.symmetric(15, 0)
                    ),
                    bgcolor=ft.colors.TERTIARY_CONTAINER,
                ),
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.WindowDragArea(
                                    ft.Container(
                                        height=40,
                                    ),
                                    expand=True,
                                ),
                                ft.Container(
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                ft.icons.MINIMIZE_ROUNDED,
                                                icon_size=18,
                                                tooltip="Minimize",
                                                on_click=minimize,
                                            ),
                                            ft.IconButton(
                                                ft.icons.CROP_SQUARE_ROUNDED,
                                                icon_size=18,
                                                tooltip="Maximize",
                                                on_click=maximize,
                                            ),
                                            ft.IconButton(
                                                ft.icons.CLOSE_ROUNDED,
                                                icon_size=18,
                                                tooltip="Exit",
                                                hover_color=ft.colors.ERROR_CONTAINER,
                                                highlight_color=ft.colors.ERROR,
                                                style=ft.ButtonStyle(
                                                    icon_color={
                                                        ft.ControlState.HOVERED: ft.colors.ON_ERROR_CONTAINER
                                                    },
                                                ),
                                                on_click=lambda _: page.window.close(),
                                            ),
                                        ],
                                        spacing=0,
                                        visible=(
                                            page.platform
                                            in (
                                                ft.PagePlatform.WINDOWS,
                                                ft.PagePlatform.LINUX,
                                            )
                                        ),
                                    ),
                                    padding=ft.padding.only(0, 8, 8, 0),
                                ),
                            ],
                            spacing=0,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    spacing=0,
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)

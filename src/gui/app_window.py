"""Windowing-related classes for building the GUI with Flet.

This module provides:
- AppWindow: The outer window of the application.
- TitleBar: A custom title bar to replace the standard native OS title bar.
- NavigationRail
"""

from typing import Callable

import flet as ft


class AppWindow:
    """The outer window of the application.

    Attributes:
        page: The base object automatically provided by Flet.
        exit_alert: Non-modal pop-up dialog to confirm app exit.
        title_bar: Custom title bar instanced from TitleBar class.

    """

    def __init__(self, page: ft.Page) -> None:
        """Initialize the app's window and related events."""
        self.page = page
        self.exit_alert = self._create_exit_alert()
        self.title_bar = TitleBar(
            minimize_callback=lambda _: self._minimize_window(),
            maximize_callback=self._maximize_window,
            exit_callback=lambda _: self.page.open(self.exit_alert),
        )
        self.navigation_manager = NavigationManager(
            color_scheme_callback=lambda _: self._randomize_color_scheme(),
            dark_mode_callback=self._toggle_dark_mode,
        )

        self._setup_window()

        self.page.add(
            ft.Stack(
                [
                    ft.Container(
                        content=self.navigation_manager,
                        alignment=ft.alignment.top_center,
                    ),
                    ft.Container(
                        content=self.title_bar,
                        alignment=ft.alignment.top_center,
                        height=40,
                    ),
                ],
                expand=True,
            ),
        )

    def _setup_window(self) -> None:
        self.page.title = "Delivery Route Planner"
        self.page.window.width = 1280
        self.page.window.height = 720
        self.page.window.min_width = 400
        self.page.window.min_height = 520
        self.page.window.center()
        self.page.window.shadow = True
        self.page.window.prevent_close = True
        self.page.window.title_bar_hidden = True
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())
        self.page.window.on_event = self._window_event_handler
        if self.page.platform == ft.PagePlatform.MACOS:
            self.title_bar.macos_buttons_background.visible = True
        elif self.page.platform in (ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX):
            self.title_bar.windows_buttons.visible = True

    def _create_exit_alert(self) -> ft.AlertDialog:
        exit_button = ft.FilledTonalButton(
            "Exit",
            on_click=lambda _: self.page.window.destroy(),
            icon=ft.icons.CLOSE_ROUNDED,
            style=ft.ButtonStyle(
                overlay_color={
                    ft.ControlState.DEFAULT: ft.colors.ERROR_CONTAINER,
                    ft.ControlState.HOVERED: ft.colors.ERROR,
                    ft.ControlState.PRESSED: ft.colors.ON_ERROR_CONTAINER,
                },
                color={ft.ControlState.HOVERED: ft.colors.ON_ERROR},
            ),
        )
        close_button = ft.FilledTonalButton(
            "Cancel",
            on_click=lambda _: self.page.close(self.exit_alert),
            icon=ft.icons.ARROW_BACK_ROUNDED,
            style=ft.ButtonStyle(
                overlay_color={
                    ft.ControlState.HOVERED: ft.colors.PRIMARY,
                    ft.ControlState.PRESSED: ft.colors.ON_PRIMARY_CONTAINER,
                },
                color={ft.ControlState.HOVERED: ft.colors.ON_PRIMARY},
            ),
        )
        return ft.AlertDialog(
            content=ft.Text("Are you sure you want to exit the app?"),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            actions=[close_button, exit_button],
        )

    def _window_event_handler(self, event: ft.WindowEvent) -> None:
        match event.type:
            case ft.WindowEventType.CLOSE:
                self.page.open(self.exit_alert)
            case ft.WindowEventType.ENTER_FULL_SCREEN:
                self.title_bar.macos_buttons_background.visible = False
            case ft.WindowEventType.LEAVE_FULL_SCREEN:
                if self.page.platform == ft.PagePlatform.MACOS:
                    self.title_bar.macos_buttons_background.visible = True
        self.page.update()

    def _minimize_window(self) -> None:
        self.page.window.minimized = True
        self.page.update()

    def _maximize_window(self, event: ft.ControlEvent) -> None:
        self.page.window.maximized = not self.page.window.maximized
        if self.page.window.maximized:
            event.control.icon = ft.icons.CLOSE_FULLSCREEN_ROUNDED
            event.control.tooltip = "Restore"
        else:
            event.control.icon = ft.icons.OPEN_IN_FULL_ROUNDED
            event.control.tooltip = "Maximize"
        self.page.update()

    def _randomize_color_scheme(self) -> None:
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())
        self.page.update()

    def _toggle_dark_mode(self, event: ft.ControlEvent) -> None:
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            event.control.icon = ft.icons.LIGHT_MODE_ROUNDED
            event.control.tooltip = "Light mode"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            event.control.icon = ft.icons.DARK_MODE_ROUNDED
            event.control.tooltip = "Dark mode"
        self.page.update()


class TitleBar(ft.Row):
    """A custom title bar to replace the standard native OS title bar.

    Attributes:
        macos_buttons_background: Border to visually separate MacOS traffic lights.
        windows_buttons: Custom caption buttons for windowing on Windows or Linux.

    """

    def __init__(
        self,
        minimize_callback: Callable[[None], None],
        maximize_callback: Callable[[ft.ControlEvent], None],
        exit_callback: Callable[[None], None],
    ) -> None:
        """Initialize the title bar as an extension of Flet's Row class."""
        super().__init__()
        self.macos_buttons_background = ft.Container(
            width=68,
            height=28,
            bgcolor=ft.colors.ON_TERTIARY,
            border_radius=ft.border_radius.only(0, 0, 0, 10),
            visible=False,
        )
        self.windows_buttons = self._create_windows_buttons(
            minimize_callback,
            maximize_callback,
            exit_callback,
        )
        self.controls = [
            self.macos_buttons_background,
            ft.WindowDragArea(
                content=ft.Container(
                    height=40,
                ),
                expand=True,
            ),
            self.windows_buttons,
        ]
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.spacing = 0

    def _create_windows_buttons(
        self,
        minimize_callback: Callable[[None], None],
        maximize_callback: Callable[[ft.ControlEvent], None],
        exit_callback: Callable[[None], None],
    ) -> ft.Container:
        minimize_button = ft.IconButton(
            icon=ft.icons.MINIMIZE_ROUNDED,
            icon_size=14,
            tooltip="Minimize",
            on_click=minimize_callback,
        )
        maximize_button = ft.IconButton(
            icon=ft.icons.OPEN_IN_FULL_ROUNDED,
            icon_size=14,
            tooltip="Maximize",
            on_click=maximize_callback,
        )
        exit_button = ft.IconButton(
            icon=ft.icons.CLOSE_ROUNDED,
            icon_size=14,
            tooltip="Exit",
            on_click=exit_callback,
            hover_color=ft.colors.ERROR_CONTAINER,
            highlight_color=ft.colors.ERROR,
            style=ft.ButtonStyle(
                icon_color={
                    ft.ControlState.HOVERED: ft.colors.ON_ERROR_CONTAINER,
                },
            ),
        )
        return ft.Container(
            content=ft.Row(
                controls=[minimize_button, maximize_button, exit_button],
                spacing=0,
            ),
            padding=ft.padding.only(0, 8, 8, 0),
            visible=False,
        )


class NavigationManager(ft.Row):
    """A left-aligned navigation bar to switch between app pages.

    Attributes:
        left_side_bar: NavigationRail extended with additional footer buttons.
        app_page_container: Main canvas of the app to display various pages.

    """

    def __init__(
        self,
        color_scheme_callback: Callable[[None], None],
        dark_mode_callback: Callable[[ft.ControlEvent], None],
    ) -> None:
        """Initialize the NavigationManager as an extension of Flet's Row class."""
        super().__init__()
        navigation_rail = self._create_navigation_rail()
        footer_buttons = self._create_footer_buttons(
            color_scheme_callback,
            dark_mode_callback,
        )
        self.left_side_bar = ft.Container(
            ft.Column(
                [navigation_rail, footer_buttons],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                expand=True,
            ),
            padding=ft.padding.only(10,40,10,20),
            bgcolor=ft.colors.TERTIARY_CONTAINER,

        )
        self.app_page_container = ft.Container(
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            margin=ft.margin.only(20,20,20,20),
            border_radius=ft.border_radius.all(20),
            expand=True,
        )
        self.controls = [
            self.left_side_bar,
            self.app_page_container,
        ]
        self.spacing = 0


    def _create_navigation_rail(self) -> ft.NavigationRail:
        setup_button = ft.NavigationRailDestination(
            icon=ft.icons.DESIGN_SERVICES_OUTLINED,
            selected_icon=ft.icons.DESIGN_SERVICES_ROUNDED,
            label="Setup",
            indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
        )
        packages_button = ft.NavigationRailDestination(
            icon=ft.icons.INVENTORY_2_OUTLINED,
            selected_icon=ft.icons.INVENTORY_2_ROUNDED,
            label="Packages",
            indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
        )
        vehicles_button = ft.NavigationRailDestination(
            icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
            selected_icon=ft.icons.LOCAL_SHIPPING_ROUNDED,
            label="Vehicles",
            indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
        )
        places_button = ft.NavigationRailDestination(
            icon=ft.icons.LOCATION_ON_OUTLINED,
            selected_icon=ft.icons.LOCATION_ON,
            label="Places",
            indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
        )
        routes_button = ft.NavigationRailDestination(
            icon=ft.icons.ROUTE_OUTLINED,
            selected_icon=ft.icons.ROUTE_ROUNDED,
            label="Routes",
            indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
        )
        about_button = ft.NavigationRailDestination(
            icon=ft.icons.INFO_OUTLINE_ROUNDED,
            selected_icon=ft.icons.INFO_ROUNDED,
            label="About",
            indicator_color=ft.colors.ON_TERTIARY_CONTAINER,
        )

        return ft.NavigationRail(
            selected_index=0,
            bgcolor=ft.colors.TERTIARY_CONTAINER,
            label_type=ft.NavigationRailLabelType.SELECTED,
            group_alignment=-0.9,
            expand=True,
            leading=ft.Container(
                ft.FloatingActionButton(
                    icon=ft.icons.AUTO_AWESOME_OUTLINED,
                    bgcolor=ft.colors.PRIMARY,
                    foreground_color=ft.colors.ON_PRIMARY,
                ),
                padding=ft.padding.only(0,0,0,10),
            ),
            destinations=[
                setup_button,
                packages_button,
                vehicles_button,
                places_button,
                routes_button,
                about_button,
            ],
        )

    def _create_footer_buttons(
        self,
        color_scheme_callback: Callable[[None], None],
        dark_mode_callback: Callable[[ft.ControlEvent], None],
    ) -> ft.Column:
        color_randomizer_button = ft.IconButton(
            icon=ft.icons.COLOR_LENS_ROUNDED,
            icon_color=ft.colors.ON_TERTIARY_CONTAINER,
            tooltip="Change color scheme",
            on_click=color_scheme_callback,
        )
        dark_mode_button = ft.IconButton(
            icon=ft.icons.DARK_MODE_ROUNDED,
            icon_color=ft.colors.ON_TERTIARY_CONTAINER,
            tooltip="Dark mode",
            on_click=dark_mode_callback,
        )

        return ft.Column(
            [
                color_randomizer_button,
                dark_mode_button,
            ],
        )


def main(page: ft.Page) -> None:
    """Test classes."""
    AppWindow(page)


if __name__ == "__main__":
    ft.app(target=main)

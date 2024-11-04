from __future__ import annotations

import flet as ft
from navigation_pane import NavigationPane
from page_view import PageView
from title_bar import TitleBar


class AppWindow:
    def __init__(self, page: ft.Page, page_views: list[PageView]) -> None:
        self.page = page
        self.page_views = page_views
        self.exit_alert = self._create_exit_alert()
        self.title_bar = TitleBar(
            minimize_callback=lambda _: self._minimize_window(),
            maximize_callback=lambda _: self._maximize_window(),
            exit_callback=lambda _: self.page.open(self.exit_alert),
        )
        self.navigation_pane = NavigationPane(
            page_views=self.page_views,
            page_switcher_callback=self._switch_view,
            color_scheme_callback=lambda _: self._randomize_color_scheme(),
            dark_mode_callback=self._toggle_dark_mode,
        )

        self.view_switcher = ft.AnimatedSwitcher(
            content=self.page_views[0],
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=100,
            reverse_duration=100,
            expand=True,
        )

        self.view_pane = ft.Container(
            content=self.view_switcher,
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            margin=ft.margin.only(30, 0, 30, 30),
            padding=ft.padding.all(30),
            border_radius=15,
            expand=True,
        )

        self._setup_window()
        page.add(self._complete_app_layout())

    def _complete_app_layout(self) -> ft.Row:
        navigation_area = ft.Container(
            self.navigation_pane,
            padding=ft.padding.only(0, 0, 0, 20),
            bgcolor=ft.colors.TERTIARY_CONTAINER,
        )
        view_area = ft.Column(
            [self.title_bar, self.view_pane],
            expand=True,
            spacing=0,
        )
        return ft.Row(
            [navigation_area, view_area],
            expand=True,
            spacing=0,
        )

    def _setup_window(self) -> None:
        self.page.window.width = 1000
        self.page.window.height = 600
        self.page.window.min_width = 525
        self.page.window.min_height = 525
        self.page.window.center()
        self.page.window.shadow = True
        self.page.window.prevent_close = True
        self.page.window.title_bar_hidden = True
        self.page.window.on_event = self._window_event_handler

        self.page.title = "Delivery Route Planner"
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.floating_action_button_theme = ft.FloatingActionButtonTheme(
            bgcolor=ft.colors.PRIMARY,
            foreground_color=ft.colors.ON_PRIMARY,
            splash_color=ft.colors.ON_PRIMARY_CONTAINER,
        )
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.random_color(),
            floating_action_button_theme=self.floating_action_button_theme,
        )

        self.page.platform = ft.PagePlatform.MACOS
        if self.page.platform == ft.PagePlatform.MACOS:
            self.navigation_pane.macos_buttons_background.visible = True
        elif self.page.platform == ft.PagePlatform.WINDOWS:
            self.page.window.title_bar_buttons_hidden = True
            self.title_bar.windows_buttons.visible = True
            self.title_bar.drag_area.height = 50

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
            icon=ft.icons.UNDO_ROUNDED,
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
        if event.type == ft.WindowEventType.CLOSE:
            self.page.open(self.exit_alert)

        if self.page.window.maximized:
            self.title_bar.maximize_button.icon = ft.icons.CLOSE_FULLSCREEN_ROUNDED
            self.title_bar.tooltip = "Unmaximize"
        else:
            self.title_bar.maximize_button.icon = ft.icons.OPEN_IN_FULL_ROUNDED
            self.title_bar.tooltip = "Maximize"

        if self.page.window.full_screen:
            self.navigation_pane.macos_buttons_background.visible = False
        elif self.page.platform == ft.PagePlatform.MACOS:
            self.navigation_pane.macos_buttons_background.visible = True

        self.page.update()

    def _minimize_window(self) -> None:
        self.page.window.minimized = True
        self.page.update()

    def _maximize_window(self) -> None:
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

    def _randomize_color_scheme(self) -> None:
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.random_color(),
            floating_action_button_theme=self.floating_action_button_theme,
        )
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

    def _switch_view(self, event: ft.ControlEvent) -> None:
        page_index = event.control.selected_index
        self.view_switcher.content = self.page_views[page_index]
        self.view_switcher.update()

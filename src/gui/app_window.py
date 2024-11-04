from __future__ import annotations

import flet as ft
from navigation_pane import NavigationPane
from page_view import PageView
from title_bar import TitleBar


class AppWindow:
    def __init__(self, page: ft.Page, views: list[PageView]) -> None:

        self.page = page
        self.views = views

        self.close_alert = self._create_close_alert()

        self.title_bar = TitleBar(
            minimize_callback=lambda _: self._minimize_window(),
            maximize_callback=lambda _: self._maximize_window(),
            close_callback=lambda _: self.page.open(self.close_alert),
        )
        self.navigation_pane = NavigationPane(
            views=self.views,
            navigation_callback=self._switch_view,
            color_scheme_callback=lambda _: self._randomize_color_scheme(),
            light_switch_callback=self._toggle_light_switch,
        )
        self.view_switch = ft.AnimatedSwitcher(
            content=self.views[0],
            duration=0,
            reverse_duration=0,
            expand=True,
        )
        self.view_pane = ft.Container(
            content=self.view_switch,
            bgcolor=ft.colors.SURFACE,
            margin=ft.margin.only(0, 0, 30, 30),
            padding=ft.padding.symmetric(0,30),
            border_radius=10,
            expand=True,
        )

        self._setup_window()

        page.add(self.title_bar)
        page.add(
            ft.Row(
                [
                    self.navigation_pane,
                    self.view_pane,
                ],
                spacing=0,
                expand=True,
            ),
        )

    def _create_close_alert(self) -> ft.AlertDialog:

        cancel_button = ft.TextButton(
            "Cancel",
            on_click=lambda _: self.page.close(self.close_alert),
        )
        close_button = ft.FilledTonalButton(
            "Exit",
            on_click=lambda _: self.page.window.destroy(),
        )

        return ft.AlertDialog(
            icon=ft.Icon(ft.icons.FRONT_HAND_ROUNDED),
            title=ft.Text("Exit app?", text_align=ft.TextAlign.CENTER),
            content=ft.Text("Are you sure you want to exit the app?\nRoutes and settings will not be saved."),
            actions=[
                cancel_button,
                close_button,
            ],
            modal=True,
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _setup_window(self) -> None:
        self.page.window.center()
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.shadow = True
        self.page.window.prevent_close = True
        self.page.window.title_bar_hidden = True
        self.page.window.on_event = self._window_event_handler

        self.page.padding = 0
        self.page.spacing = 0
        self.page.title = "Delivery Route Planner"
        self.page.bgcolor = ft.colors.SECONDARY_CONTAINER
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())

        if self.page.platform == ft.PagePlatform.WINDOWS:
            self.page.window.title_bar_buttons_hidden = True
            self.title_bar.caption_buttons.visible = True
            self.title_bar.window_drag_area.height = 40

    def _window_event_handler(self, event: ft.WindowEvent) -> None:
        if event.type == ft.WindowEventType.CLOSE:
            self.page.open(self.close_alert)
        self.page.update()

    def _minimize_window(self) -> None:
        self.page.window.minimized = True
        self.page.update()

    def _maximize_window(self) -> None:
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

    def _toggle_light_switch(self, event: ft.ControlEvent) -> None:
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            event.control.icon = ft.icons.LIGHT_MODE_ROUNDED
            event.control.tooltip = "Light mode"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            event.control.icon = ft.icons.DARK_MODE_ROUNDED
            event.control.tooltip = "Dark mode"
        self.page.update()

    def _randomize_color_scheme(self) -> None:
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())
        self.page.update()

    def _switch_view(self, event: ft.ControlEvent) -> None:
        view_index = event.control.selected_index
        self.view_switch.content = self.views[view_index]
        self.view_switch.update()

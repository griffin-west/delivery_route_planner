import flet as ft


class WindowManager:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self._setup_window()

    def _setup_window(self) -> None:
        close_alert = ft.AlertDialog(
            modal=True,
            icon=ft.Icon(ft.icons.EXIT_TO_APP_ROUNDED),
            title=ft.Text("Exit app?", text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                [
                    ft.Text("Are you sure you want to exit the app?"),
                    ft.Text("Routes and settings will not be saved."),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=lambda _: self.page.close(close_alert),
                ),
                ft.FilledTonalButton(
                    "Exit",
                    on_click=lambda _: self.page.window.destroy(),
                ),
            ],
        )

        def _window_event_handler(e: ft.WindowEvent) -> None:
            if e.type == ft.WindowEventType.CLOSE:
                self.page.open(close_alert)
            self.page.update()

        self.page.title = "Delivery Route Planner"
        self.page.window.width = 1280
        self.page.window.height = 720
        self.page.window.min_width = 450
        self.page.window.min_height = 450
        self.page.window.shadow = True
        self.page.window.prevent_close = True
        self.page.window.title_bar_hidden = True
        self.page.window.on_event = _window_event_handler
        self.page.padding = 0
        self.page.spacing = 0
        self.page.window.center()

        self.page.fonts = {
            "Outfit": "fonts/Outfit-Regular.ttf",
            "Roboto": "fonts/Roboto-Regular.ttf",
            "Roboto Serif": "fonts/RobotoSerif-Regular.ttf",
        }
        self.page.theme = ft.Theme(
            font_family="Outfit",
            color_scheme_seed=ft.colors.random_color(),
        )
        self.page.bgcolor = ft.colors.SURFACE_VARIANT

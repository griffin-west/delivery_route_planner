import flet as ft


class TitleBar:
    def __init__(self, page: ft.Page) -> None:
        self.page = page

    def render(self) -> ft.Row:
        window_drag_area = ft.WindowDragArea(
            content=ft.Container(),
            expand=True,
            height=(48 if self.page.platform == ft.PagePlatform.WINDOWS else 30),
        )

        minimize_button = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_size=18,
            tooltip="Minimize",
            on_click=self._minimize_window,
            icon_color=ft.colors.ON_SURFACE,
        )

        maximize_button = ft.IconButton(
            icon=ft.icons.CROP_SQUARE_ROUNDED,
            icon_size=18,
            tooltip="Maximize",
            on_click=self._maximize_window,
            icon_color=ft.colors.ON_SURFACE,
        )

        exit_button = ft.IconButton(
            icon=ft.icons.CLOSE_ROUNDED,
            icon_size=18,
            tooltip="Close",
            on_click=lambda _: self.page.window.close(),
            icon_color=ft.colors.ON_SURFACE,
        )

        caption_buttons = ft.Container(
            content=ft.Row(
                controls=[
                    minimize_button,
                    maximize_button,
                    exit_button,
                ],
                spacing=0,
            ),
            padding=ft.padding.all(5),
            visible=(self.page.platform == ft.PagePlatform.WINDOWS),
        )

        return ft.Row(
            controls=[
                window_drag_area,
                caption_buttons,
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _minimize_window(self, e: ft.ControlEvent) -> None:
        _ = e
        self.page.window.minimized = True
        self.page.update()

    def _maximize_window(self, e: ft.ControlEvent) -> None:
        _ = e
        self.page.window.maximized = not self.page.window.maximized
        self.page.update()

from typing import Callable

import flet as ft


class TitleBar(ft.Row):

    def __init__(
        self,
        minimize_callback: Callable[[None], None],
        maximize_callback: Callable[[ft.ControlEvent], None],
        close_callback: Callable[[None], None],
    ) -> None:

        super().__init__()

        self.window_drag_area = ft.WindowDragArea(
            content=ft.Container(),
            expand=True,
            height=30,
        )
        self.caption_buttons = self._create_caption_buttons(
            minimize_callback,
            maximize_callback,
            close_callback,
        )

        self.controls = [
            self.window_drag_area,
            self.caption_buttons,
        ]

        self.spacing = 0
        self.vertical_alignment = ft.CrossAxisAlignment.START

    def _create_caption_buttons(
        self,
        minimize_callback: Callable[[None], None],
        maximize_callback: Callable[[ft.ControlEvent], None],
        exit_callback: Callable[[None], None],
    ) -> ft.Container:

        self.minimize_button = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_size=18,
            icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            tooltip="Minimize",
            on_click=minimize_callback,
        )
        self.maximize_button = ft.IconButton(
            icon=ft.icons.CROP_SQUARE_ROUNDED,
            icon_size=18,
            icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            tooltip="Maximize",
            on_click=maximize_callback,
        )
        self.exit_button = ft.IconButton(
            icon=ft.icons.CLOSE_ROUNDED,
            icon_size=18,
            icon_color=ft.colors.ON_PRIMARY_CONTAINER,
            tooltip="Close",
            on_click=exit_callback,

            style=ft.ButtonStyle(
                color={
                    ft.ControlState.PRESSED: ft.colors.ERROR,
                    ft.ControlState.HOVERED: ft.colors.ERROR_CONTAINER,
                },
                icon_color={
                    ft.ControlState.HOVERED: ft.colors.ON_ERROR_CONTAINER,
                },
            ),
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    self.minimize_button,
                    self.maximize_button,
                    self.exit_button,
                ],
                spacing=0,
            ),
            padding=ft.padding.all(5),
            visible=False,
        )

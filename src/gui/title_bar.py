from typing import Callable

import flet as ft


class TitleBar(ft.Row):
    def __init__(
        self,
        minimize_callback: Callable[[None], None],
        maximize_callback: Callable[[ft.ControlEvent], None],
        exit_callback: Callable[[None], None],
    ) -> None:
        super().__init__()
        self.windows_buttons = self._create_windows_buttons(
            minimize_callback,
            maximize_callback,
            exit_callback,
        )
        self.drag_area = ft.WindowDragArea(
            content=ft.Container(
                height=30,
            ),
            expand=True,
        )
        self.controls = [
            self.drag_area,
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
        self.minimize_button = ft.IconButton(
            icon=ft.icons.MINIMIZE_ROUNDED,
            icon_size=20,
            tooltip="Minimize",
            on_click=minimize_callback,
        )
        self.maximize_button = ft.IconButton(
            icon=ft.icons.OPEN_IN_FULL_ROUNDED,
            icon_size=20,
            tooltip="Maximize",
            on_click=maximize_callback,
        )
        self.exit_button = ft.IconButton(
            icon=ft.icons.CLOSE_ROUNDED,
            icon_size=20,
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
                controls=[self.minimize_button, self.maximize_button, self.exit_button],
                spacing=0,
            ),
            padding=ft.padding.only(0, 8, 8, 8),
            visible=False,
        )

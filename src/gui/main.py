import flet as ft  # noqa: D100, INP001


def _create_window(page: ft.Page) -> None:

    close_alert = ft.AlertDialog(
        icon=ft.Icon(ft.icons.FRONT_HAND_ROUNDED),
        title=ft.Text("Exit app?", text_align=ft.TextAlign.CENTER),
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
                on_click=lambda _: page.close(close_alert),
            ),
            ft.FilledTonalButton(
                "Exit",
                on_click=lambda _: page.window.destroy(),
            ),
        ],
        modal=True,
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def _window_event_handler(e: ft.WindowEvent) -> None:
        if e.type == ft.WindowEventType.CLOSE:
            page.open(close_alert)
        page.update()

    page.window.center()
    page.window.width = 1000
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 500
    page.window.shadow = True
    page.window.prevent_close = True
    page.window.title_bar_hidden = True
    page.window.on_event = _window_event_handler

    page.padding = 0
    page.spacing = 0
    page.title = "Delivery Route Planner"
    page.bgcolor = ft.colors.ON_INVERSE_SURFACE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())

def _create_title_bar(page: ft.Page) -> ft.Row:

    window_drag_area = ft.WindowDragArea(
        content=ft.Container(),
        expand=True,
        height=(48 if page.platform == ft.PagePlatform.WINDOWS else 30),
    )

    def _minimize_window() -> None:
        page.window.minimized = True
        page.update()

    minimize_button = ft.IconButton(
        icon=ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED,
        icon_size=18,
        tooltip="Minimize",
        on_click=lambda _: _minimize_window(),
        icon_color=ft.colors.ON_SURFACE,
    )

    def _maximize_window() -> None:
        page.window.maximized = not page.window.maximized
        page.update()

    maximize_button = ft.IconButton(
        icon=ft.icons.CROP_SQUARE_ROUNDED,
        icon_size=18,
        tooltip="Maximize",
        on_click=lambda _: _maximize_window(),
        icon_color=ft.colors.ON_SURFACE,
    )

    exit_button = ft.IconButton(
        icon=ft.icons.CLOSE_ROUNDED,
        icon_size=18,
        tooltip="Close",
        on_click=lambda _: page.window.close(),
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
        visible=(page.platform == ft.PagePlatform.WINDOWS),
    )

    return ft.Row(
        controls=[
            window_drag_area,
            caption_buttons,
        ],
        spacing=0,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

def _create_navigation_pane(page: ft.Page) -> ft.Column:
    navigation_rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(
                label="Setup",
                icon=ft.icons.EDIT_OUTLINED,
                selected_icon=ft.icons.EDIT_ROUNDED,
            ),
            ft.NavigationRailDestination(
                label="Packages",
                icon=ft.icons.INVENTORY_2_OUTLINED,
                selected_icon=ft.icons.INVENTORY_2_ROUNDED,
            ),
            ft.NavigationRailDestination(
                label="Vehicles",
                icon=ft.icons.LOCAL_SHIPPING_OUTLINED,
                selected_icon=ft.icons.LOCAL_SHIPPING_ROUNDED,
            ),
            ft.NavigationRailDestination(
                label="Locations",
                icon=ft.icons.LOCATION_ON_OUTLINED,
                selected_icon=ft.icons.LOCATION_ON,
            ),
            ft.NavigationRailDestination(
                label="Routes",
                icon=ft.icons.ROUTE_OUTLINED,
                selected_icon=ft.icons.ROUTE_ROUNDED,
                disabled=True,
            ),
            ft.NavigationRailDestination(
                label="Data",
                icon=ft.icons.INSERT_CHART_OUTLINED_ROUNDED,
                selected_icon=ft.icons.INSERT_CHART_ROUNDED,
                disabled=True,
            ),
        ],
        expand=True,
        extended=True,
        selected_index=0,
        group_alignment=0,
        min_extended_width=170,
        bgcolor=ft.colors.TRANSPARENT,
        label_type=ft.NavigationRailLabelType.NONE,
        leading=ft.Container(
            ft.FloatingActionButton(
                text="Solve",
                icon=ft.icons.AUTO_AWESOME_ROUNDED,
                bgcolor=ft.colors.INVERSE_PRIMARY,
                width=120,
            ),
            padding=ft.padding.symmetric(20,0),
        ),
    )

    def _toggle_dark_mode(e: ft.ControlEvent) -> None:
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.DARK_MODE_ROUNDED
        page.update()

    dark_mode_button = ft.IconButton(
        icon=ft.icons.DARK_MODE_ROUNDED,
        on_click=_toggle_dark_mode,
    )

    def _randomize_colors(e: ft.ControlEvent) -> None:
        page.theme = ft.Theme(color_scheme_seed=ft.colors.random_color())
        page.update()

    color_button = ft.IconButton(
        icon=ft.icons.COLOR_LENS_ROUNDED,
        on_click=_randomize_colors,
    )

    return ft.Column(
        [
            navigation_rail,
            ft.Row([dark_mode_button, color_button]),
            ft.Container(height=10),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

def _create_app(page: ft.Page) -> None:

    _create_window(page)

    title_bar = _create_title_bar(page)

    navigation_pane = _create_navigation_pane(page)

    content = ft.Column(expand=True)

    view_pane = ft.Container(
        content=content,
        margin=ft.margin.only(0, 0, 24, 24),
        border_radius=ft.border_radius.all(20),
        expand=True,
        bgcolor=ft.colors.SURFACE,
        padding=30,
    )

    panes_layout = ft.Row(
        [
            navigation_pane,
            view_pane,
        ],
        spacing=0,
        expand=True,
    )

    page.add(title_bar)
    page.add(panes_layout)

    content.controls.extend(
        [
            ft.Row(
                [
                    ft.Text(
                        value="Setup",
                        style=ft.TextThemeStyle.HEADLINE_LARGE,
                    ),
                    ft.FilledTonalButton(
                        text="Reset values",
                        icon=ft.icons.UNDO_ROUNDED,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=_create_app, assets_dir="assets")

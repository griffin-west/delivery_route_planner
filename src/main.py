import flet as ft

from delivery_route_planner import gui, models


def main(page: ft.Page) -> None:

    data = models.DataModel.create_with_defaults()

    results_content = ft.Column(
        [
            ft.Card(
                ft.Container(
                    ft.Text("Solution has not been created yet."),
                    padding=30,
                ),
                color=ft.colors.SURFACE,
                elevation=2,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=30,
    )
    results_page = ft.Container(
        results_content,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(0, 30),
        bgcolor=ft.colors.ON_INVERSE_SURFACE,
    )

    charts_content = ft.Column(
        [
            ft.Card(
                ft.Container(
                    ft.Text("Solution has not been created yet."),
                    padding=30,
                ),
                color=ft.colors.SURFACE,
                elevation=2,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=30,
    )
    charts_page = ft.Container(
        charts_content,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(0, 30),
        bgcolor=ft.colors.ON_INVERSE_SURFACE,
    )

    setup_content = gui.create_setup_content(
        page,
        results_content,
        charts_content,
        data,
    )
    setup_page = ft.Container(
        content=setup_content,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(0, 30),
        bgcolor=ft.colors.ON_INVERSE_SURFACE,
    )

    page_tabs = ft.Tabs(
        tabs=[
            ft.Tab(
                text="Setup",
                icon=ft.icons.EDIT_ROUNDED,
                content=setup_page,
            ),
            ft.Tab(
                text="Routes",
                icon=ft.icons.ROUTE_ROUNDED,
                content=results_page,
            ),
            ft.Tab(
                text="Charts",
                icon=ft.icons.BAR_CHART_ROUNDED,
                content=charts_page,
            ),
        ],
        expand=True,
        animation_duration=200,
    )

    page.title = "Deliver Route Planner"
    page.window.width = 1280
    page.window.height = 720
    page.window.center()
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(page_tabs)


if __name__ == "__main__":
    ft.app(main)

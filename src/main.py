import flet as ft

from delivery_route_planner import gui, models


def main(page: ft.Page) -> None:

    data = models.DataModel.create_with_defaults()

    results_content = ft.Column(
        [
            ft.Text("Solution has not been created yet."),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    results_page = ft.Container(
        results_content,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(0, 20),
    )

    charts_content = ft.Column(
        [
            ft.Text("Solution has not been created yet."),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    charts_page = ft.Container(
        charts_content,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(0, 20),
    )

    setup_content = gui.create_setup_content(page, results_content, charts_content, data)
    setup_page = ft.Container(
        content=setup_content,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(0, 20),
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
                icon=ft.icons.AUTO_GRAPH_ROUNDED,
                content=charts_page,
            ),
        ],
        expand=True,
        animation_duration=150,
    )

    page.title = "Deliver Route Planner"
    page.window.min_height = 450
    page.window.min_width = 400
    page.padding = 0

    page.add(page_tabs)


if __name__ == "__main__":
    ft.app(main)

from typing import Callable, NamedTuple

import flet as ft

from delivery_route_planner.models import models


class SolutionDialogs(NamedTuple):
    progress: ft.AlertDialog
    success: ft.AlertDialog
    failure: ft.AlertDialog


class NavigationManager:
    def __init__(
        self,
        page: ft.Page,
        data: models.DataModel,
        solution_callback: Callable,
    ) -> None:
        self.page = page
        self.data = data
        self.solution_callback = solution_callback
        self.views = {}
        self.view_names = []
        self.destinations = []
        self.navigation_rail = ft.NavigationRail()
        self.view_container = ft.Container(
            margin=ft.margin.only(0, 0, 24, 24),
            bgcolor=ft.colors.SURFACE,
            border_radius=15,
            border=ft.border.all(1, ft.colors.SURFACE_VARIANT),
            expand=True,
        )

    def render(self) -> ft.Row:
        return ft.Row(
            controls=[self.navigation_rail, self.view_container],
            expand=True,
            spacing=0,
        )

    def set_views(self, views: dict) -> None:
        self.views = views
        self.view_names = list(views.keys())
        self.view_container.content = self.views["setup"].render()
        self.navigation_rail = self._build_navigation_rail(views)

    def navigate_from_view_name(self, view_name: str) -> None:
        if view_name in self.views:
            self.view_container.content = self.views[view_name].render()
            self.page.update()

    def _navigate_from_selection(self, e: ft.ControlEvent) -> None:
        selected_view_name = self.view_names[e.control.selected_index]
        self.view_container.content = self.views[selected_view_name].render()
        self.page.update()

    def _build_navigation_rail(self, views: dict) -> ft.NavigationRail:
        solve_button = ft.FloatingActionButton(
            icon=ft.icons.AUTO_AWESOME_ROUNDED,
            bgcolor=ft.colors.PRIMARY,
            foreground_color=ft.colors.ON_PRIMARY,
            elevation=2,
            hover_elevation=4,
            on_click=self.start_or_tools_solver,
        )
        solve_button_container = ft.Container(
            ft.Column(
                controls=[solve_button, ft.Text("Solve")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )
        destinations = [
            ft.NavigationRailDestination(
                label=view.title,
                icon=view.icon,
                selected_icon=view.selected_icon,
                disabled=view.disabled,
            )
            for view in views.values()
        ]
        return ft.NavigationRail(
            leading=solve_button_container,
            destinations=destinations,
            selected_index=0,
            group_alignment=-0.2,
            label_type=ft.NavigationRailLabelType.SELECTED,
            indicator_color=ft.colors.INVERSE_PRIMARY,
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self._navigate_from_selection,
        )

    def start_or_tools_solver(self, _e: ft.ControlEvent) -> None:
        solver_dialogs = self._build_solution_dialogs()

        self.page.open(solver_dialogs.progress)
        solver_successful = self.solution_callback()

        self.page.close(solver_dialogs.progress)
        if solver_successful:
            self._enable_view("routes")
            self._enable_view("reports")
            self.page.open(solver_dialogs.success)
        else:
            self.page.open(solver_dialogs.failure)

        self.page.update()

    def _enable_view(self, name: str) -> None:
        for i, view_name in enumerate(self.view_names):
            if view_name == name and self.navigation_rail.destinations:
                self.navigation_rail.destinations[i].disabled = False
        self.page.update()

    def _build_solution_dialogs(self) -> SolutionDialogs:
        solver_progress_dialog = ft.AlertDialog(
            icon=ft.Icon(name=ft.icons.AUTO_AWESOME_ROUNDED),
            title=ft.Text("Please wait..."),
            content=ft.Column(
                [
                    ft.Text("Searching for routing solutions..."),
                    ft.ProgressBar(border_radius=5),
                ],
                tight=True,
            ),
            modal=True,
        )
        solver_success_dialog = ft.AlertDialog(
            icon=ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED),
            title=ft.Text("Solution found"),
            content=ft.Text(
                "New routes have been created.\n"
                "Please view them on the Routes and Reports pages.",
            ),
            actions=[
                ft.FilledTonalButton(
                    text="Okay",
                    on_click=lambda _: self.page.close(solver_success_dialog),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        solver_failure_dialog = ft.AlertDialog(
            icon=ft.Icon(name=ft.icons.ERROR_OUTLINE_ROUNDED, color=ft.colors.ERROR),
            title=ft.Text("Solution not found", color=ft.colors.ERROR),
            content=ft.Text(
                "Routes could not be created.\nPlease adjust settings and try again.",
            ),
            actions=[
                ft.FilledTonalButton(
                    text="Okay",
                    on_click=lambda _: self.page.close(solver_failure_dialog),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return SolutionDialogs(
            solver_progress_dialog,
            solver_success_dialog,
            solver_failure_dialog,
        )

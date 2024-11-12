from __future__ import annotations

from datetime import time

import flet as ft

from delivery_route_planner.components.view_base import ViewBase


class SetupView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = ViewBase(page)
        self.title = "Setup"
        self.icon = ft.icons.EDIT_OUTLINED
        self.selected_icon = ft.icons.EDIT_ROUNDED
        self.disabled = False

        self.routing_scenario_controls = self.create_routing_scenario_controls()
        self.first_solution_controls = self.create_first_solution_controls()
        self.search_settings_controls = self.create_search_settings_controls()


    def render(self) -> ft.Container:
        self.view.title.value = self.title
        self.view.action_button.text = "Reset defaults"
        self.view.action_button.icon = ft.icons.REFRESH_ROUNDED

        self.view.body.controls = [
            self.routing_scenario_controls,
            ft.Divider(),
            self.first_solution_controls,
            ft.Divider(),
            self.search_settings_controls,
        ]

        return self.view.render()

    def create_routing_scenario_controls(self) -> ft.Column:
        heading = ft.ListTile(
            leading=ft.Icon(ft.icons.CHECKLIST_ROUNDED),
            title=ft.Text("Routing scenario"),
            subtitle=ft.Text(
                "Requirements that must be met by routing solutions",
            ),
        )
        first_row_selections = ft.Row(
            [
                ft.Chip(
                    label=ft.Text("Vehicle carry capacities"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    label=ft.Text("Delivery deadlines"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    label=ft.Text("Shipping delays"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    label=ft.Text("Vehicle-specified deliveries"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    label=ft.Text("Keep bundled packages together"),
                    on_select=lambda _: _,
                ),
            ],
            wrap=True,
        )

        start_time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick the earliest time vehicles may begin.",
            value=time(8),
        )
        end_time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick the latest time vehicles must finish.",
            value=time(18),
        )

        second_row_selections = ft.Row(
            [
                ft.FilledTonalButton(
                    text="Start time: 8:00 AM",
                    icon=ft.icons.ACCESS_TIME_ROUNDED,
                    on_click=lambda _: self.page.open(start_time_picker),
                ),
                ft.FilledTonalButton(
                    text="End time: 6:00 PM",
                    icon=ft.icons.ACCESS_TIME_ROUNDED,
                    on_click=lambda _: self.page.open(end_time_picker),
                ),
                ft.SegmentedButton(
                    on_change=lambda _: _,
                    selected={"Shortest mileage"},
                    allow_multiple_selection=False,
                    show_selected_icon=True,
                    segments=[
                        ft.Segment(
                            value="Shortest mileage",
                            label=ft.Text("Shortest mileage"),
                        ),
                        ft.Segment(
                            value="Earliest deliveries",
                            label=ft.Text("Earliest deliveries"),
                        ),
                    ],
                ),
            ],
            wrap=True,
        )

        return ft.Column(
            [
                heading,
                first_row_selections,
                ft.Container(height=5),
                second_row_selections,
            ],
        )

    def create_first_solution_controls(self) -> ft.Column:

        first_solution_controls = ft.Column(
            [
                ft.ListTile(
                    leading=ft.Icon(ft.icons.ALT_ROUTE_ROUNDED),
                    title=ft.Text("First solution strategy"),
                    subtitle=ft.Text(
                        "Algorithms for finding an initial routing solution"
                    ),
                    trailing=ft.TextButton(
                        text="Learn more", icon=ft.icons.LINK_ROUNDED
                    ),
                ),
            ],
        )

        self.first_solution_strategies = self.create_first_solution_strategies()
        first_solution_controls.controls.extend(self.first_solution_strategies)

        return first_solution_controls

    def create_first_solution_strategies(self) -> list[ft.Chip]:

        automatic_chip = ft.Chip(
            label=ft.ListTile(
                leading=ft.Icon(ft.icons.CHECK_ROUNDED, visible=False),
                title=ft.Text("Automatic"),
                subtitle=ft.Text(
                    "Lets the solver detect which strategy to use according to the model being solved."
                ),
            ),
            on_select=self.on_select_fss,
            expand=True,
            padding=0,
            label_padding=0,
            show_checkmark=False,
        )
        global_cheapest_arc_chip = ft.Chip(
            label=ft.ListTile(
                leading=ft.Icon(ft.icons.CHECK_ROUNDED, visible=False),
                title=ft.Text("Global cheapest arc"),
                subtitle=ft.Text(
                    "Iteratively connect two nodes which produce the cheapest route segment."
                ),
            ),
            on_select=self.on_select_fss,
            expand=True,
            padding=0,
            label_padding=0,
            show_checkmark=False,
        )
        local_cheapest_arc_chip = ft.Chip(
            label=ft.ListTile(
                leading=ft.Icon(ft.icons.CHECK_ROUNDED, visible=False),
                title=ft.Text("Local cheapest arc"),
                subtitle=ft.Text(
                    "Select the first node with an unbound successor and connect it to the node which produces the cheapest route segment."
                ),
                trailing=ft.Text(
                    "Recommended!",
                    theme_style=ft.TextThemeStyle.LABEL_LARGE,
                    weight=ft.FontWeight.W_600,
                    color=ft.colors.SECONDARY,
                ),
            ),
            on_select=self.on_select_fss,
            expand=True,
            padding=0,
            label_padding=0,
            show_checkmark=False,
        )

        return [
            automatic_chip,
            global_cheapest_arc_chip,
            local_cheapest_arc_chip,
        ]

    def on_select_fss(self, e: ft.ControlEvent) -> None:
        if e.control.selected:
            e.control.label.leading.visible = True
        else:
            e.control.label.leading.visible = False
        for first_solution_strategy in self.first_solution_strategies:
            if first_solution_strategy is not e.control:
                first_solution_strategy.selected = False
                first_solution_strategy.label.leading.visible = False
        self.page.update()

    def create_search_settings_controls(self) -> ft.Column:

        heading = ft.ListTile(
            leading=ft.Icon(ft.icons.DISPLAY_SETTINGS_ROUNDED),
            title=ft.Text("Search limits"),
            subtitle=ft.Text(
                "Vehicle routing problems are computationally intractable. Limits are set to ensure the solver does not run endlessly."
            ),
        )

        self.time_limit_callout = ft.Text(
            "120 seconds",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
        )

        time_limit_card = ft.Card(
            ft.Container(
                ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("Time limit"),
                            subtitle=ft.Text(
                                "Longer searches will yield better results.\nAt least 120 seconds recommended."
                            ),
                            trailing=self.time_limit_callout,
                        ),
                        ft.Slider(
                            value=120,
                            min=30,
                            max=600,
                            divisions=19,
                            label=" {value} seconds ",
                            on_change=self.time_limit_change,
                        ),
                    ],
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            color=ft.colors.ON_INVERSE_SURFACE,
            elevation=2,
            width=500,
        )

        solution_limit_card = ft.Card(
            ft.Container(
                ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text("Solution limit"),
                            subtitle=ft.Text(
                                "Solutions are iterated very rapidly.\nAt least 1000 solutions recommended."
                            ),
                            trailing=ft.Text(
                                "2000 solutions",
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            ),
                        ),
                        ft.Slider(
                            value=2000,
                            min=250,
                            max=5000,
                            divisions=19,
                            label=" {value} solutions ",
                        ),
                    ],
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            color=ft.colors.ON_INVERSE_SURFACE,
            elevation=2,
            width=500,
        )

        return ft.Column(
            [
                heading,
                ft.Row(
                    [
                        time_limit_card,
                        solution_limit_card,
                    ],
                    wrap=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
        )

    def time_limit_change(self, e: ft.ControlEvent) -> None:
        value = int(e.control.value)
        self.time_limit_callout.value = f"{value} seconds"
        if value < 120:
            self.time_limit_callout.color = ft.colors.ERROR
            e.control.active_color = ft.colors.ERROR
        else:
            self.time_limit_callout.color = None
            e.control.active_color = None
        self.page.update()

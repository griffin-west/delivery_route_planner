from __future__ import annotations

import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner.models import models

TIME_LIMIT_WARNING_THRESHOLD = 60
SOLUTION_LIMIT_WARNING_THRESHOLD = 1000


class SetupView:
    def __init__(self, page: ft.Page, data: models.DataModel) -> None:
        self.page = page
        self.data = data

        self.title = "Setup"
        self.icon = ft.icons.EDIT_OUTLINED
        self.selected_icon = ft.icons.EDIT_ROUNDED
        self.disabled = False

        self.start_time_card = self.create_start_time_card()
        self.time_limit_card = self.create_time_limit_card()
        self.solution_limit_card = self.create_solution_limit_card()
        self.search_logging_card = self.create_search_logging_card()
        self.first_solution_card = self.create_first_solution_strategy_card()
        self.metaheuristic_card = self.create_local_search_metaheuristic_card()
        self.requirements_card = self.create_requirements_card()

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        reset_button = ft.FilledTonalButton(
            "Restore defaults",
            ft.icons.RESTORE_ROUNDED,
        )

        header = ft.Container(
            ft.Row(
                [title, reset_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )

        self.vehicles_card = self.create_vehicles_card()
        self.packages_card = self.create_packages_card()

        settings_row = ft.Container(
            ft.ResponsiveRow(
                [
                    self.vehicles_card,
                    self.packages_card,
                    self.start_time_card,
                    self.time_limit_card,
                    self.solution_limit_card,
                    self.search_logging_card,
                ],
                spacing=30,
                run_spacing=30,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.only(30, 0, 30, 30),
        )
        algorithms_row = ft.Container(
            ft.ResponsiveRow(
                [
                    self.first_solution_card,
                    self.metaheuristic_card,
                    self.requirements_card,
                ],
                spacing=30,
                run_spacing=30,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.only(30, 0, 30, 30),
        )
        body = ft.Column(
            controls=[
                settings_row,
                algorithms_row,
            ],
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
        return ft.Column(
            [header, body],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def create_vehicles_card(self) -> ft.Card:
        self.vehicles_callout = ft.Text(
            str(len(self.data.vehicles)),
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        vehicles_header = ft.ListTile(
            leading=ft.Icon(ft.icons.LOCAL_SHIPPING_OUTLINED),
            title=ft.Text("Vehicles in use"),
            subtitle=ft.Text(
                "Use the Vehicles page to view, modify, or add new vehicles.",
            ),
            trailing=self.vehicles_callout,
        )
        vehicles_disclaimer = ft.Container(
            ft.Text("*Work in progress.\nVehicles cannot be modified at this time."),
            padding=ft.padding.only(20, 0, 20, 10),
        )
        return SettingsCard(
            ft.Column(
                [
                    vehicles_header,
                    vehicles_disclaimer,
                ],
            ),
        )

    def create_packages_card(self) -> ft.Card:
        self.packages_callout = ft.Text(
            str(len(self.data.packages)),
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        packages_header = ft.ListTile(
            leading=ft.Icon(ft.icons.INVENTORY_2_OUTLINED),
            title=ft.Text("Packages to deliver"),
            subtitle=ft.Text(
                "Use the Packages page to view, modify, or add new packages.",
            ),
            trailing=self.packages_callout,
        )
        packages_disclaimer = ft.Container(
            ft.Text("*Work in progress.\nPackages cannot be modified at this time."),
            padding=ft.padding.only(20, 0, 20, 10),
        )
        return SettingsCard(
            ft.Column(
                [
                    packages_header,
                    packages_disclaimer,
                ],
            ),
        )

    def create_start_time_card(self) -> ft.Card:

        def _start_time_change(_e: ft.ControlEvent) -> None:
            def _update_time(e: ft.ControlEvent) -> None:
                self.data.scenario.day_start = models.RoutingTime.from_time(
                    e.control.value,
                )
                start_time_callout.value = self.data.scenario.day_start.short_str
                self.page.update()

            time_picker = ft.TimePicker(
                confirm_text="Confirm",
                error_invalid_text="Time out of range",
                help_text="Pick the earliest time deliveries may begin.",
                value=self.data.scenario.day_start.time,
                on_change=_update_time,
            )
            self.page.open(time_picker)

        start_time_callout = ft.Text(
            self.data.scenario.day_start.short_str,
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        start_time_header = ft.ListTile(
            leading=ft.Icon(ft.icons.ACCESS_TIME_ROUNDED),
            title=ft.Text("Day start time"),
            subtitle=ft.Text(
                "This is the earliest time deliveries may begin.",
            ),
            trailing=start_time_callout,
        )
        start_time_button = ft.Container(
            ft.ElevatedButton(
                text="Select new time",
                on_click=_start_time_change,
            ),
            padding=ft.padding.only(0, 0, 20, 10),
        )
        return SettingsCard(
            ft.Column(
                [
                    start_time_header,
                    start_time_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.END,
            ),
        )

    def create_time_limit_card(self) -> ft.Card:

        def time_limit_change(e: ft.ControlEvent) -> None:
            value = int(e.control.value)
            time_limit_callout.value = f"{value} seconds"
            self.data.settings.solver_time_limit_seconds = value
            if value < TIME_LIMIT_WARNING_THRESHOLD:
                time_limit_callout.color = ft.colors.ERROR
                e.control.active_color = ft.colors.ERROR
            else:
                time_limit_callout.color = None
                e.control.active_color = None
            self.page.update()

        time_limit_callout = ft.Text(
            f"{self.data.settings.solver_time_limit_seconds} seconds",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        time_limit_header = ft.ListTile(
            leading=ft.Icon(ft.icons.TIMER_OUTLINED),
            title=ft.Text("Time limit"),
            subtitle=ft.Text(
                "Longer searches will yield better results.",
            ),
            trailing=time_limit_callout,
        )
        time_limit_slider = ft.Slider(
            value=self.data.settings.solver_time_limit_seconds,
            min=15,
            max=300,
            divisions=19,
            label=" {value} seconds ",
            inactive_color=ft.colors.OUTLINE_VARIANT,
            on_change=time_limit_change,
        )
        return SettingsCard(
            ft.Column(
                [
                    time_limit_header,
                    time_limit_slider,
                ],
            ),
        )

    def create_solution_limit_card(self) -> ft.Card:

        def solution_limit_change(e: ft.ControlEvent) -> None:
            value = int(e.control.value)
            solution_limit_callout.value = f"{value} solutions"
            self.data.settings.solver_solution_limit = value
            if value < SOLUTION_LIMIT_WARNING_THRESHOLD:
                solution_limit_callout.color = ft.colors.ERROR
                e.control.active_color = ft.colors.ERROR
            else:
                solution_limit_callout.color = None
                e.control.active_color = None
            self.page.update()

        solution_limit_callout = ft.Text(
            f"{self.data.settings.solver_solution_limit} solutions",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        solution_limit_header = ft.ListTile(
            leading=ft.Icon(ft.icons.REFRESH_ROUNDED),
            title=ft.Text("Solution limit"),
            subtitle=ft.Text(
                "More iterations will yield better results.",
            ),
            trailing=solution_limit_callout,
        )
        solution_limit_slider = ft.Slider(
            value=self.data.settings.solver_solution_limit,
            min=250,
            max=5000,
            divisions=19,
            label=" {value} solutions ",
            inactive_color=ft.colors.OUTLINE_VARIANT,
            on_change=solution_limit_change,
        )
        return SettingsCard(
            ft.Column(
                [
                    solution_limit_header,
                    solution_limit_slider,
                ],
            ),
        )

    def create_search_logging_card(self) -> ft.Card:

        def logging_switch_change(e: ft.ControlEvent) -> None:
            self.data.settings.use_search_logging = e.control.value

        logging_header = ft.ListTile(
            leading=ft.Icon(ft.icons.TERMINAL_ROUNDED),
            title=ft.Text("Search logging"),
            subtitle=ft.Text(
                "Enables detailed logging from OR-Tools. "
                "Displays as STDOUT in the terminal.",
            ),
        )
        logging_switch = ft.Container(
            ft.Switch(
                value=self.data.settings.use_search_logging,
                on_change=logging_switch_change,
            ),
            padding=ft.padding.only(0, 0, 20, 10),
        )
        return SettingsCard(
            ft.Column(
                [
                    logging_header,
                    logging_switch,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.END,
            ),
        )

    def create_first_solution_strategy_card(self) -> ft.Card:

        def first_solution_change(_e: ft.ControlEvent) -> None:
            if first_solution_strategy_radio_group.value:
                self.data.settings.first_solution_strategy = getattr(
                    FirstSolutionStrategy,
                    first_solution_strategy_radio_group.value,
                )

        first_solution_strategy_header = ft.ListTile(
            leading=ft.Icon(ft.icons.FORK_LEFT_ROUNDED),
            title=ft.Text("First solution strategy"),
            subtitle=ft.Text("Select the algorithm used to find an initial solution."),
        )
        first_solution_strategy_radio_group = ft.RadioGroup(
            value="LOCAL_CHEAPEST_INSERTION",
            on_change=first_solution_change,
            content=ft.Column(
                [
                    first_solution_strategy_header,
                    ft.ListTile(
                        title=ft.Radio(
                            value="BEST_INSERTION",
                            label="Best Insertion",
                        ),
                        subtitle=ft.Text(
                            "Iteratively build a solution by inserting the cheapest "
                            "node at its cheapest position; the cost of insertion is "
                            "based on the global cost function of the routing model.",
                        ),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="PARALLEL_CHEAPEST_INSERTION",
                            label="Parallel Cheapest Insertion",
                        ),
                        subtitle=ft.Text(
                            "Iteratively build a solution by inserting the cheapest "
                            "node at its cheapest position; the cost of insertion is "
                            "based on the arc cost function. Is faster than "
                            "'Best Insertion'.",
                        ),
                    ),
                    ft.ListTile(
                        title=ft.Row(
                            [
                                ft.Radio(
                                    value="LOCAL_CHEAPEST_INSERTION",
                                    label="Local Cheapest Insertion",
                                ),
                                ft.Icon(
                                    ft.icons.STAR_RATE_ROUNDED,
                                    color=ft.colors.PRIMARY,
                                ),
                            ],
                        ),
                        subtitle=ft.Text(
                            "Iteratively build a solution by inserting each node at "
                            "its cheapest position; the cost of insertion is based on "
                            "the arc cost function. Differs from 'Parallel Cheapest "
                            "Insertion' by the node selected for insertion; here nodes "
                            "are considered in their order of creation. Is faster than "
                            "'Parallel Cheapest Insertion'.",
                        ),
                    ),
                ],
            ),
        )
        return SettingsCard(first_solution_strategy_radio_group)

    def create_local_search_metaheuristic_card(self) -> ft.Card:

        def local_search_metaheuristic_change(_e: ft.ControlEvent) -> None:
            if local_search_metaheuristic_radio_group.value:
                self.data.settings.local_search_metaheuristic = getattr(
                    LocalSearchMetaheuristic,
                    local_search_metaheuristic_radio_group.value,
                )

        local_search_metaheuristic_header = ft.ListTile(
            leading=ft.Icon(ft.icons.HUB_OUTLINED),
            title=ft.Text("Local search metaheuristic"),
            subtitle=ft.Text(
                "Select the advanced algorithm used "
                "to further optimize the initial solution.",
            ),
        )
        local_search_metaheuristic_radio_group = ft.RadioGroup(
            value="GUIDED_LOCAL_SEARCH",
            on_change=local_search_metaheuristic_change,
            content=ft.Column(
                [
                    local_search_metaheuristic_header,
                    ft.ListTile(
                        title=ft.Radio(
                            value="GREEDY_DESCENT",
                            label="Greedy Descent",
                        ),
                        subtitle=ft.Text(
                            "Accepts improving (cost-reducing) local search neighbors "
                            "until a local minimum is reached.",
                        ),
                    ),
                    ft.ListTile(
                        title=ft.Row(
                            [
                                ft.Radio(
                                    value="GUIDED_LOCAL_SEARCH",
                                    label="Guided Local Search",
                                ),
                                ft.Icon(
                                    ft.icons.STAR_RATE_ROUNDED,
                                    color=ft.colors.PRIMARY,
                                ),
                            ],
                        ),
                        subtitle=ft.Text(
                            "Uses guided local search to escape local minima. "
                            "This is generally the most efficient metaheuristic "
                            "for vehicle routing.",
                        ),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="SIMULATED_ANNEALING",
                            label="Simulated Annealing",
                        ),
                        subtitle=ft.Text(
                            "Uses simulated annealing to escape local minima.",
                        ),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="TABU_SEARCH",
                            label="Tabu Search",
                        ),
                        subtitle=ft.Text("Uses tabu search to escape local minima."),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="GENERIC_TABU_SEARCH",
                            label="Generic Tabu Search",
                        ),
                        subtitle=ft.Text(
                            "Uses tabu search on the objective value of solution to "
                            "escape local minima.",
                        ),
                    ),
                ],
            ),
        )
        return SettingsCard(local_search_metaheuristic_radio_group)

    def create_requirements_card(self) -> ft.Card:
        requirements_header = ft.ListTile(
            leading=ft.Icon(ft.icons.CHECKLIST_ROUNDED),
            title=ft.Text("Solution requirements"),
            subtitle=ft.Text(
                "Select which constraints must be respected by the solver.",
            ),
        )
        capacity_checkbox = ft.ListTile(
            title=ft.Checkbox(label="Vehicle capacities", value=True, disabled=True),
            subtitle=ft.Text(
                "Vehicles may only carry a maximum number of packages at once.",
            ),
        )
        availability_checkbox = ft.ListTile(
            title=ft.Checkbox(label="Shipping delays", value=True, disabled=True),
            subtitle=ft.Text(
                "Packages cannot leave the Depot until their availability time.",
            ),
        )
        deadlines_checkbox = ft.ListTile(
            title=ft.Checkbox(label="Delivery deadlines", value=True, disabled=True),
            subtitle=ft.Text(
                "Packages must be devliered before their delivery deadline.",
            ),
        )
        package_vehicle_checkbox = ft.ListTile(
            title=ft.Checkbox(
                label="Package-vehicle requirements",
                value=True,
                disabled=True,
            ),
            subtitle=ft.Text(
                "Packages must be delivered by their specified vehicle.",
            ),
        )
        linked_packages_checkbox = ft.ListTile(
            title=ft.Checkbox(label="Linked packages", value=True, disabled=True),
            subtitle=ft.Text(
                "Packages that are linked together must be "
                "delivered by the same vehicle.",
            ),
        )
        requirements_toggles = ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "*Work in progress.\n "
                        "These options are not yet user-customizable.",
                    ),
                    capacity_checkbox,
                    availability_checkbox,
                    deadlines_checkbox,
                    package_vehicle_checkbox,
                    linked_packages_checkbox,
                ],
            ),
            padding=ft.padding.only(10, 0, 10, 10),
        )

        return SettingsCard(
            ft.Column(
                [
                    requirements_header,
                    requirements_toggles,
                ],
            ),
        )


class SettingsCard(ft.Card):
    def __init__(self, content: ft.Control) -> None:
        super().__init__()
        self.content = ft.Container(content, padding=10)
        self.variant = ft.CardVariant.FILLED
        self.col = {"sm": 12, "md": 6, "xxl": 4}
        self.animate_size = ft.Animation(300, ft.AnimationCurve.EASE_OUT_CIRC)

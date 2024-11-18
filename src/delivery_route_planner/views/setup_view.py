import flet as ft

from delivery_route_planner.models import models

MINIMUM_SECONDS_RECOMMENDED = 60
MINIMUM_SOLUTIONS_RECOMMENDED = 1000


class SetupView:
    def __init__(
        self,
        page: ft.Page,
        data: models.DataModel,
        settings: models.SearchSettings,
    ) -> None:
        self.page = page
        self.data = data
        self.settings = settings

        self.title = "Setup"
        self.icon = ft.icons.EDIT_OUTLINED
        self.selected_icon = ft.icons.EDIT_ROUNDED
        self.disabled = False

        self.first_solution_card = self.create_first_solution_strategy_card()
        self.metaheuristic_card = self.create_local_search_metaheuristic_card()
        self.start_time_card = self.create_start_time_card()
        self.time_limit_card = self.create_time_limit_card()
        self.solution_limit_card = self.create_solution_limit_card()
        self.search_logging_card = self.create_search_logging_card()
        self.vehicles_card = self.create_vehicles_card()
        self.packages_card = self.create_packages_card()

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        reset_button = ft.FilledTonalButton("Reset defaults", ft.icons.UNDO_ROUNDED)

        header = ft.Container(
            ft.Row(
                [title, reset_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        settings_row = ft.Container(
            ft.Row(
                [
                    self.vehicles_card,
                    self.packages_card,
                    self.start_time_card,
                    self.time_limit_card,
                    self.solution_limit_card,
                    self.search_logging_card,
                ],
                wrap=True,
                spacing=30,
                run_spacing=30,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.only(30, 0, 30, 30),
        )
        algorithms_row = ft.Container(
            ft.Row(
                [
                    self.first_solution_card,
                    self.metaheuristic_card,
                ],
                wrap=True,
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

    def create_first_solution_strategy_card(self) -> ft.Card:
        first_solution_strategy_header = ft.ListTile(
            leading=ft.Icon(ft.icons.SWITCH_ACCESS_SHORTCUT_ROUNDED),
            title=ft.Text("First solution strategy"),
            subtitle=ft.Text("Select an algorithm used to find an initial solution."),
        )
        self.first_solution_strategy_radio_group = ft.RadioGroup(
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
            value="LOCAL_CHEAPEST_INSERTION",
            on_change=lambda _: _,
        )
        return ft.Card(
            ft.Container(
                self.first_solution_strategy_radio_group,
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def create_local_search_metaheuristic_card(self) -> ft.Card:
        local_search_metaheuristic_header = ft.ListTile(
            leading=ft.Icon(ft.icons.HUB_OUTLINED),
            title=ft.Text("Local search metaheuristic"),
            subtitle=ft.Text(
                "Select a more advanced algorithm used "
                "to optimize the initial solution.",
            ),
        )
        self.local_search_metaheuristic_radio_group = ft.RadioGroup(
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
            value="GUIDED_LOCAL_SEARCH",
            on_change=lambda _: _,
        )
        return ft.Card(
            ft.Container(
                self.local_search_metaheuristic_radio_group,
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def create_time_limit_card(self) -> ft.Card:
        self.time_limit_callout = ft.Text(
            "120 seconds",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        time_limit_header = ft.ListTile(
            leading=ft.Icon(ft.icons.TIMER_OUTLINED),
            title=ft.Text("Time limit"),
            subtitle=ft.Text(
                "Longer searches will yield better results.",
            ),
            trailing=self.time_limit_callout,
        )
        time_limit_slider = ft.Slider(
            value=120,
            min=15,
            max=300,
            divisions=19,
            label=" {value} seconds ",
            inactive_color=ft.colors.OUTLINE_VARIANT,
            on_change=self.time_limit_change,
        )
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        time_limit_header,
                        time_limit_slider,
                    ],
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def time_limit_change(self, e: ft.ControlEvent) -> None:
        value = int(e.control.value)
        self.time_limit_callout.value = f"{value} seconds"
        if value < MINIMUM_SECONDS_RECOMMENDED:
            self.time_limit_callout.color = ft.colors.ERROR
            e.control.active_color = ft.colors.ERROR
        else:
            self.time_limit_callout.color = None
            e.control.active_color = None
        self.page.update()

    def create_solution_limit_card(self) -> ft.Card:
        self.solution_limit_callout = ft.Text(
            "2000",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        solution_limit_header = ft.ListTile(
            leading=ft.Icon(ft.icons.REFRESH_ROUNDED),
            title=ft.Text("Solution iteration limit"),
            subtitle=ft.Text(
                "Solutions are iterated very rapidly " "as optimized routes are found.",
            ),
            trailing=self.solution_limit_callout,
        )
        solution_limit_slider = ft.Slider(
            value=2000,
            min=250,
            max=5000,
            divisions=19,
            label=" {value} solutions ",
            inactive_color=ft.colors.OUTLINE_VARIANT,
            on_change=self.solution_limit_change,
        )
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        solution_limit_header,
                        solution_limit_slider,
                    ],
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def solution_limit_change(self, e: ft.ControlEvent) -> None:
        value = int(e.control.value)
        self.solution_limit_callout.value = f"{value}"
        if value < MINIMUM_SOLUTIONS_RECOMMENDED:
            self.solution_limit_callout.color = ft.colors.ERROR
            e.control.active_color = ft.colors.ERROR
        else:
            self.solution_limit_callout.color = None
            e.control.active_color = None
        self.page.update()

    def create_start_time_card(self) -> ft.Card:
        self.start_time_callout = ft.Text(
            "8:00 AM",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        start_time_header = ft.ListTile(
            leading=ft.Icon(ft.icons.ACCESS_TIME_ROUNDED),
            title=ft.Text("Day start time"),
            subtitle=ft.Text(
                "This is the earliest time deliveries may begin.",
            ),
            trailing=self.start_time_callout,
        )
        start_time_button = ft.Container(
            ft.ElevatedButton(
                text="Select new time",
            ),
            padding=ft.padding.only(0, 0, 20, 10),
        )
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        start_time_header,
                        start_time_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def create_search_logging_card(self) -> ft.Card:
        logging_header = ft.ListTile(
            leading=ft.Icon(ft.icons.TERMINAL_ROUNDED),
            title=ft.Text("Search logging"),
            subtitle=ft.Text(
                "Enables detailed logging from OR-Tools. "
                "Displays as STDOUT in the terminal.",
            ),
        )
        logging_switch = ft.Container(
            ft.Switch(value=True),
            padding=ft.padding.only(0, 0, 20, 10),
        )
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        logging_header,
                        logging_switch,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def create_vehicles_card(self) -> ft.Card:
        self.vehicles_callout = ft.Text(
            "2",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        vehicles_header = ft.ListTile(
            leading=ft.Icon(ft.icons.LOCAL_SHIPPING_OUTLINED),
            title=ft.Text("Vehicles in use"),
            subtitle=ft.Text(
                "Use the Vehicles page to view, modify, or add " "new vehicles.",
            ),
            trailing=self.vehicles_callout,
        )
        vehicles_disclaimer = ft.Container(
            ft.Text("*Work in progress.\nVehicles can only be added at this time."),
            padding=ft.padding.only(20, 0, 20, 10),
        )
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        vehicles_header,
                        vehicles_disclaimer,
                    ],
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

    def create_packages_card(self) -> ft.Card:
        self.packages_callout = ft.Text(
            "40",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        packages_header = ft.ListTile(
            leading=ft.Icon(ft.icons.INVENTORY_2_OUTLINED),
            title=ft.Text("Packages to deliver"),
            subtitle=ft.Text(
                "Use the Packages page to view, modify, or add " "new packages.",
            ),
            trailing=self.packages_callout,
        )
        packages_disclaimer = ft.Container(
            ft.Text("*Work in progress.\nPackages cannot be modified at this time."),
            padding=ft.padding.only(20, 0, 20, 10),
        )
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        packages_header,
                        packages_disclaimer,
                    ],
                ),
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
            width=400,
        )

import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner.models import models

MINIMUM_SECONDS_RECOMMENDED = 60
MINIMUM_SOLUTIONS_RECOMMENDED = 1000


class SetupView:
    def __init__(self, page: ft.Page, data: models.DataModel, settings: models.SearchSettings) -> None:
        self.page = page
        self.data = data
        self.settings = settings

        self.title = "Setup"
        self.icon = ft.icons.EDIT_OUTLINED
        self.selected_icon = ft.icons.EDIT_ROUNDED
        self.disabled = False

    def render(self) -> ft.Column:
        title = ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL)
        reset_button = ft.FilledTonalButton("Reset defaults", ft.icons.RESTART_ALT_ROUNDED)
        header = ft.Container(
            ft.Row(
                [title, reset_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=30,
        )
        body = ft.Column(
            controls=[
                ft.Container(
                    ft.Row(
                        [
                            self.create_time_limit_card(),
                            self.create_solution_limit_card(),
                        ],
                        wrap=True,
                        spacing=30,
                        run_spacing=30,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=ft.padding.only(30, 0, 30, 30),
                ),
                self.create_first_solution_strategy_card(),
                self.create_local_search_metaheuristic_card(),
            ],
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
        return ft.Column(
            [
                header,
                body,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def create_first_solution_strategy_card(self) -> ft.Container:
        first_solution_strategy_header = ft.ListTile(
            leading=ft.Icon(ft.icons.SWITCH_ACCESS_SHORTCUT_ROUNDED),
            title=ft.Text("First solution strategy"),
            subtitle=ft.Text("Choose an algorithm to find an initial solution."),
            trailing=ft.TextButton("Learn more", ft.icons.LINK_ROUNDED),
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
                        subtitle=ft.Text("Iteratively build a solution by inserting the cheapest node at its cheapest position; the cost of insertion is based on the global cost function of the routing model."),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="PARALLEL_CHEAPEST_INSERTION",
                            label="Parallel Cheapest Insertion",
                        ),
                        subtitle=ft.Text("Iteratively build a solution by inserting the cheapest node at its cheapest position; the cost of insertion is based on the arc cost function. Is faster than 'Best Insertion'."),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="LOCAL_CHEAPEST_INSERTION",
                            label="Local Cheapest Insertion",
                        ),
                        subtitle=ft.Text("Iteratively build a solution by inserting each node at its cheapest position; the cost of insertion is based on the arc cost function. Differs from 'Parallel Cheapest Insertion' by the node selected for insertion; here nodes are considered in their order of creation. Is faster than 'Parallel Cheapest Insertion'."),
                    ),
                ],
            ),
            on_change=lambda _: _,
        )
        first_solution_strategy_card = ft.Card(
            ft.Container(
                self.first_solution_strategy_radio_group,
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
        )
        return ft.Container(
            first_solution_strategy_card,
            padding=ft.padding.only(30, 0, 30, 30),
        )

    def create_local_search_metaheuristic_card(self) -> ft.Container:
        local_search_metaheuristic_header = ft.ListTile(
            leading=ft.Icon(ft.icons.HUB_OUTLINED),
            title=ft.Text("Local search metaheuristic"),
            subtitle=ft.Text("Choose an algorithm to optimize the initial solution."),
            trailing=ft.TextButton("Learn more", ft.icons.LINK_ROUNDED),
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
                        subtitle=ft.Text("Accepts improving (cost-reducing) local search neighbors until a local minimum is reached."),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="GUIDED_LOCAL_SEARCH",
                            label="Guided Local Search",
                        ),
                        subtitle=ft.Text("Uses guided local search to escape local minima. This is generally the most efficient metaheuristic for vehicle routing."),
                    ),
                    ft.ListTile(
                        title=ft.Radio(
                            value="SIMULATED_ANNEALING",
                            label="Simulated Annealing",
                        ),
                        subtitle=ft.Text("Uses simulated annealing to escape local minima."),
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
                        subtitle=ft.Text("Uses tabu search on the objective value of solution to escape local minima."),
                    ),
                ],
            ),
            on_change=lambda _: _,
        )
        local_search_metaheuristic_card = ft.Card(
            ft.Container(
                self.local_search_metaheuristic_radio_group,
                padding=10,
            ),
            variant=ft.CardVariant.FILLED,
        )
        return ft.Container(
            local_search_metaheuristic_card,
            padding=ft.padding.only(30, 0, 30, 30),
        )

    def create_time_limit_card(self) -> ft.Container:
        self.time_limit_callout = ft.Text(
            "120 seconds",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
        )
        time_limit_header = ft.ListTile(
            leading=ft.Icon(ft.icons.ACCESS_TIME_ROUNDED),
            title=ft.Text("Time limit"),
            subtitle=ft.Text(
                "Longer searches will yield better results.\nAt least 60 seconds recommended.",
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
        time_limit_card = ft.Card(
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
            width=500,
        )
        return ft.Container(
            content=time_limit_card,
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

    def create_solution_limit_card(self) -> ft.Container:
        self.solution_limit_callout = ft.Text(
            "2000 solutions",
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
        )
        solution_limit_header = ft.ListTile(
            leading=ft.Icon(ft.icons.REFRESH_ROUNDED),
            title=ft.Text("Solution iteration limit"),
            subtitle=ft.Text(
                "More iterations will yield better results.\nAt least 1000 solutions recommended.",
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
        solution_limit_card = ft.Card(
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
            width=500,
        )
        return ft.Container(
            content=solution_limit_card,
        )

    def solution_limit_change(self, e: ft.ControlEvent) -> None:
        value = int(e.control.value)
        self.solution_limit_callout.value = f"{value} solutions"
        if value < MINIMUM_SOLUTIONS_RECOMMENDED:
            self.solution_limit_callout.color = ft.colors.ERROR
            e.control.active_color = ft.colors.ERROR
        else:
            self.solution_limit_callout.color = None
            e.control.active_color = None
        self.page.update()

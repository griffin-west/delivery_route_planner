import flet as ft
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)

from delivery_route_planner import models, routing


def main(page: ft.Page) -> None:

    data = models.DataModel.with_defaults()
    scenario = models.RoutingScenario()
    settings = models.SearchSettings()

    def solve_button_clicked(e: ft.ControlEvent) -> None:

        if first_solution_strategy_dropdown.value:
            settings.first_solution_strategy = getattr(
                FirstSolutionStrategy, first_solution_strategy_dropdown.value,
            )

        if local_search_metaheuristic_dropdown.value:
            settings.local_search_metaheuristic = getattr(
                LocalSearchMetaheuristic, local_search_metaheuristic_dropdown.value,
            )

        if time_limit_slider.value:
            settings.solver_time_limit_seconds = int(time_limit_slider.value)

        solution = routing.solve_vehicle_routing_problem(data, scenario, settings)

        solution.print_solution() if solution else print("Solution not found.")

        page.update()

    solve_button = ft.FilledTonalButton(
        text="Solve",
        on_click=solve_button_clicked,
    )

    first_solution_strategy_dropdown = ft.Dropdown(
        label="First solution strategy",
        options=[
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_INSERTION",
                text="Local cheapest inserstion",
            ),
            ft.dropdown.Option(
                key="LOCAL_CHEAPEST_COST_INSERTION",
                text="Local cheapest cost insertion",
            ),
            ft.dropdown.Option(
                key="SEQUENTIAL_CHEAPEST_INSERTION",
                text="Sequential cheapest insertion",
            ),
            ft.dropdown.Option(
                key="PARALLEL_CHEAPEST_INSERTION",
                text="Parallel cheapest insertion",
            ),
            ft.dropdown.Option(
                key="BEST_INSERTION",
                text="Best insertion",
            ),
        ],
    )

    local_search_metaheuristic_dropdown = ft.Dropdown(
        label="Local search metaheuristic",
        options=[
            ft.dropdown.Option(
                key="SIMULATED_ANNEALING",
                text="Simulated annealing",
            ),
            ft.dropdown.Option(
                key="GUIDED_LOCAL_SEARCH",
                text="Guided local search",
            ),
            ft.dropdown.Option(
                key="GREEDY_DESCENT",
                text="Greedy descent",
            ),
            ft.dropdown.Option(
                key="TABU_SEARCH",
                text="Tabu search",
            ),
            ft.dropdown.Option(
                key="GENERIC_TABU_SEARCH",
                text="Generic tabu search",
            ),
        ],
    )

    time_limit_heading = ft.Text("Time limit in seconds:")
    time_limit_slider = ft.Slider(
        value=60, min=30, max=600, divisions=19, label="{value}",
    )

    page.add(
        first_solution_strategy_dropdown,
        local_search_metaheuristic_dropdown,
        time_limit_heading,
        time_limit_slider,
        solve_button,
    )


if __name__ == "__main__":
    ft.app(main)

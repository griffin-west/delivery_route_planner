import flet as ft

from delivery_route_planner.components.page_view import PageView


class SetupView:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.view = PageView(page)
        self.title = "Setup"
        self.icon = ft.icons.EDIT_OUTLINED
        self.selected_icon = ft.icons.EDIT_ROUNDED
        self.disabled = False

    def render(self) -> ft.Container:
        self.view.title.value = self.title
        self.view.action_button.text = "Reset defaults"
        self.view.action_button.icon = ft.icons.REFRESH_ROUNDED

        routing_scenario_selections = self.create_routing_scenario_selections()
        search_strategy_selections = self.create_search_strategy_selections()
        search_settings_selections = self.create_search_settings_selections()

        self.view.body.controls = [
            routing_scenario_selections,
            ft.Divider(),
            search_strategy_selections,
            ft.Divider(),
            search_settings_selections,
            ft.Divider(),
        ]

        return self.view.render()

    def create_routing_scenario_selections(self) -> ft.Column:
        heading = ft.ListTile(
            leading=ft.Icon(ft.icons.CHECKLIST_ROUNDED),
            title=ft.Text("Routing scenario"),
            subtitle=ft.Text(
                "Select the requirements that must be met by the routing solution.",
            ),
        )
        selections = ft.Row(
            [
                ft.Chip(
                    selected=True,
                    show_checkmark=True,
                    label=ft.Text("Vehicle carry capacities"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    selected=True,
                    show_checkmark=True,
                    label=ft.Text("Delivery deadlines"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    selected=True,
                    show_checkmark=True,
                    label=ft.Text("Shipping delays"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    selected=True,
                    show_checkmark=True,
                    label=ft.Text("Vehicle-specified deliveries"),
                    on_select=lambda _: _,
                ),
                ft.Chip(
                    selected=True,
                    show_checkmark=True,
                    label=ft.Text("Keep bundled packages together"),
                    on_select=lambda _: _,
                ),
            ],
            wrap=True,
        )
        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick the earliest time vehicles may leave the depot.",
        )
        day_start_time_button = ft.Container(
                ft.OutlinedButton(
                text="Day start time: 8:00 AM",
                icon=ft.icons.ACCESS_TIME_ROUNDED,
                on_click=lambda _: self.page.open(time_picker),
            ),
            padding=ft.padding.symmetric(10,0),
        )

        return ft.Column([heading, selections, day_start_time_button])

    def create_search_strategy_selections(self) -> ft.Column:
        heading = ft.ListTile(
            leading=ft.Icon(ft.icons.SEARCH_ROUNDED),
            title=ft.Text("Search strategies"),
            subtitle=ft.Text(
                "Select the algorithms to be used in the solution search.",
            ),
            trailing=ft.TextButton(text="Learn more", icon=ft.icons.LINK_ROUNDED),
        )
        first_solution_drop_down = ft.Dropdown(
            label="First solution strategy",
            helper_text="The algorithm used to find the first routing solution.",
            width=400,
            padding=ft.padding.symmetric(10, 5),
            filled=True,
            border_width=0,
            border_radius=10,
            icon_enabled_color=ft.colors.ON_SURFACE,
            icon_content=ft.Icon(ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED),
            fill_color=ft.colors.SURFACE_VARIANT,
            label_style=ft.TextStyle(color=ft.colors.ON_SURFACE),
            on_change=self.show_first_solution_info_card,
            options=[
                ft.dropdown.Option("Local cheapest arc"),
                ft.dropdown.Option("Global cheapest arc"),
                ft.dropdown.Option("Path cheapest arc"),
                ft.dropdown.Option("Local cheapest insertion"),
                ft.dropdown.Option("Parallel cheapest insertion"),
                ft.dropdown.Option("Best insertion"),
                ft.dropdown.Option("First unbound min value"),
                ft.dropdown.Option("Christofides"),
                ft.dropdown.Option("Savings"),
                ft.dropdown.Option("Sweep"),
            ],
        )
        metaheuristic_dropdown = ft.Dropdown(
            label="Local search metaheuristic",
            helper_text="The algorithm used to iterate and improve solutions.",
            width=400,
            padding=ft.padding.symmetric(10, 5),
            filled=True,
            border_width=0,
            border_radius=10,
            icon_enabled_color=ft.colors.ON_SURFACE,
            icon_content=ft.Icon(ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED),
            fill_color=ft.colors.SURFACE_VARIANT,
            label_style=ft.TextStyle(color=ft.colors.ON_SURFACE),
            options=[
                ft.dropdown.Option("Guided local search"),
                ft.dropdown.Option("Simulated annealing"),
                ft.dropdown.Option("Greedy descent"),
                ft.dropdown.Option("Tabu search"),
                ft.dropdown.Option("Generic tabu search"),
            ],
        )
        optimization_dropdown = ft.Dropdown(
            label="Optimization focus",
            helper_text="Determines which solutions to prioritize.",
            width=400,
            padding=ft.padding.symmetric(10, 5),
            filled=True,
            border_width=0,
            border_radius=10,
            icon_enabled_color=ft.colors.ON_SURFACE,
            icon_content=ft.Icon(ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED),
            fill_color=ft.colors.SURFACE_VARIANT,
            label_style=ft.TextStyle(color=ft.colors.ON_SURFACE),
            options=[
                ft.dropdown.Option("Lowest total mileage"),
                ft.dropdown.Option("Earliest deliveries"),
            ],
        )
        self.first_solution_info_card = ft.Card(
            ft.ListTile(
                leading=ft.Icon(ft.icons.INFO_OUTLINE_ROUNDED),
                title=ft.Text("Path cheapest arc"),
                subtitle=ft.Text(
                    "Starting from a route 'start' node, connect it to the node which produces the cheapest route segment, then extend the route by iterating on the last node added to the route."
                ),
            ),
            variant=ft.CardVariant.FILLED,
            expand=True,
            color=ft.colors.SECONDARY_CONTAINER,
            visible=False,
        )

        return ft.Column(
            [
                heading,
                first_solution_drop_down, 
                self.first_solution_info_card,
                metaheuristic_dropdown,
                optimization_dropdown,
            ],
        )

    def show_first_solution_info_card(self, e: ft.ControlEvent) -> None:
        self.first_solution_info_card.visible = True
        self.page.update()

    def create_search_settings_selections(self) -> ft.Column:
        heading = ft.ListTile(
            leading=ft.Icon(ft.icons.DISPLAY_SETTINGS_ROUNDED),
            title=ft.Text("Search settings"),
            subtitle=ft.Text(
                "Adjust the settings to be used in the solution search.",
            ),
        )
        maximum_time_slider = ft.Column(
            [
                ft.Text("Maximum time allowed to search for solutions", theme_style=ft.TextThemeStyle.LABEL_LARGE),
                ft.Slider(
                    min=0, max=300, divisions=10, label="{value} seconds",
                ),
            ],
        )
        maximum_solutions_slider = ft.Column(
            [
                ft.Text("Maximum number of solutions generated during the search", theme_style=ft.TextThemeStyle.LABEL_LARGE),
                ft.Slider(
                    min=0, max=5000, divisions=20, label="{value} solutions",
                ),
            ],
        )
        maximum_vehicle_mileage_slider = ft.Column(
            [
                ft.Text("Maximum mileage allowed per vehicle", theme_style=ft.TextThemeStyle.LABEL_LARGE),
                ft.Slider(
                    min=0, max=200, divisions=20, label="{value} miles",
                ),
            ],
        )

        return ft.Column(
            [
                heading,
                maximum_time_slider,
                maximum_solutions_slider,
                maximum_vehicle_mileage_slider,
            ],
        )

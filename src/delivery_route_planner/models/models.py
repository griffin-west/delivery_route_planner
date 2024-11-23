from __future__ import annotations

import csv
import datetime
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, TypeAlias

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

FSS = routing_enums_pb2.FirstSolutionStrategy
LSM = routing_enums_pb2.LocalSearchMetaheuristic
ADDRESS_FILE = "src/delivery_route_planner/data/distance_matrix.csv"
PACKAGE_FILE = "src/delivery_route_planner/data/package_details.csv"
MILEAGE_SCALE_FACTOR = 10
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = SECONDS_PER_HOUR * 24

OrToolsEnum: TypeAlias = int
AddressDict: TypeAlias = dict[str, "Address"]
AddressMap: TypeAlias = dict[str, float]
VehicleDict: TypeAlias = dict[int, "Vehicle"]
PackageDict: TypeAlias = dict[int, "Package"]
CsvRow: TypeAlias = dict[str, str]


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    distance_map_miles: AddressMap

    @classmethod
    def from_csv(cls) -> AddressDict:
        with Path(ADDRESS_FILE).open(newline="", encoding="utf-8-sig") as file:
            return {
                row["Street"]: cls(
                    street=row.pop("Street"),
                    city=row.pop("City"),
                    state=row.pop("State"),
                    zip_code=row.pop("Zip Code"),
                    distance_map_miles={k: float(v) for k, v in row.items()},
                )
                for row in csv.DictReader(file)
            }


@dataclass
class TravelCostMap:
    cost_map: dict[str, dict[str, int]]

    @classmethod
    def create_from_addresses_with_transformer(
        cls,
        addresses: AddressDict,
        transform: Callable[[float], int],
    ) -> TravelCostMap:
        cost_map = {
            from_address: {
                to_address: transform(distance)
                for to_address, distance in address.distance_map_miles.items()
            }
            for from_address, address in addresses.items()
        }
        return cls(cost_map=cost_map)

    @classmethod
    def with_distance(cls, addresses: AddressDict) -> TravelCostMap:
        return cls.create_from_addresses_with_transformer(
            addresses,
            lambda distance: int(distance * MILEAGE_SCALE_FACTOR),
        )

    @classmethod
    def with_duration(cls, addresses: AddressDict, speed_mph: float) -> TravelCostMap:
        return cls.create_from_addresses_with_transformer(
            addresses,
            lambda distance: int(distance / speed_mph * SECONDS_PER_HOUR),
        )


@dataclass
class Vehicle:
    id: int
    speed_mph: float
    package_capacity: int
    duration_map: TravelCostMap

    @classmethod
    def with_shared_attributes(
        cls,
        vehicle_count: int,
        speed_mph: float,
        package_capacity: int,
        duration_map: TravelCostMap,
    ) -> VehicleDict:
        return {
            vehicle_id: cls(
                id=vehicle_id,
                speed_mph=speed_mph,
                package_capacity=package_capacity,
                duration_map=duration_map,
            )
            for vehicle_id in range(1, vehicle_count + 1)
        }

    @classmethod
    def add_to_fleet(
        cls,
        data: DataModel,
        vehicle_id: int,
        speed_mph: float,
        package_capacity: int,
    ) -> None:
        new_travel_map = TravelCostMap.with_duration(data.addresses, speed_mph)
        new_vehicle = cls(
            id=vehicle_id,
            speed_mph=speed_mph,
            package_capacity=package_capacity,
            duration_map=new_travel_map,
        )
        data.vehicles[vehicle_id] = new_vehicle

    @classmethod
    def find_max_vehicle_id(cls, vehicles: VehicleDict) -> int:
        max_vehicle_id = 0
        for vehicle in vehicles.values():
            max_vehicle_id = max(max_vehicle_id, vehicle.id)
        return max_vehicle_id

    @property
    def index(self) -> int:
        """OR-Tools uses 0-based indexing for all vehicle references."""
        return self.id - 1


@dataclass
class RoutingTime:
    _total_seconds: int

    def __str__(self) -> str:
        return self.time.strftime("%I:%M:%S %p").lstrip("0").lower()

    @classmethod
    def from_time(cls, t: datetime.time) -> RoutingTime:
        total_seconds = t.hour * SECONDS_PER_HOUR + t.minute * 60 + t.second
        return cls(total_seconds)

    @classmethod
    def from_seconds(cls, seconds: int) -> RoutingTime:
        return cls(seconds % SECONDS_PER_DAY)

    @classmethod
    def from_isoformat(cls, value: str) -> RoutingTime | None:
        try:
            return cls.from_time(datetime.time.fromisoformat(value))
        except (ValueError, TypeError):
            return None

    @property
    def time(self) -> datetime.time:
        hours = self._total_seconds // SECONDS_PER_HOUR
        minutes = (self._total_seconds % SECONDS_PER_HOUR) // 60
        seconds = self._total_seconds % 60
        return datetime.time(hours, minutes, seconds)

    @property
    def seconds(self) -> int:
        return self._total_seconds

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.combine(
            datetime.datetime.now(tz=datetime.UTC),
            self.time,
        )

    @property
    def short_str(self) -> str:
        return self.time.strftime("%I:%M %p").lstrip("0").lower()

    def duration_until(self, other: RoutingTime) -> int:
        return other.seconds - self.seconds

    def duration_after(self, other: RoutingTime) -> int:
        return self.seconds - other.seconds


@dataclass
class Package:
    id: int
    address: Address
    weight_kg: float | None = None
    shipping_availability: RoutingTime | None = None
    delivery_deadline: RoutingTime | None = None
    vehicle_requirement: Vehicle | None = None
    bundled_packages: list[Package] = field(default_factory=list)
    shipped_time: RoutingTime | None = None
    delivered_time: RoutingTime | None = None
    vehicle_used: Vehicle | None = None

    @classmethod
    def from_csv(cls, addresses: AddressDict, vehicles: VehicleDict) -> PackageDict:
        with Path(PACKAGE_FILE).open(newline="", encoding="utf-8-sig") as file:
            rows = list(csv.DictReader(file))
            packages = {
                int(row["id"]): cls.from_row(row, vehicles, addresses) for row in rows
            }
            for row in rows:
                cls.add_bundled_packages(row, packages)
        return packages

    @classmethod
    def from_row(
        cls,
        row: CsvRow,
        vehicles: VehicleDict,
        addresses: AddressDict,
    ) -> Package:
        vehicle_id = cls._convert_or_none(row["vehicle_requirement"], int)
        return cls(
            id=int(row["id"]),
            address=addresses[row["address"].strip()],
            weight_kg=cls._convert_or_none(row["weight_kg"], float),
            shipping_availability=RoutingTime.from_isoformat(row["availability"]),
            delivery_deadline=RoutingTime.from_isoformat(row["deadline"]),
            vehicle_requirement=vehicles[vehicle_id] if vehicle_id else None,
        )

    @classmethod
    def add_bundled_packages(cls, row: CsvRow, packages: PackageDict) -> None:
        bundled_ids = [
            cls._convert_or_none(bundled_id, int)
            for bundled_id in row["linked_packages"].split(",")
        ]
        packages[int(row["id"])].bundled_packages.extend(
            packages[bundled_id] for bundled_id in bundled_ids if bundled_id
        )

    @staticmethod
    def _convert_or_none(value: Any, convert_func: Callable[[str], Any]) -> Any | None:
        try:
            return convert_func(value.strip())
        except (ValueError, TypeError, AttributeError):
            return None

    @staticmethod
    def _find_node_index(
        package: Package,
        nodes: list[Node],
        kind: NodeKind,
    ) -> int | None:
        for index, node in enumerate(nodes):
            if node.package == package and node.kind == kind:
                return index
        return None

    @property
    def required_vehicle_index(self) -> int | None:
        return self.vehicle_requirement.id - 1 if self.vehicle_requirement else None

    def pickup_node_index(self, nodes: list[Node]) -> int | None:
        return self._find_node_index(self, nodes, NodeKind.PICKUP)

    def delivery_node_index(self, nodes: list[Node]) -> int | None:
        return self._find_node_index(self, nodes, NodeKind.DELIVERY)


class NodeKind(Enum):
    ORIGIN = ("Route Start/End", 0)
    PICKUP = ("Pickup", 1)
    DELIVERY = ("Delivery", -1)

    def __init__(self, description: str, capacity_impact: int) -> None:
        self.description = description
        self.capacity_impact = capacity_impact


@dataclass
class Node:
    kind: NodeKind
    address: str
    package: Package | None = None
    origin_id = 0

    @classmethod
    def from_packages(cls, packages: PackageDict) -> list[Node]:
        nodes: list[Node] = [cls(NodeKind.ORIGIN, "Depot")]
        for package in packages.values():
            nodes.append(cls(NodeKind.PICKUP, "Depot", package))
            nodes.append(cls(NodeKind.DELIVERY, package.address.street, package))
        return nodes


@dataclass
class Constraints:
    vehicle_capacities: bool = True
    shipping_availability: bool = True
    delivery_deadline: bool = True
    vehicle_requirement: bool = True
    bundled_packages: bool = True


class OptimizationType(Enum):
    MILEAGE = "Mileage"
    TIME = "Time"


@dataclass
class RoutingScenario:
    day_start: RoutingTime = field(
        default_factory=lambda: RoutingTime.from_time(datetime.time(8)),
    )
    day_end: RoutingTime = field(
        default_factory=lambda: RoutingTime.from_time(datetime.time(23, 59, 59)),
    )
    vehicle_count: int = 2
    vehicle_speed_mph: float = 18.0
    vehicle_capacity: int = 16
    constraints: Constraints = field(default_factory=lambda: Constraints())
    optimization: OptimizationType = OptimizationType.MILEAGE


@dataclass
class SearchSettings:
    max_mileage_per_vehicle: int = 100
    distance_span_cost_coefficient: int = 0
    base_penalty: int = 1000
    penalty_scale_req_vehicle: int = 3
    penalty_scale_pickups: int = 2
    use_full_propagation: bool = True
    use_search_logging: bool = False
    first_solution_strategy: OrToolsEnum = FSS.LOCAL_CHEAPEST_INSERTION
    local_search_metaheuristic: OrToolsEnum = LSM.GUIDED_LOCAL_SEARCH
    solver_time_limit_seconds: int | None = 120
    solver_solution_limit: int | None = 2000


@dataclass
class DataModel:
    addresses: AddressDict
    distance_map: TravelCostMap
    vehicles: VehicleDict
    packages: PackageDict
    nodes: list[Node]
    scenario: RoutingScenario
    settings: SearchSettings

    @classmethod
    def with_defaults(cls) -> DataModel:
        scenario = RoutingScenario()
        addresses = Address.from_csv()
        vehicles = Vehicle.with_shared_attributes(
            scenario.vehicle_count,
            scenario.vehicle_speed_mph,
            scenario.vehicle_capacity,
            TravelCostMap.with_duration(addresses, scenario.vehicle_speed_mph),
        )
        packages = Package.from_csv(addresses, vehicles)
        return cls(
            addresses=addresses,
            distance_map=TravelCostMap.with_distance(addresses),
            vehicles=vehicles,
            packages=packages,
            nodes=Node.from_packages(packages),
            scenario=RoutingScenario(),
            settings=SearchSettings(),
        )


@dataclass
class Stop:
    node: Node
    vehicle_load: int
    visit_time: RoutingTime
    mileage: float


@dataclass
class Route:
    vehicle: Vehicle
    stops: list[Stop]

    @classmethod
    def create_route(
        cls,
        vehicle: Vehicle,
        data: DataModel,
        manager: pywrapcp.RoutingIndexManager,
        router: pywrapcp.RoutingModel,
        assignments: pywrapcp.Assignment,
    ) -> Route:
        stops = []
        vehicle_load = 0
        mileage = 0.0
        index = router.Start(vehicle.index)
        time_dimension = router.GetDimensionOrDie("Time")

        def create_stop(index: int, previous_index: int | None) -> Stop:
            nonlocal vehicle_load, mileage
            node = data.nodes[manager.IndexToNode(index)]
            vehicle_load += node.kind.capacity_impact
            route_seconds = assignments.Min(time_dimension.CumulVar(index))
            visit_time = RoutingTime.from_seconds(
                data.scenario.day_start.seconds + route_seconds,
            )
            if previous_index:
                mileage += (
                    router.GetArcCostForVehicle(previous_index, index, vehicle.index)
                    / MILEAGE_SCALE_FACTOR
                )

            if node.kind == NodeKind.PICKUP:
                node.package.shipped_time = visit_time
                node.package.vehicle_used = vehicle
            elif node.kind == NodeKind.DELIVERY:
                node.package.delivered_time = visit_time

            return Stop(node, vehicle_load, visit_time, mileage)

        previous_index = None
        while not router.IsEnd(index):
            stops.append(create_stop(index, previous_index))
            previous_index = index
            index = assignments.Value(router.NextVar(index))
        stops.append(create_stop(index, previous_index))

        return cls(vehicle, stops)

    @property
    def delivered_packages(self) -> PackageDict:
        return {
            stop.node.package.id: stop.node.package
            for stop in self.stops
            if stop.node.kind == NodeKind.DELIVERY and stop.node.package
        }

    @property
    def mileage(self) -> float:
        return self.stops[-1].mileage if self.stops else 0.0

    @property
    def end_time(self) -> RoutingTime | None:
        return self.stops[-1].visit_time if self.stops else None


@dataclass
class Solution:
    data: DataModel
    routes: list[Route]

    @classmethod
    def save_solution(
        cls,
        data: DataModel,
        manager: pywrapcp.RoutingIndexManager,
        router: pywrapcp.RoutingModel,
        assignments: pywrapcp.Assignment,
    ) -> Solution:
        return cls(
            data=data,
            routes=[
                Route.create_route(
                    vehicle,
                    data,
                    manager,
                    router,
                    assignments,
                )
                for vehicle in data.vehicles.values()
            ],
        )

    @property
    def mileage(self) -> float:
        return sum(route.mileage for route in self.routes)

    @property
    def end_time(self) -> RoutingTime | None:
        route_times = [
            route.end_time.seconds for route in self.routes if route.end_time
        ]
        if route_times:
            max_time = max(route_times)
            return RoutingTime.from_seconds(max_time)
        return None

    @property
    def delivered_packages(self) -> PackageDict:
        return {
            package_id: package
            for route in self.routes
            for package_id, package in route.delivered_packages.items()
        }

    @property
    def missed_packages(self) -> PackageDict:
        return {
            package_id: package
            for package_id, package in self.data.packages.items()
            if package_id not in self.delivered_packages
        }

    @property
    def missed_packages_str(self) -> str:
        return str(list(self.missed_packages.keys()))[1:-1]

    @property
    def delivered_packages_count(self) -> int:
        return len(self.delivered_packages)

    @property
    def missed_packages_count(self) -> int:
        return len(self.missed_packages)

    @property
    def delivery_success_rate(self) -> float:
        return self.delivered_packages_count / (
            self.delivered_packages_count + self.missed_packages_count
        )

    @property
    def delivery_percentage(self) -> str:
        return f"{round(self.delivery_success_rate * 100, 2)}%"

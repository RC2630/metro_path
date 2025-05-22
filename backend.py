from __future__ import annotations
from typing import Any
from queue import Queue

# ------------------------------------------------------------------

def intersection(l1: list[Any], l2: list[Any]) -> list[Any]:
    return [element for element in l1 if element in l2]

# ------------------------------------------------------------------

class Station:

    def __init__(self: Station, name: str) -> None:
        self.name: str = name
        self.lines: list[Line] = []
        self.lines_raw: list[str] = []
        self.neighbours: list[Station] = []
        self.neighbours_raw: list[str] = []

# ------------------------------------------------------------------

class Line:

    def __init__(self: Line, name: str, is_loop: bool) -> None:
        self.name: str = name
        self.stations: list[Station] = []
        self.stations_raw: list[str] = []
        self.is_loop: bool = is_loop

    def get_station_index(self: Line, station: str) -> int:
        for i in range(len(self.stations)):
            if self.stations[i].name == station:
                return i
        raise RuntimeError(f"no station found: {station}")

# ------------------------------------------------------------------

class PathComponent:

    def __init__(
        self: PathComponent, from_station: str, to_station: str,
        lines: list[str], num_stations: int
    ) -> None:
        self.from_station: str = from_station
        self.to_station: str = to_station
        self.lines: list[str] = lines
        self.num_stations: int = num_stations

# ------------------------------------------------------------------

class Path:

    def __init__(self: Path) -> None:
        self.components: list[PathComponent] = []

# ------------------------------------------------------------------

def contains_station(station_list: list[Station], station: str) -> bool:
    for station_obj in station_list:
        if station_obj.name == station:
            return True
    return False

def contains_line(line_list: list[Line], line: str) -> bool:
    for line_obj in line_list:
        if line_obj.name == line:
            return True
    return False

def get_station(station_list: list[Station], station: str) -> Station:
    for station_obj in station_list:
        if station_obj.name == station:
            return station_obj
    raise RuntimeError(f"no station found: {station}")

def get_line(line_list: list[Line], line: str) -> Line:
    for line_obj in line_list:
        if line_obj.name == line:
            return line_obj
    raise RuntimeError(f"no line found: {line}")

def get_lines_for_station_to_neighbour(station: Station, neighbour: Station) -> list[Line]:

    lines_in_common: list[Line] = intersection(station.lines, neighbour.lines)
    okay_lines: list[Line] = []

    for line in lines_in_common:
        station_index: int = line.get_station_index(station.name)
        neighbour_index: int = line.get_station_index(neighbour.name)

        diff_is_1: bool = abs(station_index - neighbour_index) == 1
        station_index_is_edge: bool = station_index in [0, len(line.stations) - 1]
        neighbour_index_is_edge: bool = neighbour_index in [0, len(line.stations) - 1]

        if diff_is_1 or (line.is_loop and station_index_is_edge and neighbour_index_is_edge):
            okay_lines.append(line)

    return okay_lines

# ------------------------------------------------------------------

def find_shortest_path(start_station: Station, end_station: Station) -> Path:

    path_raw: list[Station] = []
    try:
        path_raw = pathfind_helper(start_station, end_station)
    except RuntimeError as e:
        raise e
    
    path: Path = Path()
    for i in range(1, len(path_raw)):
        path.components.append(PathComponent(
            path_raw[i - 1].name, path_raw[i].name,
            [line.name for line in get_lines_for_station_to_neighbour(
                path_raw[i - 1], path_raw[i]
            )], 1
        ))

    simplify(path)
    return path

def pathfind_helper(start_station: Station, end_station: Station) -> list[Station]:
    frontier: Queue[list[Station]] = Queue()
    frontier.put([start_station])
    while not frontier.empty():
        curr: list[Station] = frontier.get()
        if curr[-1].name == end_station.name:
            return curr
        for neighbour in curr[-1].neighbours:
            frontier.put(curr + [neighbour])
    raise RuntimeError(f"no path found: {start_station.name} -> {end_station.name}")

def simplify(path: Path) -> None:
    index: int = 0
    while index < len(path.components) - 1:
        pc1: PathComponent = path.components[index]
        pc2: PathComponent = path.components[index + 1]
        lines_in_common: list[str] = intersection(pc1.lines, pc2.lines)
        if len(lines_in_common) > 0:
            path.components[index] = PathComponent(
                pc1.from_station, pc2.to_station, lines_in_common,
                pc1.num_stations + pc2.num_stations
            )
            del path.components[index + 1]
        else:
            index += 1
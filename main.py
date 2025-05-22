from typing import Any
from io import TextIOWrapper as File
from backend import *

# ------------------------------------------------------------------

STATIONS: list[Station] = []
LINES: list[Line] = []

# ------------------------------------------------------------------

def is_number_between(target: Any, a: int, b: int) -> bool:
    try:
        converted: int = int(target)
        return a <= converted <= b
    except ValueError:
        return False
    
def append_if_not_present(l: list[Any], e: Any):
    if e not in l:
        l.append(e)
    
# ------------------------------------------------------------------

def init_lines_stations() -> None:
    
    stations_file: File = open("info/stations.txt", "r", encoding = "utf-8")
    content: list[list[str]] = [line.split(" ") for line in stations_file.read().split("\n")]
    stations_file.close()

    for content_line in content:
        parsed_line: str = content_line[0][:-1]
        parsed_stations: list[str] = content_line[1:]
        init_line_with_stations(parsed_line, parsed_stations)

    for line in LINES:
        for station_raw in line.stations_raw:
            line.stations.append(get_station(STATIONS, station_raw))
    
    for station in STATIONS:
        for line_raw in station.lines_raw:
            station.lines.append(get_line(LINES, line_raw))
        for neighbour_raw in station.neighbours_raw:
            station.neighbours.append(get_station(STATIONS, neighbour_raw))

def init_line_with_stations(line: str, stations: list[str]) -> None:
    new_line: Line = Line(line)
    for i in range(len(stations)):
        station_name: str = stations[i]
        contains: bool = contains_station(STATIONS, station_name)
        station: Station = \
            get_station(STATIONS, station_name) if contains else Station(station_name)
        station.lines_raw.append(line)
        new_line.stations_raw.append(station_name)
        if i != 0:
            append_if_not_present(station.neighbours_raw, stations[i - 1])
        if i != len(stations) - 1:
            append_if_not_present(station.neighbours_raw, stations[i + 1])
        if not contains:
            STATIONS.append(station)
    LINES.append(new_line)

def display_lines() -> None:
    for line in LINES:
        print(f"\nLINE {line.name}:")
        for i in range(len(line.stations)):
            current_station: Station = line.stations[i]
            print(f"{i + 1}. {current_station.name}", end = "")
            if len(current_station.lines) >= 2:
                transfer_list: list[str] = [l.name for l in current_station.lines if l != line]
                line_wording: str = "line" if len(transfer_list) == 1 else "lines"
                print(f" (can transfer to {line_wording} {', '.join(transfer_list)})")
            else:
                print()

def display_stations() -> None:
    for station in STATIONS:
        print(
            f"\nSTATION {station.name}:\n"
            f"- lines: {', '.join([line.name for line in station.lines])}\n"
            f"- neighbours: {', '.join(neighbour.name for neighbour in station.neighbours)}"
        )

def find_path() -> None:

    start_station: str = input("\nEnter the starting station: ")
    while not contains_station(STATIONS, start_station):
        start_station = input("This station does not exist. Try again: ")
    end_station: str = input("Enter the destination station: ")
    while not contains_station(STATIONS, end_station):
        end_station = input("This station does not exist. Try again: ")
    
    if start_station == end_station:
        print("\nSince the starting and destination stations are the same, the path is trivial. Have fun travelling to nowhere, lol!")
        return
    
    path: Path = find_shortest_path(
        get_station(STATIONS, start_station),
        get_station(STATIONS, end_station)
    )

    print()
    for i in range(len(path.components)):
        component: PathComponent = path.components[i]
        num_stations_wording: str = "station" if component.num_stations == 1 else "stations"
        print(
            f"{i + 1}. take line {' or '.join(component.lines)} "
            f"from {component.from_station} to {component.to_station} "
            f"({component.num_stations} {num_stations_wording})"
        )
    
# ------------------------------------------------------------------

def run_program() -> None:

    choice_raw: str = input(
        "\nWelcome to the Metro Path program! We offer the following services:\n\n"
        "(1) list all lines and their stations\n"
        "(2) list all stations and which lines they serve\n"
        "(3) find shortest path between two stations\n\n"
        "Which option would you like to choose? Enter your choice here: "
    )

    while not is_number_between(choice_raw, 1, 3):
        choice_raw = input("Your choice is not valid! Try again: ")
    choice: int = int(choice_raw)
    init_lines_stations()

    if choice == 1:
        display_lines()
    elif choice == 2:
        display_stations()
    elif choice == 3:
        find_path()

    print("\nThank you for using the Metro Path program! Have a great day!")

# ------------------------------------------------------------------

if __name__ == "__main__":
    run_program()
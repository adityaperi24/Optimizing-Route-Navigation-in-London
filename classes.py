"""CSC111 Final Project, DataClasses

This python module contains classes for junctions and road system(entire system of roads in london),
functions to read road map data, add junctions, add roads, get distance, location, vehicle data,
compute the time between two junctions, and create the graph according to the dataset.


Copyright and Usage Information
===============================

This file is Copyright (c) 2021 by Aditya Shankar Sarma Peri, Praket Kanaujia,
Aakash Vaithyanathan, and Nazanin Ghazitabatabai.

This module is expected to use data from:
https://data.gov.uk/dataset/208c0e7b-353f-4e2d-8b7a-1a7118467acc/gb-road-traffic-counts.
The GB Road Traffic Counts is produced by the Department for Transport. The Department for Transport
collects traffic data to produce statistics on the level of traffic on roads in Great Britain,
last updated in October 2020.
"""

from __future__ import annotations
from typing import Any, Union
import csv


class Junction:
    """This dataclass represents a junction.

    Instance Attributes:
        - name: The name of the junction.
        - neighbours: a dictionary that maps neighbouring junctions to a float which contains the
         distance between them and a list of the number of cycles and motor vehicles.

    Representation Invariants:
    - isinstance(self.name, str)
    - isinstance(self.neighbours, dict)
    """
    name: str
    neighbours: dict[Junction, tuple[float, list[int, int]]]

    def __init__(self, road_name: str,
                 neighbours: dict[Junction, tuple[float, list[int, int]]]) -> None:
        """Initialize Junction class. """
        self.name = road_name
        self.neighbours = neighbours

    def check_connected(self, target_item: Any, visited: set[Junction]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.name == target_item:
            return True
        else:
            visited.add(self)
            for u in self.neighbours:
                if u not in visited:
                    if u.check_connected(target_item, visited):
                        return True

            return False


class RoadSystem:
    """This dataclass represents the entire system of roads in London.

    Instance Attributes:
        - junctions - A dictionary of the junction name with the junction object.

    Representation Invariants:
    - isinstance(self.junctions, dict)

    """

    junctions: dict[Any, Junction]

    def __init__(self) -> None:
        """Initialize an empty RoadSystem
        """
        self.junctions = {}

    def get_all_junctions(self) -> list:
        """Return a list of all the junctions in the RoadSystem"""
        return list(self.junctions.keys())

    def get_junction_name(self, name: str) -> Junction:
        """Return the junction given its name from the RoadSystem

        Preconditions:
        - name != ''
        """

        if name in self.junctions:
            return self.junctions[name]
        else:
            raise ValueError

    def add_junction(self, road_name: Any) -> None:
        """Adds a junction into the RoadSystem."""
        if road_name == '':
            return None
        elif road_name in self.junctions:
            return None
        else:
            self.junctions[road_name] = Junction(road_name, {})
            return None

    def add_road(self, junction1_name: str, junction2_name: str,
                 distance: float, cycles: int, motor: int) -> None:
        """Adds a road(edge) if two junctions are adjacent to one another

        Raises a ValueError if either of the junctions entered as parameter aren't present in
        self._junctions.

        Preconditions:
          - distance >= 0.0
          - cycles >= 0
          - motor >= 0
        """
        if junction1_name == '' or junction2_name == '':
            return None

        elif junction1_name in self.junctions and junction2_name in self.junctions:
            v1 = self.junctions[junction1_name]
            v2 = self.junctions[junction2_name]

            v1.neighbours[v2] = (distance, [cycles, motor])
            v2.neighbours[v1] = (distance, [cycles, motor])
            return None
        else:
            raise ValueError

    def get_junctions_dist(self, start: str, end: str) -> Union[float, None]:
        """ Return the distance associated with the start and end junction if they are neighbours.

            Return None if there is no distance associated between the two junctions.

            Preconditions:
            - start != ''
            - end != ''
        """
        v1 = self.junctions[start]
        v2 = self.junctions[end]
        if v1 in self.junctions[end].neighbours and v2 in self.junctions[start].neighbours:
            return v1.neighbours[v2][0]
        else:
            return None

    @staticmethod
    def get_junctions_location(start: str, end: str) -> [float, float]:
        """ Return the location as [latitude, longitude] associated with the start and end junction.

        Precondition:
        - start != ''
        - end != ''
        """
        dict_junctions = load_dict('road.csv')
        location = []
        start_vertex_dict = dict_junctions[start]
        for value in start_vertex_dict:
            if value['end junction'] == end:
                location.extend([value['latitude'], value['longitude']])
                break

        if location != []:
            return location
        else:
            end_vertex_dict = dict_junctions[end]
            for value in end_vertex_dict:
                if value['end junction'] == start:
                    location.extend([value['latitude'], value['longitude']])
                    break

            return location

    def get_road_vehicle_data(self, start: str, end: str, mode: str) -> Union[int, None]:
        """ Return the number of vehicles present on the road between start and end junctions,
            if they are neighbours.

            Return None if they are not neighbours.

            Preconditions:
            - start != ''
            - end != ''
            - mode != ''

        """
        v1 = self.junctions[start]
        v2 = self.junctions[end]
        if v1 in self.junctions[end].neighbours and v2 in self.junctions[start].neighbours:
            if mode == 'cycle':
                return v1.neighbours[v2][1][0]
            else:
                return v1.neighbours[v2][1][1]
        else:
            return None

    def connected(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are connected vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.junctions and item2 in self.junctions:
            v1 = self.junctions[item1]
            return v1.check_connected(item2, set())  # Pass in an empty "visited" set
        else:
            return False

    def time_taken_between_junctions(self, mode: str, start: str, end: str) -> Union[float, str]:
        """
        This method calculates the time taken based on the mode of transport the user inputs,
        accounting for any delays due to traffic.

        Preconditions:
        - mode != ''
        - start != ''
        - end != ''
        """
        dist = self.get_junctions_dist(start, end)
        vehicle = self.get_road_vehicle_data(start, end, mode)
        if mode == 'cycle':
            if vehicle == 0:
                return 'Cycles cannot be used on that road!'
            else:
                cycle_flow = vehicle / 24
                cycle_density = (cycle_flow / 60.0) / dist
                speed = float(cycle_flow) / float(cycle_density)
                time_taken = dist / speed
        else:
            motor_flow = vehicle / 24
            motor_density = (motor_flow / 60.0) / dist
            speed = motor_flow / motor_density
            time_taken = dist / speed

        return round(time_taken, 3)


def load_graph(file_name: str) -> RoadSystem:
    """Read file_name and return a graph where the vertices are the start_junction_road_name
    and end_junction_road_name with their edge and their distance.
    Both the start and end junctions are major roads located in London.

    Preconditions
       - isinstance(file_name, str)
       - file_name is a path to the csv file location

    Note: The file_name is 'road.csv'
    """
    graph = RoadSystem()
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            graph.add_junction(row[4])
            graph.add_junction(row[5])
            graph.add_road(row[4], row[5], float(row[8]), int(row[9]), int(row[10]))
    return graph


def load_dict(file_name: str) -> dict[str, list[dict]]:
    """Read file_name and return a dictionary where the keys are the start junctions
        and the values are a list of dictionaries. Each dictionary contains the keys
        road name, end junction,  latitude, longitude, pedal cycle, distance, and all motor vehicles
        with their corresponding value.
        The roads are major roads located in London in 2019(latest version).

       Preconditions
       - isinstance(file_name, str)
       - file_name is a path to the csv file location

        Note: The file_name is 'road.csv'
       """
    dict_so_far = {}
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            new_dict = {}
            if row[4] not in dict_so_far:
                dict_so_far[row[4]] = []
                dict_so_far[row[4]].append(new_dict)
                new_dict['end junction'] = row[5]
                new_dict['road name'] = row[2]
                new_dict['latitude'] = float(row[6])
                new_dict['longitude'] = float(row[7])
                new_dict['distance'] = float(row[8])
                new_dict['pedal cycle'] = int(row[9])
                new_dict['all motor vehicles'] = int(row[10])
            else:
                if all(row[5] != subdict['end junction'] for subdict in dict_so_far[row[4]]):
                    dict_so_far[row[4]].append(new_dict)
                    new_dict['end junction'] = row[5]
                    new_dict['road name'] = row[2]
                    new_dict['latitude'] = float(row[6])
                    new_dict['longitude'] = float(row[7])
                    new_dict['distance'] = float(row[8])
                    new_dict['pedal cycle'] = int(row[9])
                    new_dict['all motor vehicles'] = int(row[10])

    return dict_so_far


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E9998', 'E1136', 'R0913'],
        'extra-imports': ['math', 'csv'],
        'allowed-io': [],
        'max-nested-blocks': 5,
    })

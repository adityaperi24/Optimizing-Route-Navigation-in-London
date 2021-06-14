"""CSC111 Final Project, DataClasses

This python module contains several methods for performing the different computations on the data
extracted from the csv file with the help of methods in classes.py file.
The list of computations done on this data are:

1. A function with outputs a path with the shortest time ( path_with_shortest_time() )

2. A function which calculates and outputs the shortest route using Dijkstra's algorithm
    ( shortest_route() )

3. A function which outputs all the possible paths between 2 junctions
    ( multiple_path() with helper find_path())

4. A function which calculates and outputs the most direct route between the 2 junctions using
    Breadth First Search Algorithm ( direct_route() )


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

from typing import Dict, Union, Optional
import math
import classes


def path_with_shortest_time(graph: classes.RoadSystem, mode: str, alternative_paths: Dict) \
        -> tuple[list[str], float, float]:
    """
    Shortest time taken based on the mode of transport the user inputs, accounting for any
    delays due to traffic.

    In the returned tuple, the first element represents the path, the second represents the time
    taken between those paths and the third element represents the distance of that path

    Preconditions:
    - mode != ''
    - alternative_paths != {}

    """
    time_taken = []
    paths = []
    distances = []
    keys = alternative_paths.keys()
    for key in keys:
        path = alternative_paths[key]
        paths.append(path)
        time = 0.0
        distance = 0.0
        for i in range(0, len(path) - 1):
            start = path[i]
            end = path[i + 1]
            times = graph.time_taken_between_junctions(mode, start, end)
            if isinstance(times, float):
                time += times
            distance += graph.get_junctions_dist(start, end)
        time_taken.append(time)
        distances.append(distance)

    min_time = min(time_taken)
    min_time_index = time_taken.index(min_time)
    shortest_path = paths[min_time_index]
    shortest_path_distance = distances[min_time_index]
    return (shortest_path, round(min_time, 3), shortest_path_distance)


def shortest_route(graph: classes.RoadSystem, junction1_name: str, junction2_name: str) \
        -> tuple[list, float]:
    """Return the shortest route between junction1 and junction2 using Dijkstra's
    algorithm and its distance

    Preconditions:
    - junction1_name != '' and junction2_name != ''

    >>> g = classes.RoadSystem()
    >>> g.add_junction('A')
    >>> g.add_junction('B')
    >>> g.add_junction('C')
    >>> g.add_junction('D')
    >>> g.add_junction('E')
    >>> g.add_road('A', 'B', 6, 0, 0)
    >>> g.add_road('A', 'D', 1, 0, 0)
    >>> g.add_road('D', 'B', 2, 0, 0)
    >>> g.add_road('D', 'E', 1, 0, 0)
    >>> g.add_road('E', 'B', 2, 0, 0)
    >>> g.add_road('C', 'B', 5, 0, 0)
    >>> g.add_road('E', 'C', 5, 0, 0)
    >>> shortest_route(g, 'A', 'C')
    (['A', 'D', 'E', 'C'], 7.0)
    >>> shortest_route(g, 'A', 'B')
    (['A', 'D', 'B'], 3.0)
    """
    if not graph.connected(junction1_name, junction2_name):
        return ([], 0.0)

    path_so_far = []
    dict_all_dist = {junction1_name: (0, [])}
    visited = []
    unvisited = []
    for v in graph.get_all_junctions():
        unvisited.append(v)
        if v != junction1_name:
            dict_all_dist[v] = (math.inf, [])

    while junction2_name in unvisited:
        if junction1_name in unvisited:
            current_vertex = junction1_name

        else:
            min_d = dict_all_dist[unvisited[0]]
            current_vertex = unvisited[0]
            for vertex in unvisited:
                d = dict_all_dist[vertex]
                if d < min_d:
                    current_vertex = vertex

        for neighbor in graph.junctions[current_vertex].neighbours:
            if neighbor.name not in visited:
                d = graph.get_junctions_dist(current_vertex, neighbor.name)
                if d + dict_all_dist[current_vertex][0] < dict_all_dist[neighbor.name][0]:
                    dict_all_dist[neighbor.name] = \
                        (d + dict_all_dist[current_vertex][0], current_vertex)

        visited.append(current_vertex)

        unvisited.remove(current_vertex)

    previous_vertex = dict_all_dist[junction2_name][1]
    path_so_far.append(previous_vertex)
    while previous_vertex != []:
        previous_vertex = dict_all_dist[previous_vertex][1]
        path_so_far.insert(0, previous_vertex)

    path_so_far.append(junction2_name)
    return (path_so_far[1:], float(dict_all_dist[junction2_name][0]))


def multiple_path(graph: classes.RoadSystem, start: str, end: str, n: Optional[int] = 0) -> Dict:
    """This function returns a dictionary mapping the total_distance to the path taken from
    start to end. The dictionary may contain more than one key depending on the value of 'n'.
    'n' denotes the number of paths the user wants to have to reach from 'start' to 'end'.
    Less than 'n' paths are returned if there isn't any such paths.

    Preconditions:
     - start != '' and end != ''
     - graph is a valid graph object with different junctions inputted from the readfile
      methods.

    """
    all_possible_paths = []
    start_vertex = graph.get_junction_name(name=start)
    for junction in start_vertex.neighbours:  # junction represents a vertex
        path = find_path(junction, end, {start_vertex})
        if path is not None:
            if path[-1] == end:
                # Add the start_node to the path.
                path.insert(0, start)
                all_possible_paths.append(path)

    if n == 0:
        dict_path = {}
        for path in all_possible_paths:
            total_dist = 0
            for i in range(0, len(path) - 1):
                total_dist += graph.get_junctions_dist(path[i], path[i + 1])

            dict_path[total_dist] = path

        return dict_path

    elif n < len(all_possible_paths):
        dict_path = {}
        required_paths = all_possible_paths[0:n]
        for path in required_paths:
            total_dist = 0
            for i in range(0, len(path) - 1):
                total_dist += graph.get_junctions_dist(path[i], path[i + 1])

            dict_path[total_dist] = path

        return dict_path

    else:
        dict_path = {}
        for path in all_possible_paths:
            total_dist = 0
            for i in range(0, len(path) - 1):
                total_dist += graph.get_junctions_dist(path[i], path[i + 1])

            dict_path[total_dist] = path

        return dict_path


def find_path(start: classes.Junction, target: str, visited: set[classes.Junction]) -> \
        Union[None, list]:
    """This helper method return a path from the vertex to the target_item if such a path exists.

    Preconditions:
    - target != ''

    """

    if start.name == target:
        return [start.name]
    else:
        visited.add(start)
        path = [start.name]
        neighbours = start.neighbours
        if neighbours != {}:
            for v in neighbours:
                if v not in visited:
                    lst = find_path(start=v, target=target, visited=visited)
                    if lst is not None:
                        path.extend(lst)
                    else:
                        path.extend([])
                    return path

        else:
            return []
    return None


def direct_route(graph: classes.RoadSystem, start: str, end: str) -> tuple[list, float]:
    """Return the most direct route between start and end along with its distance using
    Breadth-first search algorithm.
    >>> g = classes.RoadSystem()
    >>> g.add_junction('A')
    >>> g.add_junction('B')
    >>> g.add_junction('C')
    >>> g.add_junction('D')
    >>> g.add_junction('E')
    >>> g.add_junction('F')
    >>> g.add_road('A', 'B', 6, 0, 0)
    >>> g.add_road('A', 'D', 1, 0, 0)
    >>> g.add_road('D', 'B', 2, 0, 0)
    >>> g.add_road('D', 'E', 1, 0, 0)
    >>> g.add_road('E', 'B', 2, 0, 0)
    >>> g.add_road('C', 'B', 5, 0, 0)
    >>> g.add_road('E', 'C', 5, 0, 0)
    >>> g.add_road('E', 'F', 5, 0, 0)
    >>> direct_route(g, 'A', 'F')
    (['A', 'B', 'E', 'F'], 13.0)
    """
    total_distance = 0.0
    visited = set()
    queue = [[start]]
    if start == end:
        return ([start], 0.0)

    while queue != []:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            for neighbour in graph.junctions[node].neighbours:
                new_path = list(path)
                new_path.append(neighbour.name)

                queue.append(new_path)

                if neighbour.name == end:
                    for i in range(len(new_path) - 1):
                        total_distance += graph.get_junctions_dist(new_path[i], new_path[i + 1])

                    return (new_path, total_distance)
            visited.add(node)
    return ([], 0.0)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E9997', 'E1136', 'R0914'],
        'extra-imports': ['math', 'classes', 'typing'],
        'allowed-io': [],
        'max-nested-blocks': 5,
    })

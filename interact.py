"""CSC111 Final Project, Interact file.

The interact file to interact with the user, ask the origin, stop places, and destination and
visualize multiple paths, shortest path, the most direct path, and the shortest path in terms of time OR the path with the specific stops that the user inputed.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 by Aditya Shankar Sarma Peri, Praket Kanaujia,
Aakash Vaithyanathan, and Nazanin Ghazitabatabai.

This module is expected to use data from:
https://data.gov.uk/dataset/208c0e7b-353f-4e2d-8b7a-1a7118467acc/gb-road-traffic-counts.
The GB Road Traffic Counts is produced by the Department for Transport. The Department for Transport
collects traffic data to produce statistics on the level of traffic on roads in Great Britain,
last updated in October 2020."""

import classes
import computations
import visualizations

graph_dict = classes.load_dict('road.csv')
graph = classes.load_graph('road.csv')


def ask_origin() -> str:
    """Ask the user where they want to go? Recommend start junctions to the user
        to pick one from. Return the user's answer."""
    question1 = 'Where do you want to start? Recommended places are: LA Boundary,' \
                ' M1 spur, A406, York St. '
    input1 = input(question1)
    return input1


origin = ask_origin()


def ask_stops() -> int:
    """Ask the user how many places to stop by."""

    question2 = 'How many places do you want to stop by?' \
                ' (Please enter an integer For example 1, 2, 3, or 4.)'
    input2 = input(question2)

    return int(input2)


number_stops = ask_stops()


def ask_destination() -> str:
    """Ask the user where they want to go and recommended end junctions to
     pick one from."""

    question3 = 'Where do you want to go? Recommended places are:' \
                ' A406, M1 spur, LA Boundary, A223, Fowler Rd, Marsh Way, High St, Caledonian Rd. '
    input3 = input(question3)
    return input3


destination = ask_destination()


def ask_mode_transport() -> str:
    """Ask the mode of transport being used. Either cycle or motor vehicles
    (bus, car, truck, motorcycle)."""
    question = 'Which mode of transport you will use? cycle or' \
               ' motor vehicles(bus, car, motorcycle, truck etc.)? '
    mode_input = input(question)
    return mode_input


mode_transport = ask_mode_transport()


def visualize() -> None:
    """Show the visualizations for paths with the number of stops OR direct path, shortest path,
     and the most efficient path in terms of time along with the total destination and time taken.
     """

    is_available = visualizations.visualize_path_specific_stops(origin,
                                                                destination, number_stops)
    if not is_available[0]:
        print('')
        n = input(f'How many paths are you looking for from {origin} to {destination}?')
        visualizations.visualize_multiple_path(origin, destination, int(n))

        print('')
        print(f'No path found between {origin} and {destination} with {number_stops} stops.')
        print('')

        if visualizations.visualize_shortest_path(origin, destination):
            total_distance_shortest = computations.shortest_route(graph, origin, destination)[
                1]
            path_shortest = computations.shortest_route(graph, origin, destination)[
                0]
            list_time_shortestpath = []
            for i in range(len(path_shortest) - 1):
                list_time_shortestpath.append(
                    classes.RoadSystem.time_taken_between_junctions(graph,
                                                                    mode_transport,
                                                                    path_shortest[i],
                                                                    path_shortest[i + 1]))

            if any(isinstance(item, str) for item in list_time_shortestpath):
                print('Cycles cannot be used on the shortest road!')
            else:
                tota_time_shortestpath = sum(list_time_shortestpath)
                print(f'Total distance of the shortest path = {total_distance_shortest} KM')
                print(f'Total time of the shortest path = {tota_time_shortestpath} hours')
                print('')

        if visualizations.visualize_direct_path(origin, destination):
            helper_visualize()

        if visualizations.visualize_shortest_time_path(origin, destination, mode_transport):
            helper_visualize2()

    else:
        total_distance = is_available[1]
        time_between_juncs = []
        alternative_paths = computations.multiple_path(graph, origin, destination)
        shortest_time_path_tuple = computations.path_with_shortest_time(graph, mode_transport,
                                                                        alternative_paths)
        for i in range(len(shortest_time_path_tuple[0]) - 1):
            time_between_juncs.append(
                graph.time_taken_between_junctions(mode_transport, shortest_time_path_tuple[0][i],
                                                   shortest_time_path_tuple[0][i + 1]))
        if any(isinstance(item, str) for item in time_between_juncs):
            print('Cycles cannot be used on that road!')
            print('')
        else:
            total_time = sum(time_between_juncs)
            print(f'Total distance of the path with {number_stops} stops = {total_distance} KM')
            print(f'Total time of the path with {number_stops} stops = {total_time} hours')
            print('')

    print(
        'Please open the generated files to view the visualizations if either of the paths exist.')


def helper_visualize() -> None:
    """A helper for visualize for the direct path branch."""
    total_distance_direct = computations.direct_route(graph, origin, destination)[1]
    path_direct = computations.direct_route(graph, origin, destination)[0]
    list_time_direct = []
    for i in range(len(path_direct) - 1):
        list_time_direct.append(
            classes.RoadSystem.time_taken_between_junctions(graph,
                                                            mode_transport,
                                                            path_direct[i],
                                                            path_direct[i + 1]))

    if any(isinstance(item, str) for item in list_time_direct):
        print('Cycles cannot be used on the direct road!')
        print('')
    else:
        total_time_direct = sum(list_time_direct)
        print(f'Total distance of the direct path = {total_distance_direct} KM')
        print(f'Total time of the direct path = {total_time_direct} hours')
        print('')


def helper_visualize2() -> None:
    """A helper for visualize for the shortest time path branch."""
    alternative_paths = computations.multiple_path(graph, origin, destination)
    total_distance_shortest_time \
        = computations.path_with_shortest_time(graph, mode_transport, alternative_paths)[2]
    total_time_shortest_time \
        = computations.path_with_shortest_time(graph, mode_transport, alternative_paths)[1]

    print(f'Total distance of the shortest time path = {total_distance_shortest_time} KM')
    print(f'Total time of the shortest time path = {total_time_shortest_time} hours')
    print('')


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9997'],
        'extra-imports': ['random', 'classes', 'visualizations', 'computations'],
        'allowed-io': ['ask_origin', 'ask_stops', 'ask_mode_transport', 'ask_destination',
                       'visualize', 'helper_visualize', 'helper_visualize2'],
        'max-nested-blocks': 5,
    })

"""CSC111 Final Project, DataClasses

This python module contains several methods for visualizing the different routes plots with the
help of folium library.

The list of possible visualizations are:
- Plot multiple paths between the start and end junctions ( visualize_multiple_path() )

- Plot a path with certain number of stops specific by the user ( visualize_path_specific_stops() )

- Plot the shortest path between the start and end junctions and draw a few paths (maximum of 2) for
 comparative purposes ( visualize_shortest_path() )

- Plot the most direct path between the start and end junctions and draw a few paths (maximum of 2)
 for comparative purposes ( visualize_direct_path() )

- Plot the path with shortest time taken between the start and end junctions
( visualize_shortest_time_path() )


Copyright and Usage Information
===============================

This file is Copyright (c) 2021 by Aditya Shankar Sarma Peri, Praket Kanaujia,
Aakash Vaithyanathan, and Nazanin Ghazitabatabai.

This module is expected to use data from (with the help of the methods from classes file):
https://data.gov.uk/dataset/208c0e7b-353f-4e2d-8b7a-1a7118467acc/gb-road-traffic-counts.
The GB Road Traffic Counts is produced by the Department for Transport. The Department for Transport
collects traffic data to produce statistics on the level of traffic on roads in Great Britain,
last updated in October 2020.
"""

from typing import Tuple
import random
import folium
import classes
import computations


def visualize_multiple_path(start: str, end: str, n: int) -> None:
    """This method draws multiple routes (up to n such paths) between the start and end junctions.
    It returns less than n paths if those many paths do not exists. If no such path exists, the
    function simply prints a message indicating no such path exists.
    The method saves the map result in a separate file called 'multiple_routes.html' which when
    opened shows the visualization.

    NOTE: The start and end junctions are marked with beige markers to help identify them.

    file_path: 'road.csv'

    Preconditions
     - start != ''
     - end != ''
     - start != end
     - start and end represent appropriate places on the map

     """
    if start == end:
        print(' The start and end end junctions are the same! Please re run the program with '
              ' different start and end junctions.')
        return None

    dict_junctions = classes.load_dict('road.csv')
    end_junc_coord = [dict_junctions[end][0]['latitude'], dict_junctions[end][0]['longitude']]

    dict_road_coords = {}
    plot_map = folium.Map(location=[51.509865, -0.118092], tiles='cartodbpositron',
                          zoom_start=12)
    # Make marker for end junction.
    folium.Marker(location=end_junc_coord, popup='<b>' + end + '</b>',
                  tooltip='<b>Click here to see junction name</b>',
                  icon=folium.Icon(color='beige', icon='road')).add_to(plot_map)
    graph = classes.load_graph('road.csv')
    dict_path = computations.multiple_path(graph, start, end, n)

    colours = ['red', 'blue', 'purple', 'green', 'orange', 'gray', 'black', 'pink']
    colours_markers = colours.copy()

    if dict_path != {}:
        list_paths = [dict_path[key] for key in dict_path]
        # Plot different markers for all junctions in list_paths.
        req_plotting_variables = [colours_markers, end_junc_coord, plot_map]
        helper_plot_markers(graph, list_paths, dict_road_coords, start, req_plotting_variables)

        # Plot link between different markers
        req_road_link_variables = [end_junc_coord, plot_map]
        helper_plot_road_links(list_paths, colours, end, dict_road_coords, req_road_link_variables)

        print('\n\nHOORAY! A map with the possible multiple paths has been traced and generated. '
              'Please open the "multiple_routes.html" file under '
              'Plots_Generated folder to view the plot.')
        plot_map.save('Plots_Generated/multiple_routes.html')
        return None

    else:
        print(f'\n\nSorry! No multiple paths exists between the {start} and {end} junctions.')
        return None


def visualize_path_specific_stops(start: str, end: str, num_stops: int) -> Tuple[bool, float]:
    """This method plots a path between the start and end junctions based on the number of stops
    the user would like to make as specified by the parameter.
    The method saves the map result in a separate file called 'path_with_specific_stops.html',
    which when opened shows the visualization.

    The function also returns a Tuple(bool, float) which represents whether we could find such a
    path which the given num_stops or not along with the cumulative distance of this path.
    These return values are used in the main file appropriately

    NOTE: The start and end junctions are marked with green markers and the green road link
    represents the shortest path

    file_path: 'road.csv'

    Preconditions
     - start != ''
     - end != ''
     - start != end
     - start and end represent appropriate places on the map

     """
    if start == end:
        print(' The start and end end junctions are the same! Please re run the program with '
              ' different start and end junctions.')
        return (False, 0.0)

    dict_junctions = classes.load_dict('road.csv')
    end_junc_coord = [dict_junctions[end][0]['latitude'], dict_junctions[end][0]['longitude']]

    dict_road_coords = {}
    plot_map = folium.Map(location=[51.509865, -0.118092], tiles='cartodbpositron',
                          zoom_start=12)
    # Make marker for end junction.
    folium.Marker(location=end_junc_coord, popup='<b>' + end + '</b>',
                  tooltip='<b>Click here to see junction name</b>',
                  icon=folium.Icon(color='green', icon='road')).add_to(plot_map)
    graph = classes.load_graph('road.csv')
    dict_path = computations.multiple_path(graph, start, end)

    if dict_path != {}:
        list_paths = [dict_path[key] for key in dict_path]

        specific_stops_paths = [path for path in list_paths if len(path) == num_stops + 2]

        if specific_stops_paths != []:
            specific_stops_path = specific_stops_paths[0]
            # Plot different markers for shortest path
            req_plotting_variables = [end_junc_coord, plot_map]
            helper_plot_specific_marker(graph, specific_stops_path, dict_road_coords, start,
                                        req_plotting_variables)

            # Plot link between different markers for shortest path
            helper_plot_shortest_road_links(specific_stops_path, end, end_junc_coord,
                                            dict_road_coords, plot_map)

            # dist_specific_stop_path = [key for key in dict_path
            #                            if dict_path[key] == specific_stops_path][0]

            print('\n\nHOORAY! A map with paths with specific stops has been traced and generated. '
                  'Please open the "path_with_specific_stops.html" file '
                  'under Plots_Generated folder to view the plot.')
            plot_map.save('Plots_Generated/path_with_specific_stops.html')

            return (True, [key for key in dict_path
                           if dict_path[key] == specific_stops_path][0])

        else:
            return (False, 0.0)

    else:
        return (False, 0.0)


def visualize_shortest_path(start: str, end: str) -> bool:
    """This method draws multiple routes between the start and end junctions and colour codes the
     shortest path with green colour.
    The method saves the map result in a separate file called 'shortest_route.html', which when
    opened shows the visualization.

    NOTE: The start and end junctions are marked with green markers and the green road link
    represents the shortest path

    file_path: 'road.csv'

    Preconditions
     - start != ''
     - end != ''
     - start != end
     - start and end represent appropriate places on the map

     """
    if start == end:
        print(' The start and end end junctions are the same! Please re run the program with '
              ' different start and end junctions.')
        return False
    dict_junctions = classes.load_dict('road.csv')
    end_junc_coord = [dict_junctions[end][0]['latitude'], dict_junctions[end][0]['longitude']]

    dict_road_coords = {}
    plot_map = folium.Map(location=[51.509865, -0.118092], tiles='cartodbpositron',
                          zoom_start=12)
    # Make marker for end junction.
    folium.Marker(location=end_junc_coord, popup='<b>' + end + '</b>',
                  tooltip='<b>Click here to see junction name</b>',
                  icon=folium.Icon(color='green', icon='road')).add_to(plot_map)
    graph = classes.load_graph('road.csv')
    dict_path = computations.multiple_path(graph, start, end, 2)

    shortest_path = computations.shortest_route(graph, start, end)[0]

    colours = ['red', 'blue', 'purple', 'orange', 'gray', 'black', 'pink']
    colours_other_markers = colours.copy()

    if dict_path != {} and shortest_path != []:
        list_paths = [dict_path[key] for key in dict_path]
        if shortest_path in list_paths:
            list_paths.remove(shortest_path)

        # Plot different markers for each junction in path
        req_plotting_variables = [colours_other_markers, end_junc_coord, plot_map]
        helper_plot_markers(graph, list_paths, dict_road_coords, start, req_plotting_variables)

        # Plot different markers for shortest path
        req_plotting_variables = [end_junc_coord, plot_map]
        helper_plot_shortest_marker(graph, shortest_path, dict_road_coords, start,
                                    req_plotting_variables)

        # Plot link between different markers other than shortest path
        req_road_link_variables = [end_junc_coord, plot_map]
        helper_plot_road_links(list_paths, colours, end, dict_road_coords, req_road_link_variables)

        # Plot link between different markers for shortest path
        helper_plot_shortest_road_links(shortest_path, end, end_junc_coord, dict_road_coords,
                                        plot_map)

        print('\n\nHOORAY! A map with the shortest route has been traced and generated. '
              'Please open the "shortest_route.html" file under Plots_Generated folder '
              'to view the plot.')
        plot_map.save('Plots_Generated/shortest_route.html')
        return True

    else:
        print(f'\n\nSorry! No such shortest path exists between the {start} and {end} junctions.')
        return False


def visualize_direct_path(start: str, end: str) -> bool:
    """This method draws a few routes between the start and end junctions and colour codes the
     most direct path with green colour between the start and end junctions.
    The method saves the map result in a separate file called 'most_direct_route.html', which when
    opened shows the visualization.

    NOTE: The start and end junctions are marked with green markers and the green road link
    represents the shortest path

    file_path: 'road.csv'

    Preconditions
     - start != ''
     - end != ''
     - start != end
     - start and end represent appropriate places on the map

     """
    if start == end:
        print(' The start and end end junctions are the same! Please re run the program with '
              ' different start and end junctions.')
        return False

    dict_junctions = classes.load_dict('road.csv')
    end_junc_coord = [dict_junctions[end][0]['latitude'], dict_junctions[end][0]['longitude']]

    dict_road_coords = {}
    plot_map = folium.Map(location=[51.509865, -0.118092], tiles='cartodbpositron',
                          zoom_start=12)
    # Make marker for end junction.
    folium.Marker(location=end_junc_coord, popup='<b>' + end + '</b>',
                  tooltip='<b>Click here to see junction name</b>',
                  icon=folium.Icon(color='green', icon='road')).add_to(plot_map)
    graph = classes.load_graph('road.csv')
    dict_path = computations.multiple_path(graph, start, end, 2)

    direct_path = computations.direct_route(graph, start, end)[0]

    colours = ['red', 'blue', 'purple', 'orange', 'gray', 'black', 'pink']
    colours_other_markers = colours.copy()

    if dict_path != {} and direct_path != []:
        list_paths = [dict_path[key] for key in dict_path]
        if direct_path in list_paths:
            list_paths.remove(direct_path)

        # Plot different markers for each junction in path
        req_plotting_variables = [colours_other_markers, end_junc_coord, plot_map]
        helper_plot_markers(graph, list_paths, dict_road_coords, start, req_plotting_variables)

        # Plot different markers for shortest path
        req_plotting_variables = [end_junc_coord, plot_map]
        helper_plot_shortest_marker(graph, direct_path, dict_road_coords, start,
                                    req_plotting_variables)

        # Plot link between different markers other than shortest path
        req_road_link_variables = [end_junc_coord, plot_map]
        helper_plot_road_links(list_paths, colours, end, dict_road_coords, req_road_link_variables)

        # Plot link between different markers for shortest path
        helper_plot_shortest_road_links(direct_path, end, end_junc_coord, dict_road_coords,
                                        plot_map)

        print('\n\nHOORAY! A map with most direct paths has been traced and generated. '
              'Please open the "most_direct_route.html" file under Plots_Generated folder '
              'to view the plot.')
        plot_map.save('Plots_Generated/most_direct_route.html')
        return True

    else:
        print(f'\n\nSorry! No such direct path exists between the {start} and {end} junctions.')
        return False


def visualize_shortest_time_path(start: str, end: str, mode: str) -> bool:
    """This method draws multiple routes between the start and end junctions and colour codes the
     shortest path with green colour.
    The method saves the map result in a separate file called 'shortest_route.html', which when
    opened shows the visualization.

    NOTE: The start and end junctions are marked with green markers and the green road link
    represents the shortest path

    file_path: 'road.csv'

    Preconditions
     - start != ''
     - end != ''
     - start != end
     - start and end represent appropriate places on the map

     """
    if start == end:
        print(' The start and end end junctions are the same! Please re run the program with '
              ' different start and end junctions.')
        return False

    dict_junctions = classes.load_dict('road.csv')
    end_junc_coord = [dict_junctions[end][0]['latitude'], dict_junctions[end][0]['longitude']]

    dict_road_coords = {}
    plot_map = folium.Map(location=[51.509865, -0.118092], tiles='cartodbpositron',
                          zoom_start=12)
    # Make marker for end junction.
    folium.Marker(location=end_junc_coord, popup='<b>' + end + '</b>',
                  tooltip='<b>Click here to see junction name</b>',
                  icon=folium.Icon(color='green', icon='road')).add_to(plot_map)
    graph = classes.load_graph('road.csv')
    dict_path = computations.multiple_path(graph, start, end, 2)

    if dict_path != {}:
        list_paths = [dict_path[key] for key in dict_path]
        time_between_juncs = []
        shortest_time_path_tuple = computations.path_with_shortest_time(graph, mode, dict_path)
        for i in range(len(shortest_time_path_tuple[0]) - 1):
            time_between_juncs.append(
                graph.time_taken_between_junctions(mode, shortest_time_path_tuple[0][i],
                                                   shortest_time_path_tuple[0][i + 1]))

        if shortest_time_path_tuple[1] in list_paths:
            list_paths.remove(shortest_time_path_tuple[1])

        # Plot different markers for shortest_time_path
        req_plotting_variables = [end_junc_coord, plot_map]
        helper_plot_shortest_marker(graph, shortest_time_path_tuple[0], dict_road_coords, start,
                                    req_plotting_variables)

        # Plot link between different markers for shortest_time_path
        req_road_link_variables = [end_junc_coord, plot_map]
        helper_plot_time_road_links(shortest_time_path_tuple[0], time_between_juncs,
                                    end, dict_road_coords, req_road_link_variables)

        print('\n\nHOORAY! A map with the shortest time paths has been traced and generated. '
              'Please open the "shortest_route.html" file under Plots_Generated folder '
              'to view the plot.')
        plot_map.save('Plots_Generated/shortest_time_route.html')
        return True

    else:
        print(f'\n\nSorry! No such shortest time path exists between the {start} '
              f'and {end} junctions.')
        return False


def helper_plot_markers(graph: classes.RoadSystem(), list_paths: list, dict_road_coords: dict,
                        start: str, req_plotting_variables: list) -> None:
    """This is a helper method for visualize_multiple_path() method.
     The method iterates over the different junctions in a path and makes a marker for it with the
     help of the folium library plotting methods."""

    end_junc_coord = req_plotting_variables[1]
    colours = req_plotting_variables[0]
    list_colours = colours.copy()
    k = 0
    for path in list_paths:
        if k >= len(list_colours) and list_colours == []:
            colour = random.choice(colours)
        else:
            colour = colours[k]

        for i in range(len(path) - 1):
            if path[i] not in dict_road_coords:
                if path[i] == start:
                    coordinates = graph.get_junctions_location(start=path[i], end=path[i + 1])
                    dict_road_coords[path[i]] = coordinates

                    folium.Marker(location=coordinates, popup='<b>' + path[i] + '</b>',
                                  tooltip='<b><i>Click here to see junction name</i></b>',
                                  icon=folium.Icon(color='beige', icon='road')
                                  ).add_to(req_plotting_variables[2])
                else:
                    coordinates = graph.get_junctions_location(start=path[i], end=path[i + 1])
                    if coordinates == end_junc_coord:
                        list_paths.remove(path)
                    else:
                        dict_road_coords[path[i]] = coordinates
                        folium.Marker(location=coordinates, popup='<b>' + path[i] + '</b>',
                                      tooltip='<b><i>Click here to see junction name</i></b>',
                                      icon=folium.Icon(color=colour, icon='road')
                                      ).add_to(req_plotting_variables[2])

        k += 1
        if list_colours == []:
            pass
        else:
            list_colours.remove(colour)

    return None


def helper_plot_specific_marker(graph: classes.RoadSystem(), shortest_path: list,
                                dict_road_coords: dict, start: str,
                                req_plotting_variables: list) -> None:
    """This is a helper method for visualize_path_specific_stops() method.
     The method iterates over the different junctions in a path and makes a marker for it with the
     help of the folium library plotting methods."""
    end_junc_coord = req_plotting_variables[0]
    for i in range(len(shortest_path) - 1):
        if shortest_path[i] not in dict_road_coords:
            if shortest_path[i] == start:
                coordinates = graph.get_junctions_location(start=shortest_path[i],
                                                           end=shortest_path[i + 1])
                dict_road_coords[shortest_path[i]] = coordinates

                folium.Marker(location=coordinates, popup='<b>' + shortest_path[i] + '</b>',
                              tooltip='<b><i>Click here to see junction name</i></b>',
                              icon=folium.Icon(color='green', icon='road')
                              ).add_to(req_plotting_variables[1])
            else:
                coordinates = graph.get_junctions_location(start=shortest_path[i],
                                                           end=shortest_path[i + 1])
                if coordinates == end_junc_coord:
                    return None
                else:
                    dict_road_coords[shortest_path[i]] = coordinates
                    folium.Marker(location=coordinates, popup='<b>' + shortest_path[i] + '</b>',
                                  tooltip='<b><i>Click here to see junction name</i></b>',
                                  icon=folium.Icon(color='gray', icon='road')
                                  ).add_to(req_plotting_variables[1])

    return None


def helper_plot_shortest_marker(graph: classes.RoadSystem(), shortest_path: list,
                                dict_road_coords: dict, start: str,
                                req_plotting_variables: list) -> None:
    """This is a helper method for visualize_shortest_path() and visualize_direct_path() methods.
     The method iterates over the different junctions in a path and makes a marker for it with the
     help of the folium library plotting methods."""
    end_junc_coord = req_plotting_variables[0]
    for i in range(len(shortest_path) - 1):
        if shortest_path[i] == start:
            if shortest_path[i] not in dict_road_coords:
                coordinates = graph.get_junctions_location(start=shortest_path[i],
                                                           end=shortest_path[i + 1])
                dict_road_coords[shortest_path[i]] = coordinates
                folium.Marker(location=coordinates, popup='<b>' + shortest_path[i] + '</b>',
                              tooltip='<b><i>Click here to see junction name</i></b>',
                              icon=folium.Icon(color='green', icon='road')
                              ).add_to(req_plotting_variables[1])

        if shortest_path[i] not in dict_road_coords:
            if shortest_path[i] == start:
                coordinates = graph.get_junctions_location(start=shortest_path[i],
                                                           end=shortest_path[i + 1])
                dict_road_coords[shortest_path[i]] = coordinates

                folium.Marker(location=coordinates, popup='<b>' + shortest_path[i] + '</b>',
                              tooltip='<b><i>Click here to see junction name</i></b>',
                              icon=folium.Icon(color='green', icon='road')
                              ).add_to(req_plotting_variables[1])
            else:
                coordinates = graph.get_junctions_location(start=shortest_path[i],
                                                           end=shortest_path[i + 1])
                if coordinates == end_junc_coord:
                    return None
                else:
                    dict_road_coords[shortest_path[i]] = coordinates
                    folium.Marker(location=coordinates, popup='<b>' + shortest_path[i] + '</b>',
                                  tooltip='<b><i>Click here to see junction name</i></b>',
                                  icon=folium.Icon(color='gray', icon='road')
                                  ).add_to(req_plotting_variables[1])

    return None


def helper_plot_road_links(list_paths: list, colours: list, end: str, dict_road_coords: dict,
                           req_road_link_variables: list) -> None:
    """This is a helper method for visualize_multiple_path() method.
     The method iterates over the different junctions in a path and makes a link between the 2
     markers with the help of folium library plotting methods."""
    end_junc_coord = req_road_link_variables[0]
    j = 0
    for path in list_paths:
        if j >= len(colours):
            colour = random.choice(colours)
        else:
            colour = colours[j]
        for i in range(len(path) - 2):
            start_coord = dict_road_coords[path[i]]
            end_coord = dict_road_coords[path[i + 1]]

            coordinates = [start_coord, end_coord]
            if colour == 'pink':
                # Draw the link between each marker.
                folium.PolyLine(coordinates, tooltip='<b>Path between ' + path[i] + ' and'
                                ' ' + path[i + 1] + '</b>', color=colour, weight=4.5,
                                opacity=1
                                ).add_to(req_road_link_variables[1])
            else:
                # Draw the link between each marker.
                folium.PolyLine(coordinates, tooltip='<b>Path between ' + path[i] + ' and'
                                ' ' + path[i + 1] + '</b>', color=colour, weight=4.5,
                                opacity=0.5
                                ).add_to(req_road_link_variables[1])

        start_coord = dict_road_coords[path[-2]]
        coordinates = [start_coord, end_junc_coord]
        if colour == 'pink':
            folium.PolyLine(coordinates, popup='<b>Path traced between the 2 roads</b>',
                            tooltip='<b>Path between ' + path[-2] + ' and ' + end + '</b>',
                            color=colour, weight=4.5, opacity=1).add_to(req_road_link_variables[1])
        else:
            folium.PolyLine(coordinates, popup='<b>Path traced between the 2 roads</b>',
                            tooltip='<b>Path between ' + path[-2] + ' and ' + end + '</b>',
                            color=colour, weight=4.5, opacity=0.5
                            ).add_to(req_road_link_variables[1])
        j += 1
    return None


def helper_plot_shortest_road_links(shortest_path: list, end: str, end_junc_coord: list,
                                    dict_road_coords: dict, plot_map: folium) -> None:
    """This is a helper method for visualize_shortest_path(), visualize_direct_path() and
    visualize_path_specific_stops() methods.
     The method iterates over the different junctions in a path and makes a link between the 2
     markers with the help of folium library plotting methods."""
    for i in range(len(shortest_path) - 2):
        start_coord = dict_road_coords[shortest_path[i]]
        end_coord = dict_road_coords[shortest_path[i + 1]]

        coordinates = [start_coord, end_coord]
        # Draw the link between each marker.
        folium.PolyLine(coordinates, popup='<b></b>',
                        tooltip='<b>Path between ' + shortest_path[i] + ' and'
                        ' ' + shortest_path[i + 1] + '</b>', color='green', weight=4.5,
                        opacity=0.5).add_to(plot_map)

    start_coord = dict_road_coords[shortest_path[-2]]
    coordinates = [start_coord, end_junc_coord]

    folium.PolyLine(coordinates, popup='<b>Path traced between the 2 roads</b>',
                    tooltip='<b>Path between ' + shortest_path[-2] + ' and ' + end + '</b>',
                    color='green', weight=4.5, opacity=0.5).add_to(plot_map)
    return None


def helper_plot_time_road_links(shortest_time_path: list, time_between_juncs: list,
                                end: str, dict_road_coords: dict,
                                req_road_link_variables: list) -> None:
    """This is a helper method for visualize_shortest_path() and visualize_path_specific_stops()
     methods.
     The method iterates over the different junctions in a path and makes a link between the 2
     markers with the help of folium library plotting methods."""
    end_junc_coord = req_road_link_variables[0]
    for i in range(len(shortest_time_path) - 2):
        start_coord = dict_road_coords[shortest_time_path[i]]
        end_coord = dict_road_coords[shortest_time_path[i + 1]]

        coordinates = [start_coord, end_coord]
        # Draw the link between each marker.
        if isinstance(time_between_juncs[i], str):
            folium.PolyLine(coordinates, popup='<b>' + str(time_between_juncs[i]) + '</b>',
                            tooltip='<b>Path between ' + shortest_time_path[i] + ' and'
                            ' ' + shortest_time_path[i + 1] + '</b>', color='green', weight=4.5,
                            opacity=0.5).add_to(req_road_link_variables[1])
        else:
            folium.PolyLine(coordinates, popup='<b>' + str(time_between_juncs[i]) + ' hours </b>',
                            tooltip='<b>Path between ' + shortest_time_path[i] + ' and'
                            ' ' + shortest_time_path[i + 1] + '</b>', color='green', weight=4.5,
                            opacity=0.5).add_to(req_road_link_variables[1])

    start_coord = dict_road_coords[shortest_time_path[-2]]
    coordinates = [start_coord, end_junc_coord]

    folium.PolyLine(coordinates, popup='<b>' + str(time_between_juncs[-1]) + ' hours </b>',
                    tooltip='<b>Path between ' + shortest_time_path[-2] + ' and ' + end + '</b>',
                    color='green', weight=4.5, opacity=0.5).add_to(req_road_link_variables[1])
    return None


if __name__ == '__main__':
    # Certain visualizations to try for yourself!

    # Multiple paths

    # visualize_multiple_path('A406', 'LA Boundary', 10)
    # visualize_multiple_path('A23', 'LA Boundary', 10)
    # visualize_multiple_path('M1 spur', 'A223', 10)
    # visualize_multiple_path('LA Boundary', 'M1 spur', 10)

    # Shortest paths

    # visualize_shortest_path('LA Boundary', 'M1 spur')
    # visualize_shortest_path('M1 spur', 'A223')
    # visualize_shortest_path('A406', 'LA Boundary')
    # visualize_shortest_path('A23', 'LA Boundary')

    # Specific stops

    # visualize_path_specific_stops('A406', 'LA Boundary', 1)

    # Direct paths

    # visualize_direct_path('A406', 'LA Boundary')

    # Shortest Time Based stops

    # visualize_shortest_time_path('A406', 'M1 spur', 'cycle')

    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E9998'],
        'extra-imports': ['folium', 'random', 'classes', 'typing', 'computations'],
        'allowed-io': ['classes.get_junctions_location', 'classes.load_graph'],
        'max-nested-blocks': 5,
    })

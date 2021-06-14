"""CSC111 Final Project, Main file.

Our main file.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 by Aditya Shankar Sarma Peri, Praket Kanaujia,
Aakash Vaithyanathan, and Nazanin Ghazitabatabai.

This module is expected to use data from:
https://data.gov.uk/dataset/208c0e7b-353f-4e2d-8b7a-1a7118467acc/gb-road-traffic-counts.
The GB Road Traffic Counts is produced by the Department for Transport. The Department for Transport
collects traffic data to produce statistics on the level of traffic on roads in Great Britain,
last updated in October 2020."""

import interact


def overall() -> None:
    """Ask the user where they want to go? Recommend start junctions to the user
    to pick one from. Then ask how many places to stop by. Finally recommended end
    junctions to pick one from.
    Show the visualizations for direct path, all paths, and the most efficient path along
    with the total destination and time taken."""
    interact.visualize()


if __name__ == '__main__':
    overall()

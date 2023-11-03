from typing import List

from networkx import (
    astar_path, bellman_ford_path, dijkstra_path, single_source_dijkstra_path,
)

from .graph import build


def route_path(source: int, destination: int, mode="prefer_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> List[int]:
    """_summary_

    Args:
        source (int): From Solar System ID
        destination (int): To Solar System ID
        mode (str, optional): Weighting mode Defaults to "prefer_shortest". ["prefer_shortest", "prefer_safest", "prefer_less_safe"]
        algorithm (str, optional): Routing Function to use. Defaults to "astar" ["astar", "dijkstra", "bellman_ford"]
        edges (list, optional): Extra edges to load, example [(30100000, 30003841, {'prefer_shortest': 1.0, 'prefer_safest': 1.0, 'prefer_less_safe': 1.0}),]. Defaults to [].
        static_cache (bool, optional): Use Pregenerated Cache. Defaults to False.

    Returns:
        [int]: list of integer Solar System IDs
    """
    G = build(static_cache)
    if edges is not {}:
        G.add_edges_from(edges)

    if algorithm == "astar":
        return astar_path(build(static_cache), source, destination, weight=mode)
    elif algorithm == "dijkstra":
        return dijkstra_path(build(static_cache), source, destination, weight=mode)
    elif algorithm == "bellman_ford":
        return bellman_ford_path(build(static_cache), source, destination, weight=mode)
    else:
        return astar_path(build(static_cache), source, destination, weight=mode)


def route_length(source: int, destination: int, mode="prefer_shortest", algorithm="astar", edges: List = [], static_cache: bool = False) -> int:
    """_summary_

    Args:
        source (int): From Solar System ID
        destination (int): To Solar System ID
        mode (str, optional): Weighting mode Defaults to "prefer_shortest". ["prefer_shortest", "prefer_safest", "prefer_less_safe"]
        algorithm (str, optional): Routing Function to use. Defaults to "astar" ["dijkstra", "bellman_ford"]
        edges (list, optional): Extra edges to load, example [(30100000, 30003841, {'prefer_shortest': 1.0, 'prefer_safest': 1.0, 'prefer_less_safe': 1.0})]. Defaults to [].
        static_cache (bool, optional): Use Pregenerated Cache. Defaults to False.

    Returns:
        int : the number of JUMPS, this will be one shorter than route_path, as it includes the source system.
    """

    return len(route_path(source, destination, mode, algorithm, edges, static_cache)) - 1


def systems_range(source: int, range: int, mode="prefer_shortest", edges: list = [], static_cache: bool = False) -> List:
    list = [key for key in single_source_dijkstra_path(build(static_cache), source, range, weight=mode)]
    list.remove(source)
    return list

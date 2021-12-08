from typing import Dict, Tuple, Set, List, Callable
import random

from classes import *

# 1. Randomly distribute small amounts of pheromone (between 0 and 1) on the construction graph.

# def init_graph()

# Graph:
# Node:
# Connecting Nodes: List of Node

# List of nodes and edges list[set[node (other indices in the list): int]]
# List of pheromones (indices are nodes) list[pheromone: int]
# Paths: list[list[node: str]]
# Pheromone = 100 / fitness
# Fitness = difference between biggest bin and smallest bin

# 013211103
# k0b1, k1b2, k2b3

def create_bin_packing_graph(items: List[Item], bins: int) -> Graph:
    """
    Creates a graph to reflect a bin packing problem.

    "s" and "e" nodes are always created. Each node is created as "iXbY" where X
    is item's position in the list and Y is the bin index.

    Args:
        items (List[Item]): Number of items.
        bins (int): Number of bins to sort.

    Returns:
        (Graph): Graph object that contains the nodes and edges of the graph.
    """
    if (len(items) == 0):
        raise ValueError("No items to create nodes from.")

    if (bins == 0):
        raise ValueError("No bins to create nodes from.")

    nodes: Dict[str, Set[str]] = {}

    no_items = len(items)

    # Create nodes
    for i in range(no_items):
        for b in range(bins):
            nodes[f"i{i}b{b}"] = set()

    nodes["s"] = set()
    nodes["e"] = set()

    # Create links between nodes
    edges = set()

    ## Connect start node to initial next nodes
    for b in range(bins):
        nodes["s"].add(f"i0b{b}")
        edges.add(("s", f"i0b{b}"))
    
    for i in range(no_items):
        if i == no_items - 1:
            ## Connect to end node
            for b in range(bins):
                current_node = f"i{i}b{b}"
                
                nodes[current_node].add("e")
                edges.add((current_node, "e"))
        else:
            ## Connect to next item's nodes
            for pre_bin in range(bins):
                current_node = f"i{i}b{pre_bin}"

                for post_bin in range(bins):
                    next_node = f"i{i + 1}b{post_bin}"

                    nodes[current_node].add(next_node)
                    edges.add((current_node, next_node))

    return Graph(nodes, edges)


def convert_path_to_bins(items: List[Item], bins: int, path: List[str]) -> List[List[Item]]:
    """
    Converts a graph path into bins.

    Args:
        items (List[Item]): The list of items.
        bins (int): The number of bins we have.
        path (List[str]): The travelled nodes. Must start with 's' and end with 
            'e'. Path must start at item 0 (or the first item).

    Returns:
        (List[List[Item]]): A list of bins and their items.
    """
    if items is None or len(items) == 0:
        raise ValueError("Invalid items parameter given.")

    if bins == 0:
        raise ValueError("No bins given.")

    if path is None or len(path) == 0:
        raise ValueError("Invalid path given.")

    item_counter = 0
    bins = [ [] for _ in range(bins) ]

    # Ignore start and end nodes
    for node in path[1:-1]:
        item_bin = int(node.split('b')[1])
        item = items[item_counter]

        bins[item_bin].append(item)

        item_counter += 1

    return bins


def bin_weight(bin: List[Item]) -> int:
    """
    Get the total weight of a bin.

    Args:
        bin (List[Item]): List of bin items.

    Returns:
        (int): The total item weight.
    """
    if bin is None:
        raise ValueError("Bin was None.")

    weight = 0
    for item in bin:
        weight += item.weight

    return weight


def get_ant_colony_best_fitness(graph: Graph, evaluation_limit: int, evaporation_rate: float, fitness_function: Callable[[List[str]], int]) -> Tuple[List[str], int]:
    """
    Runs the ant colony optimisation (ACO) algorithm and returns the best 
    candidate path through the supplied nodes.

    Args:
        graph (Graph): The graph to evaluate.
        fitness_function (Callable[[List[str]], int]): A function that takes
            a candidate path and returns a fitness value for optimisation.

    Returns:
        (Tuple[List[str], int]): A tuple of the path taken and the fitness
            value for it.
    """
    graph = create_bin_packing_graph()
    # pheromone_table: Dict[Tuple[str, str], int] = create_pheromone_table(edges)
    # paths: List[List[str]] = generate_bin_packing_paths(nodes, path_limit)
    pass

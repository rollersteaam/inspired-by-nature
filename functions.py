import math
import random
from functools import reduce
from typing import Dict, Tuple, Set, List, Callable

from classes import *


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


def max_min_bin_diff_fitness(bins: List[List[Item]]) -> int:
    """
    Calculates the difference between the biggest and smallest bin. Can be used
    as a fitness function for ant colony optimisation.

    Args:
        bins (List[List[Item]]): A list of bins with items in.

    Returns:
        (int): The difference between the biggest and smallest bin.
    """
    smallest_bin: int = math.inf
    biggest_bin: int = 0

    for b in bins:
        weight = bin_weight(b)

        smallest_bin = weight if weight < smallest_bin else smallest_bin
        biggest_bin = weight if weight > biggest_bin else biggest_bin

    return biggest_bin - smallest_bin


def generate_paths_with_pheromones(graph: Graph, pheromone_table: Dict[Tuple[str, str], float], amount: int) -> List[List[str]]:
    """
    Generates a set of graph paths with a pheromone bias, paths with highest
    pheromone values are more likely to be travelled.

    Args:
        graph (Graph): The graph.
        pheromone_table (Dict[Tuple[str, str], float]): A dictionary mapping
            links between two nodes to a pheromone value.
        amount (int): The amount of paths to generate.

    Returns:
        (List[List[str]]): The generated paths.
    """
    paths = []

    for _ in range(amount):
        path = ["s"]
        current_node = "s"

        while current_node != "e":
            # Find the next best node to travel
            possible_nodes = graph.nodes[current_node]
            next_node = None

            # Create a table of "travel to node" probabilities
            pheromone_total = reduce(lambda sum, node: sum + pheromone_table[(current_node, node)], possible_nodes, 0)
            probability_table = []
            running_total = 0

            for node in possible_nodes:
                probability = pheromone_table[(current_node, node)] / pheromone_total
                running_total += probability
                probability_table.append((node, running_total))

            # TODO: Does this break sometimes because the final value may not be 1?

            # Randomly choose which node to travel to
            random_number = random.random()

            for pair in probability_table:
                probability = pair[1]

                if random_number <= probability:
                    node = pair[0]

                    next_node = node
                    break

            # Travel to the node
            path.append(next_node)
            current_node = next_node

        # Submit path
        paths.append(path)

    return paths


def get_bin_packing_ant_colony_best_fitness(graph: Graph, items: List[Item], bins: int, per_loop_limit: int, evaluation_limit: int, evaporation_rate: float, fitness_function: Callable[[List[List[Item]], int], int]) -> Tuple[List[str], int]:
    """
    Runs the ant colony optimisation (ACO) algorithm for bin packing
    and returns the best candidate path through the supplied nodes.

    Args:
        graph (Graph): The graph to evaluate.
        items (List[Item]): The items used for the bin packing problem.
        bins (int): The amount of bins to sort into.
        per_loop_limit (int): How many paths to traverse per loop before
            evaporation.
        evaluation_limit (int): Maximum number of fitness evaluations overall.
        evaporation_rate (float): The amount to reduce pheromones by after
            a loop of evaluations.
        fitness_function (Callable[[List[List[Item]], int]): A function that 
            takes a list of bins and returns a fitness value for optimisation.

    Returns:
        (Tuple[List[str], int]): A tuple of the path taken and the fitness
            value for it.
    """
    pheromone_table: Dict[Tuple[str, str], float] = {}
    total_evaluations = 0

    best_fitness = math.inf
    best_path: List[List[str]] = None

    while total_evaluations < evaluation_limit:
        # 1. Randomly distribute small amounts of pheromone.
        for edge in graph.edges:
            pheromone_table[edge] = 1 * random.random()

        # 2. Generate a set of ant paths from S (start) to E (end)
        paths = generate_paths_with_pheromones(graph, pheromone_table, per_loop_limit)

        # 3. Update the pheromone in your pheromone table for each ant’s path according to its fitness.
        for path in paths:
            bin_list = convert_path_to_bins(items, bins, path)
            fitness = fitness_function(bin_list)
            pheromone = 100 / fitness

            if fitness < best_fitness:
                best_fitness = fitness
                best_path = path

            ## Add the pheromone to each edge in the path
            for r in range(len(path) - 1):
                current_node = path[r]
                next_node = path[r + 1]

                pheromone_table[(current_node, next_node)] += pheromone

        # 4. Evaporate the pheromone for all links in the graph.
        for edge in graph.edges:
            pheromone_table[edge] *= evaporation_rate

        total_evaluations += per_loop_limit

    return best_path, best_fitness


    # Generating Ant Paths: An ant will traverse your construction graph by making a decision at each new item it comes to (i.e. an ant at S can choose to go to bin 1, 2 or 3 in the illustration above). This selection is made at random, but biased by the amount of pheromone on the choices ahead (e.g. if an ant is placed at position S and bin 1 has a pheromone value of 0.5, bin 2 has a pheromone value of 0.8 and bin 3 has a pheromone value of 0.1, the ant should have a 5/14 chance of selecting bin 1, an 8/14 chance of selecting bin 2, and a 1/14 chance of selecting bin 3). This should be repeated for all k variables and b bins. There is no local heuristic for this implementation.

# for node, connections in nodes.items():
#     # print(f"Node {node} connects to {connections}")
#     set_iter = iter(connections)
#     print(f"       /------>{next(set_iter)}")
#     print("      /")
#     print("     /")
#     print(f"{node} ------>{next(set_iter)}")
#     print("     /")
#     print("      /")
#     print(f"       /------>{next(set_iter)}")
#     print("")

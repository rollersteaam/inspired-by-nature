from typing import Dict, Set, Tuple


class Item:
    def __init__(self, weight: int):
        self.weight = weight
    
    def __str__(self) -> str:
        return f"{self.weight}"

    def __repr__(self):
        return f"{self.weight}"


class Graph:
    def __init__(self, nodes: Dict[str, Set[str]], edges: Set[Tuple[str, str]]):
        """
        A graph object.

        Args:
            nodes (Dict[str, Set[str]]): A dictionary of nodes in the graph,
                mapping to a set of nodes a node is connected to.
            edges (Set[Tuple[str, str]]): The edges of the graph. Each tuple
                shows an edge in the graph.
        """
        self.nodes = nodes
        self.edges = edges

import random

from functions import *

items = [ random.randint(1, 50) for _ in range(0, 50) ]
bins = 3
path_limit = 10000

graph = create_bin_packing_graph(items, bins)

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

bins = convert_path_to_bins([Item(10), Item(20), Item(30)], 3, ["s", "i0b0", "i1b1", "i2b1", "e"])

print(bin_weight(bins[0]))
print(bin_weight(bins[1]))
print(bin_weight(bins[2]))
# print(get_ant_colony_best_fitness(graph, path_limit, 0.5, lambda x))

# 2. Generate a set of p ant paths from S (start) to E (end) (where p is a variable and specified below).


# 3. Update the pheromone in your pheromone table for each ant’s path according to its fitness.


# 4. Evaporate the pheromone for all links in the graph.

# Termination Criterion: When the algorithm has reached a maximum number of fitness evaluations (generated paths). The result is then the fitness of the best ant in the population at the end.

# Generating Ant Paths: An ant will traverse your construction graph by making a decision at each new item it comes to (i.e. an ant at S can choose to go to bin 1, 2 or 3 in the illustration above). This selection is made at random, but biased by the amount of pheromone on the choices ahead (e.g. if an ant is placed at position S and bin 1 has a pheromone value of 0.5, bin 2 has a pheromone value of 0.8 and bin 3 has a pheromone value of 0.1, the ant should have a 5/14 chance of selecting bin 1, an 8/14 chance of selecting bin 2, and a 1/14 chance of selecting bin 3). This should be repeated for all k variables and b bins. There is no local heuristic for this implementation.

# Pheromone Update: Once the fitness has been computed, the pheromone must be updated accordingly. With the bin packing problem, we want to reward paths that lead to bin packs with smaller differences. Therefore the pheromone update for the path will be 100/fitness.

# Pheromone Evaporation: Finally, the pheromone on all paths must be evaporated. This is achieved simply by multiplying all paths within the construction graph by the evaporation rate e (specified below).

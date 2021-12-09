import random

from functions import *

items = [ Item(random.randint(1, 50)) for _ in range(0, 50) ]
bins = 3
per_loop_limit = 100
path_limit = 10000
evaporation_rate = 0.5

graph = create_bin_packing_graph(items, bins)

# bins = convert_path_to_bins(
#     items=[Item(10), Item(20), Item(30), Item(15)],
#     bins=3,
#     path=["s", "i0b0", "i1b1", "i2b1", "i3b2", "e"]
# )

# print(bin_weight(bins[0]))
# print(bin_weight(bins[1]))
# print(bin_weight(bins[2]))
# print(max_min_bin_diff_fitness(bins))

best_fitness = get_bin_packing_ant_colony_best_fitness(graph, items, bins, per_loop_limit, path_limit, evaporation_rate, max_min_bin_diff_fitness)

print(best_fitness)


import random

from functions import *

for _ in range(5):
    items = [ Item(weight) for weight in range(1, 501) ]
    bins = 10
    per_loop_limit = 100
    path_limit = 10000
    evaporation_rate = 0.5

    graph = create_bin_packing_graph(items, bins)

    path, best_fitness = get_bin_packing_ant_colony_best_fitness(graph, items, bins, per_loop_limit, path_limit, evaporation_rate, max_min_bin_diff_fitness)

    print(path)

    print(f"Fitness: {best_fitness}")

    bins = convert_path_to_bins(items, bins, path)
    print_bins(bins)

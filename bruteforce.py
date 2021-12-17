import copy
import math
import time
import classes as cl


def brute_solve(network: cl.Network) -> cl.Network:
    start = time.time()
    print("Bruteforce started!")

    # Get all possible permutations of paths
    possibilities = cl.Possibilities(network)

    iteration = cl.Iteration(possibilities)
    print(str(len(iteration.values)) + "; " + str(iteration.values))
    best_solution = Solution(math.inf, [])

    iteration.update_progress(0, 'infinity')
    # For every permutation calculate load on links and how many modules are needed to accommodate this load
    # Select best solution - can be multiple ones
    while iteration.next_iteration(str(best_solution.cost)):
    # iteration.next_iteration(str(best_solution.cost))
        competing_solution = calculate_modules_cost(network, iteration.values)
        best_solution = best_solution.compare(competing_solution)

    iteration.update_progress(1, str(best_solution.cost))
    end = time.time()

    print()
    print("Number of possible solutions is {}:".format(len(best_solution.values)))
    for solveNumber in range(len(best_solution.values)):
        best_solution.print(network, solveNumber)

    print("Calculations took: {}".format(end - start))

    for demand in range(len(best_solution.values[0])):
        for path in range(len(best_solution.values[0][0])):
            try:
                network.demands_list[demand].demand_path_list[path].solution_path_signal_count = best_solution.values[0][demand][path]
            except IndexError:
                # Should be only printed in debug
                print("IndexError number of paths for demand {} is shorter then max {}".format(demand, network.longest_demand_path))

    network.update_link_capacity()
    for link in network.links_list:
        link.print_result()
    return network


class Solution(object):
    def __init__(self, cost: float, values: []):
        self.cost = cost
        self.values = values

    def compare(self, other):
        if other.cost < self.cost:
            return other
        elif other.cost == self.cost:
            self.append(other.values[0])
            return self
        else:
            return self

    def append(self, new_solution: []):
        self.values.append(new_solution)

    def print(self, network: cl.Network, solve_number: int):

        row_format = "{:<7}" + "{:^5}" * network.number_of_demands
        demand_list = ["[%s]" % x for x in range(1, network.number_of_demands + 1)]
        path_list = ["[%s]" % x for x in range(1, network.longest_demand_path + 1)]
        transposed_data = zip(*self.values[solve_number])

        print('Routes: \\ Demands:')
        print(row_format.format("", *demand_list))
        for path_id, row in enumerate(transposed_data):
            print(row_format.format(path_list[path_id], *row))
        print(row_format.format("h(d):",
                                *[network.demands_list[x].demand_volume for x in range(len(network.demands_list))]))
        print("Solution cost: {}".format(self.cost))
        print("Is solution valid: {}".format(self.validate(network, solve_number)))
        print()

    def validate(self, network: cl.Network, solve_number: int):
        valid = True
        for demand in range(len(self.values[solve_number])):
            demand_passed = sum(self.values[solve_number][demand])
            valid = valid and (demand_passed >= network.demands_list[demand].demand_volume)

        return valid


def calculate_modules_cost(network, flow_array) -> Solution:
    modules_cost = 0
    load = calculate_links_load(network, flow_array)
    for linkId in range(0, network.number_of_links):
        link = network.links_list[linkId]
        # Check if link is not overloaded
        if load[linkId] < link.maximum_number_of_modules * link.single_module_capacity:
            modules_used = math.ceil(load[linkId] / link.single_module_capacity)
            modules_cost = modules_cost + modules_used * link.module_cost
    return Solution(modules_cost, [copy.deepcopy(flow_array)])


def calculate_links_load(network, flow_array):
    load = [0] * network.number_of_links
    for demand in range(0, network.number_of_demands):
        for path in range(0, network.demands_list[demand].number_of_demand_paths):
            flows_running_this_path = flow_array[demand][path]
            for linkInPath in network.demands_list[demand].demand_path_list[path].link_list:
                load[linkInPath - 1] = load[linkInPath - 1] + flows_running_this_path
    return load
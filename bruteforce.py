import copy
import math
import time
import classes as cl


def brute_solve_ddap(network: cl.Network) -> cl.Network:
    start = time.time()
    possibilities = cl.Possibilities(network)   # Get all possible permutations of paths
    iteration = cl.Iteration(possibilities)
    #print(str(len(iteration.values)) + "; " + str(iteration.values))  #pokazuje wektory rozwiązania
    best_solution = Solution(math.inf, [])
    iteration.update_progress(0, 'nieskończoność')
    # For every permutation calculate load on links and how many modules are needed to accommodate this load
    # Select best solution - can be multiple ones
    while iteration.next_iteration(str(best_solution.cost)):
        competing_solution = calculate_modules_cost(network, iteration.values)
        best_solution = best_solution.compare(competing_solution)

    iteration.update_progress(1, str(best_solution.cost))
    end = time.time()
    print("\nLiczba możliwych rozwiązań: {}:".format(len(best_solution.values)))
    for solveNumber in range(len(best_solution.values)):
        best_solution.print(network, solveNumber)
    print("Obliczenia zajęły: {}".format(end - start))

    for demand in range(len(best_solution.values[0])):
        for path in range(len(best_solution.values[0][0])):
            try:
                network.demands[demand].list_of_demand_paths[path].solution_path_signal_count = \
                best_solution.values[0][demand][path]
            except IndexError:
                print()
                #print("IndexError number of paths for demand {} is shorter then max {}".format(demand,network.longest_demand_path))
    network.update_link_capacity()
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

        row_format = "{:<7}" + "{:^5}" * len(network.demands)
        demand_list = ["[%s]" % x for x in range(1, len(network.demands) + 1)]
        path_list = ["[%s]" % x for x in range(1, network.longest_demand_path + 1)]
        transposed_data = zip(*self.values[solve_number])

        print('Routes: \\ Demands:')
        print(row_format.format("", *demand_list))
        for path_id, row in enumerate(transposed_data):
            print(row_format.format(path_list[path_id], *row))
        print(row_format.format("h(d):",
                                *[network.demands[x].demand_volume for x in range(len(network.demands))]))
        print("Koszt rozwiązania: {}".format(self.cost))
        print("Czy rowiązanie poprawne: {}".format(self.validate(network, solve_number)))
        print()

    def validate(self, network: cl.Network, solve_number: int):
        valid = True
        for demand in range(len(self.values[solve_number])):
            demand_passed = sum(self.values[solve_number][demand])
            valid = valid and (demand_passed >= network.demands[demand].demand_volume)

        return valid


def calculate_modules_cost(network, flow_array) -> Solution:
    modules_cost = 0
    load = calculate_links_load(network, flow_array)
    for linkId in range(0, len(network.links)):
        link = network.links[linkId]
        # Check if link is not overloaded
        if load[linkId] < int(link.number_of_modules) * int(link.link_module):
            modules_used = math.ceil(load[linkId] / int(link.link_module))
            modules_cost = modules_cost + modules_used * int(link.module_cost)
    return Solution(modules_cost, [copy.deepcopy(flow_array)])


def calculate_links_load(network, flow_array):
    load = [0] * len(network.links)
    for demand in range(0, len(network.demands)):
        for path in range(0, network.demands[demand].number_of_demand_paths):
            flows_running_this_path = flow_array[demand][path]
            for linkInPath in network.demands[demand].list_of_demand_paths[path].links_in_path:
                load[linkInPath - 1] = load[linkInPath - 1] + flows_running_this_path
    return load


def brute_solve_dap(network: cl.Network) -> cl.Network:
    start = time.time()
    possibilities = cl.Possibilities(network)   # Get all possible permutations of paths
    iteration = cl.Iteration(possibilities)
    #print(str(len(iteration.values)) + "; " + str(iteration.values))  #pokazuje wektory rozwiązania
    best_solution = DAPSolution(math.inf, [])
    iteration.update_progress(0, 'inf')
    # For every permutation calculate load on links and how many modules are needed to accommodate this load
    # Select best solution - can be multiple ones
    while iteration.next_iteration(str(best_solution.cost)):
        competing_solution = calculate_dap_cost(network, iteration.values)
        best_solution = best_solution.compare(competing_solution)

    iteration.update_progress(1, str(best_solution.cost))
    end = time.time()
    print("\nLiczba możliwych rozwiązań: {}:".format(len(best_solution.values)))
    for solveNumber in range(len(best_solution.values)):
        best_solution.print(network, solveNumber)
    print("Obliczenia zajęły: {}".format(end - start))

    for demand in range(len(best_solution.values[0])):
        for path in range(len(best_solution.values[0][0])):
            try:
                network.demands[demand].list_of_demand_paths[path].solution_path_signal_count = \
                best_solution.values[0][demand][path]
            except IndexError:
                print()
    network.update_link_capacity()
    return network


class DAPSolution(object):
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

        row_format = "{:<7}" + "{:^5}" * len(network.demands)
        demand_list = ["[%s]" % x for x in range(1, len(network.demands) + 1)]
        path_list = ["[%s]" % x for x in range(1, network.longest_demand_path + 1)]
        transposed_data = zip(*self.values[solve_number])

        print('Routes: \\ Demands:')
        print(row_format.format("", *demand_list))
        for path_id, row in enumerate(transposed_data):
            print(row_format.format(path_list[path_id], *row))
        print(row_format.format("h(d):",
                                *[network.demands[x].demand_volume for x in range(len(network.demands))]))
        print("Koszt rozwiązania: {}".format(self.cost))
        print("Czy rowiązanie poprawne: {}".format(self.validate(network, solve_number)))
        print()

    def validate(self, network: cl.Network, solve_number: int):
        valid = True
        for demand in range(len(self.values[solve_number])):
            demand_passed = sum(self.values[solve_number][demand])
            valid = valid and (demand_passed >= network.demands[demand].demand_volume)

        return valid

def calculate_dap_cost(network, flow_array) -> DAPSolution:
    #print(flow_array)
    cost = 0
    load = calculate_links_load(network, flow_array)
    f = [0 for i in range(len(load))] #przeciążenie DAP
    for e in range(len(load)):
        f[e] = load[e] - int(network.links[e].number_of_modules) * int(network.links[e].link_module)
    cost = max(f)
    return DAPSolution(cost, [copy.deepcopy(flow_array)])

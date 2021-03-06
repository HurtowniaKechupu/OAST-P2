import sys
import itertools
import math


class Link:
    def __init__(self, start_node, end_node, number_of_modules, module_cost, link_module):
        self.start_node = start_node
        self.end_node = end_node
        self.number_of_modules = number_of_modules
        self.module_cost = module_cost
        self.link_module = link_module

    def print_link(self):
        print("Start: {}, End: {}, Number of modules: {}, Module cost: {}, Link module: {}"
              .format(self.start_node, self.end_node, self.number_of_modules, self.module_cost, self.link_module))


class Demand:
    def __init__(self, demand_data, demand_number):
        self.start_node = demand_data[0]
        self.end_node = demand_data[1]
        self.demand_volume = int(demand_data[2])
        self.demand_number = demand_number
        self.list_of_demand_paths = []
        self.number_of_demand_paths = len(self.list_of_demand_paths)

    def print_demand(self, number_of_demand_paths):
        print("Start: {}, End: {}, Demand: {}, Demand number: {}"
              .format(self.start_node, self.end_node, self.demand_volume, self.demand_number))
        for i in range(0, number_of_demand_paths):
            self.list_of_demand_paths[i].print_demand_path()
        self.number_of_demand_paths = len(self.list_of_demand_paths)


class DemandPath:
    def __init__(self, demand_path_data, demand_number):
        self.demand_path_id = demand_path_data[0]
        self.number_of_demand = demand_number
        self.links_in_path = [int(link_id) for link_id in demand_path_data[1:]]

    def print_demand_path(self):
        print("Demand id: {}, Path: {}"
              .format(self.demand_path_id, self.links_in_path))


class Network:
    def __init__(self):
        self.links = []
        self.demands = []
        self.longest_demand_path = []

    def update_link_capacity(self):
        for link in self.links:
            link.number_of_signals = 0
            link.number_of_fibers = 0
            for demand in self.demands:
                for path in demand.list_of_demand_paths:
                    if link in path.links_in_path and path.solution_path_signal_count != 0:
                        link.number_of_signals = link.number_of_signals + 1
                        link.number_of_fibers = math.ceil(link.number_of_signals / link.single_module_capacity)


class Gene:
    def __init__(self, list_of_a, demand_volume):
        self.list_of_a = list_of_a
        self.demand_volume = demand_volume


class Chromosome:
    def __init__(self, list_of_genes, dap_fitness, ddap_fitness):
        self.list_of_genes = list_of_genes
        self.dap_fitness = dap_fitness
        self.ddap_fitness = ddap_fitness


class PathIteration(object):
    def find_combinations_util(self, arr, index, buckets, num, reduced_num, output):
        if reduced_num < 0:
            return

        # Je??li znaleziono to print
        if reduced_num == 0:
            curr_array = [0] * buckets
            curr_array[:index] = arr[:index]
            all_perm = list(itertools.permutations(curr_array))
            for solution in set(all_perm):
                output.append(solution)
            return

        prev = 1 if (index == 0) else arr[index - 1]
        for k in range(prev, num + 1):
            if index >= buckets:
                return
            arr[index] = k

            self.find_combinations_util(arr, index + 1, buckets, num,
                                        reduced_num - k, output)

    def find_combinations(self, n, buckets):
        output = []
        arr = [0] * buckets
        self.find_combinations_util(arr, 0, buckets, n, n, output)
        return output


class Possibilities(object):
    def __init__(self, network: Network):
        self.possibilities = []
        for demand in network.demands:
            path_iter = PathIteration()
            iter_for_demand = path_iter.find_combinations(demand.demand_volume, demand.number_of_demand_paths)
            for id, perm in enumerate(iter_for_demand):
                if len(perm) < network.longest_demand_path:
                    new_tuple = perm + tuple([0] * (network.longest_demand_path - len(perm)))
                    iter_for_demand[id] = new_tuple
            self.possibilities.append(iter_for_demand)

        self.number_of_demands = len(self.possibilities)
        self.longest_route = network.longest_demand_path

    def __getitem__(self, y):
        return self.possibilities[y]


class Iteration(object):
    def __init__(self, possibilities: Possibilities):
        self.possibilities = possibilities
        self.values = []
        self.state = [0] * self.possibilities.number_of_demands
        for i in range(0, self.possibilities.number_of_demands):
            self.values.append([0] * self.possibilities.longest_route)

    def next_iteration(self, modules_used: str):
        for i in reversed(range(0, self.possibilities.number_of_demands)):
            if self.state[i] < len(self.possibilities[i]) - 1:
                self.state[i] = self.state[i] + 1
                self.set_values()
                return True
            elif self.state[i - 1] < len(self.possibilities[i - 1]) - 1:
                self.state[i - 1] = self.state[i - 1] + 1
                self.state[i:] = [0] * (self.possibilities.number_of_demands - i)
                if i == 1:
                    self.update_progress(self.state[0] / len(self.possibilities[0]), modules_used)
                self.set_values()
                return True
        return False

    def set_values(self):
        for i in range(0, self.possibilities.number_of_demands):
            self.values[i] = self.possibilities[i][self.state[i]]

    # Wy??wietla post??p
    def update_progress(self, progress, modules: str):
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "b????d: \r\n"
        if progress < 0:
            progress = 0
            status = "Stop...\r\n"
        if progress >= 1:
            progress = 1
            status = "Zako??czono.\r\n"

        text = "\rWykorzystane modu??y: [{2}], Post??p: {0}% {1}".format(progress * 100, status, modules)

        sys.stdout.write(text)
        sys.stdout.flush()
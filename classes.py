class Link:
    def __init__(self, start_node, end_node, number_of_modules, module_cost, link_module):
        self.start_node = start_node
        self.end_node = end_node
        self.number_of_modules = number_of_modules
        self.module_cost = module_cost
        self.link_module = link_module

    def print_link(self):
        print("Start node: {}, End node: {}, Number of modules: {}, Module cost: {}, Link module: {}"
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
        print("Start node: {}, End node: {}, Demand volume: {}, Demand number: {}"
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
        print("Demand path id: {}, Path: {}"
              .format(self.demand_path_id, self.links_in_path))


class Network:
    def __init__(self):
        self.links = []
        self.demands = []


class Gene:
    def __init__(self, list_of_a, demand_volume):
        self.list_of_a = list_of_a
        self.demand_volume = demand_volume


class Chromosome:
    def __init__(self, list_of_genes, dap_fitness, ddap_fitness):
        self.list_of_genes = list_of_genes
        self.dap_fitness = dap_fitness
        self.ddap_fitness = ddap_fitness

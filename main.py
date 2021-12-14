import classes as cl
import evolution as evo
import time
import random

def check_if_stop():
    if stop_criterium == "1":
        return duration < MAX_TIME
    elif stop_criterium == "2":
        return iteration < MAX_GENERATIONS
    elif stop_criterium == "3":
        return mutations < MAX_MUTATIONS
    elif stop_criterium == "4":
        return not_improved_iteration < MAX_NOT_IMPROVED
    else:
        return False


# Default variables
MAX_TIME = 200
MAX_GENERATIONS = 250
MAX_MUTATIONS = 500
MAX_NOT_IMPROVED = 10

INITIAL_POPULATION = 100
CROSSOVER_PROBABILITY = 0.65
MUTATION_PROBABILITY = 0.15
SEED = 2137

duration = 0
iteration = 0
mutations = 0
not_improved_iteration = 0

# UI
option = 0
while True:
    option = input('Wybierz plik:\n1. net4.txt \n2. net12_1.txt \n3. net12_2.txt: ')
    if option == "1":
        file = "./Dane/net4.txt"
        break
    elif option == "2":
        file = "./Dane/net12_1.txt"
        break
    elif option == "3":
        file = "./Dane/net12_2.txt"
        break
    else:
        print("Nieprawidłowy plik! Wybierz ponownie.")

try:
    INITIAL_POPULATION = int(input("\nPopulacja początkowa (int): "))
except ValueError:
    print(f"Nieprawidłowa wartość! Wczytano domyślną: {INITIAL_POPULATION}")
    INITIAL_POPULATION = INITIAL_POPULATION
try:
    CROSSOVER_PROBABILITY = float(input("Prawdopodobieństwo krzyżowania (float): "))
except ValueError:
    print(f"Nieprawidłowa wartość! Wczytano domyślną: {CROSSOVER_PROBABILITY}")
    CROSSOVER_PROBABILITY = CROSSOVER_PROBABILITY
try:
    MUTATION_PROBABILITY = float(input("Prawdopodobieństwo mutacji (float): "))
except ValueError:
    print(f"Nieprawidłowa wartość! Wczytano domyślną: {MUTATION_PROBABILITY}")
    MUTATION_PROBABILITY = MUTATION_PROBABILITY
try:
    SEED = int(input("Ziarno dla generatora liczb pseudolosowych (int): "))
except ValueError:
    print(f"Nieprawidłowa wartość! Wczytano domyślną: {SEED} \n")
    SEED = SEED


while True:
    stop_criterium = input(
        "Wybierz kryterium stopu: \n1. Czas\n2. Liczba generacji\n3. Liczba mutacji\n4. Brak poprawy najlepszego rozwiązania w kolejnych N iteracjach:  ")
    if stop_criterium == "1":
        try:
            MAX_TIME = int(input("Liczba sekund: "))
        except ValueError:
            print(f"Nieprawidłowa wartość! Wczytano domyślną: {MAX_TIME} \n")
            MAX_TIME = MAX_TIME
        break
    elif stop_criterium == "2":
        try:
            MAX_GENERATIONS = int(input("Liczba generacji: "))
        except ValueError:
            print(f"Nieprawidłowa wartość! Wczytano domyślną: {MAX_GENERATIONS} \n")
            MAX_GENERATIONS = MAX_GENERATIONS
        break
    elif stop_criterium == "3":
        try:
            MAX_MUTATIONS = int(input("Liczba mutacji: "))
        except ValueError:
            print(f"Nieprawidłowa wartość! Wczytano domyślną: {MAX_MUTATIONS} \n")
            MAX_MUTATIONS = MAX_MUTATIONS
        break
    elif stop_criterium == "4":
        try:
            MAX_NOT_IMPROVED = int(input("Liczba iteracji: "))
        except ValueError:
            print(f"Nieprawidłowa wartość! Wczytano domyślną: {MAX_NOT_IMPROVED} \n")
            MAX_NOT_IMPROVED = MAX_NOT_IMPROVED
        break
    else:
        print("Błędne kryterium stopu! Wybierz ponownie.")


network = cl.Network()

#parser
with open(file, "r") as f:
    number_of_links = int(f.readline())

    for line in range(number_of_links):
        link_data = f.readline().strip().split(" ")
        link = cl.Link(link_data[0], link_data[1], link_data[2], link_data[3], link_data[4])
        network.links.append(link)
        link.print_link()

    for x in range(2):
        f.readline()

    number_of_demands = int(f.readline().strip())
    f.readline()

    for demand_number in range(number_of_demands):
        demand_data = f.readline().strip().split(" ")
        demand = cl.Demand(demand_data=demand_data, demand_number=demand_number + 1)
        number_of_demand_paths = int(f.readline())

        for line in range(number_of_demand_paths):
            demand_path_data = f.readline().strip().split(" ")
            demand_path = cl.DemandPath(demand_path_data=demand_path_data, demand_number=demand_number + 1)
            demand.list_of_demand_paths.append(demand_path)

        network.demands.append(demand)
        demand.print_demand(number_of_demand_paths)
        f.readline()

#start
random.seed(SEED)
first_population = evo.gen_first_population(network.demands, INITIAL_POPULATION)
current_population = first_population
evo.calc_fitness(network.links, network.demands, current_population)
for chromosome in first_population:
    for gene in chromosome.list_of_genes:
        print(gene.list_of_a)
    print("Funkcja kosztu DAP:" + str(chromosome.fitness_dap))
    print("Funkcja kosztu DDAP:" + str(chromosome.fitness_ddap))

#początek algorytmu
counter = 1
best_dap = chromosome.fitness_dap
best_ddap = chromosome.fitness_ddap
while check_if_stop():
    start = time.time()
    old_ddap = current_population[0].fitness_ddap
    old_dap = current_population[0].fitness_dap
    new_population = evo.do_cross(current_population, CROSSOVER_PROBABILITY)

    for chromosome in new_population:
        if evo.do_mutation(chromosome, MUTATION_PROBABILITY):
            mutations += 1

    print("\n----> Generacja nr", counter)
    counter += 1
    x, y = evo.calc_fitness(network.links, network.demands, new_population)
    if x < best_dap:
        best_dap = x
    if y < best_ddap:
        best_ddap = y

    new_population.sort(key=lambda x: x.fitness_ddap, reverse=False)

    if old_ddap >= new_population[1].fitness_ddap and old_dap >= new_population[1].fitness_dap:
        not_improved_iteration += 1

    sliced_population = new_population[:INITIAL_POPULATION]
    current_population = sliced_population
    end = time.time()
    iteration += 1
    duration += end - start

# Koniec algorytmu (wypisanie wartości końcowych)
print("\n----------------------------------------------")
print("Liczba generacji: " + str(iteration))
print("Liczba mutacji: " + str(mutations))
print("Czas działania: " + str(duration))
print("\nNajlepsza funkcja kosztu DAP:", best_dap)
print("Najlepsza funkcja kosztu DDAP:", best_ddap)
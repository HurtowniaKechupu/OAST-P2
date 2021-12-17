import classes as cl
import evolution as evo
import bruteforce as bf
import time
import random

def check_if_stop():
    if stop_criterium == "1":
        return duration < max_time
    elif stop_criterium == "2":
        return iteration < max_generations
    elif stop_criterium == "3":
        return mutations < max_mutations
    elif stop_criterium == "4":
        return not_improved_iteration < max_not_improved
    else:
        return False


# Default variables
max_time = 200
max_generations = 250
max_mutations = 500
max_not_improved = 10

initial_population = 100
crossover_probability = 0.65
mutation_probability = 0.15
seed = 2137

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


mode = 0
while True:
    mode = input("\nWybierz algorytm:\n1. Brute Force \n2. Algorytm Ewolucyjny")
    if mode == "1":
        break
    elif mode == "2":
        break
    else:
        print(f"Nieprawidłowa wartość! Wczytano domyślnie algorytm Brute Force")

if mode == "1":
    #print("Brute Force")
    #DAP:
    #liczba_xow = 0
    #for demand in network.demands:
        #liczba_xow = liczba_xow + demand.number_of_demand_paths
    bf.brute_solve(network)

elif mode == "2":
    try:
        initial_population = int(input("\nPopulacja początkowa (int): "))
    except ValueError:
        print(f"Nieprawidłowa wartość! Wczytano domyślną: {initial_population}")
        initial_population = initial_population
    try:
        crossover_probability = float(input("Prawdopodobieństwo krzyżowania (float): "))
    except ValueError:
        print(f"Nieprawidłowa wartość! Wczytano domyślną: {crossover_probability}")
        crossover_probability = crossover_probability
    try:
        mutation_probability = float(input("Prawdopodobieństwo mutacji (float): "))
    except ValueError:
        print(f"Nieprawidłowa wartość! Wczytano domyślną: {mutation_probability}")
        mutation_probability = mutation_probability
    try:
        seed = int(input("Ziarno dla generatora liczb pseudolosowych (int): "))
    except ValueError:
        print(f"Nieprawidłowa wartość! Wczytano domyślną: {seed} \n")
        seed = seed


    while True:
        stop_criterium = input(
            "Wybierz kryterium stopu: \n1. Czas\n2. Liczba generacji\n3. Liczba mutacji\n4. Brak poprawy najlepszego rozwiązania w kolejnych N iteracjach:  ")
        if stop_criterium == "1":
            try:
                max_time = int(input("Liczba sekund: "))
            except ValueError:
                print(f"Nieprawidłowa wartość! Wczytano domyślną: {max_time} \n")
                max_time = max_time
            break
        elif stop_criterium == "2":
            try:
                max_generations = int(input("Liczba generacji: "))
            except ValueError:
                print(f"Nieprawidłowa wartość! Wczytano domyślną: {max_generations} \n")
                max_generations = max_generations
            break
        elif stop_criterium == "3":
            try:
                max_mutations = int(input("Liczba mutacji: "))
            except ValueError:
                print(f"Nieprawidłowa wartość! Wczytano domyślną: {max_mutations} \n")
                max_mutations = max_mutations
            break
        elif stop_criterium == "4":
            try:
                max_not_improved = int(input("Liczba iteracji: "))
            except ValueError:
                print(f"Nieprawidłowa wartość! Wczytano domyślną: {max_not_improved} \n")
                max_not_improved = max_not_improved
            break
        else:
            print("Błędne kryterium stopu! Wybierz ponownie.")




    #start
    random.seed(seed)
    first_population = evo.gen_first_population(network.demands, initial_population)
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
        new_population = evo.do_cross(current_population, crossover_probability)

        for chromosome in new_population:
            if evo.do_mutation(chromosome, mutation_probability):
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

        sliced_population = new_population[:initial_population]
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
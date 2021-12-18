import classes as cl
from math import ceil
import random


# Oblicza i zwraca funcję celu
def calc_fitness(links, demands, population):
    for chromosome in population:
        l = [0 for i in range(len(links))]  #ładowanie sciezek
        y = [0 for i in range(len(links))]  #pojemnosc dla DDAP
        f = [0 for i in range(len(links))]  #przeciazenie DAP
        chromosome.fitness_ddap = 0
        chromosome.fitness_dap = 0

        for d in range(len(chromosome.list_of_genes)):
            for p in range(len(chromosome.list_of_genes[d].list_of_a)):
                for e in range(len(links)):
                    if check_demand(e + 1, demands[d], p):
                        l[e] += chromosome.list_of_genes[d].list_of_a[p]
        for e in range(len(links)):
            y[e] = ceil(l[e] / int(links[e].link_module))
            f[e] = l[e] - int(links[e].number_of_modules) * int(links[e].link_module)
            chromosome.fitness_ddap += y[e] * int(links[e].module_cost)
        chromosome.fitness_dap = max(f)
    print("Rozmiary łączy: ", y)
    print("Obciążenia łączy: ", l)
    print("Funkcja kosztu DAP: ", chromosome.fitness_dap)
    print("Funkcja kosztu DDAP: ", chromosome.fitness_ddap)
    return chromosome.fitness_dap, chromosome.fitness_ddap

# Sprawdzenie czy połączenie jest wymagane
def check_demand(link, dem, p):
    path = dem.list_of_demand_paths[p]
    if int(link) in path.links_in_path:
        return True
    else:
        return False


# Generacja pierwszej populacji
def gen_first_population(list_of_demands, pop_size_int):
    first_pop_list = list()  # List of Chromosome objects

    # Wygenerowanie liczby chromosomow jak rozmiar polulacji
    for i in range(0, pop_size_int):
        first_pop_list.append(gen_chromosome(list_of_demands))

    print("\nPopulacja początkowa:")
    return first_pop_list


# Decyduje przeprowadza mutacje, biorąc pod uwagę zadane prawdopodobienstwa
def do_mutation(chromosome, m_prob):
    # Sprawdz czy prawd w [0, 1]
    if 0 < m_prob <= 1:
        m_prob = m_prob
    else:
        # Jeżeli niepoprawne prawdopodobienstwo
        m_prob = 0.7

    for gene in chromosome.list_of_genes:

        if random.random() < m_prob:

            num_of_a = len(gene.list_of_a)

            # Losowo wybrane dwie generacje
            first_gen_val_swap = random.randint(0, num_of_a - 1)
            sec_gen_val_swap = random.randint(0, num_of_a - 1)


            while gene.list_of_a[first_gen_val_swap] <= 0:
                first_gen_val_swap = random.randint(0, num_of_a - 1)


            while sec_gen_val_swap == first_gen_val_swap:
                sec_gen_val_swap = random.randint(0, num_of_a - 1)

            gene.list_of_a[first_gen_val_swap] -= 1
            gene.list_of_a[sec_gen_val_swap] += 1
            return True
        else:
            return False

# Przeprowadza krzyzowanie, zwraca listę chromosomow i populacji po mutacji
def do_cross(list_of_chrom, cross_prob):
    # Sprawdz czy prawd w [0, 1]
    if 0 < cross_prob <= 1:
        cross_prob = cross_prob
    else:
        # Jeżeli niepoprawne prawdopodobienstwo
        cross_prob = 0.7

    # Przeprowadza krzyzowanie
    list_off = list()
    # Dodajemy chromosomy z listy
    list_off += list_of_chrom

    while len(list_of_chrom) >= 2:
        # Tpobiera rodziców z listy
        first_parent_genes = list_of_chrom.pop(0).list_of_genes
        second_parent_genes = list_of_chrom.pop(0).list_of_genes

        # Określa czy dochodzi do krzyżowanie dla każdej pary rodziców
        if random.random() < cross_prob:

            first_off_gen = list()
            second_off_gen = list()

            # Wykreowanie potomstwa
            for i in range(0, len(first_parent_genes)):
                # Decide which gene is taken from which parent
                if random.random() < 0.5:

                    first_off_gen.append(first_parent_genes[i])
                    second_off_gen.append(second_parent_genes[i])
                else:


                    first_off_gen.append(second_parent_genes[i])
                    second_off_gen.append(first_parent_genes[i])

            # Dodanie do listy potomstwa
            list_off.append(cl.Chromosome(first_off_gen, 0, 0))
            list_off.append(cl.Chromosome(second_off_gen, 0, 0))

    return list_off


# Funcja generuje chromosom
def gen_chromosome(list_of_dem):
    list_of_gen = list()
    for item in list_of_dem:
        dem_vol = item.demand_volume  # Pobierz potrzebna
        num_demands = item.number_of_demand_paths

        list_of_all = [0] * num_demands

        dem_to_assign = dem_vol

        while dem_to_assign > 0:
            # Wybiera w sposób losowy, który "allel" będzie inkrementowany
            al_to_increment = random.randint(0, num_demands - 1)
            # Inkrementacja "alleli"
            list_of_all[al_to_increment] += 1
            # dekrementacja
            dem_to_assign -= 1

        # Dodanie generacji do chromosomu
        list_of_gen.append(cl.Gene(list_of_all, dem_vol))

    # Stworzenie instancji chromosomu
    chromosome = cl.Chromosome(list_of_gen, 0, 0)
    return chromosome
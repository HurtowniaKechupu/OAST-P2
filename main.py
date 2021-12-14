import time

# Default variables
MAX_TIME = 200
MAX_GENERATIONS = 250
MAX_MUTATIONS = 500
MAX_NOT_IMPROVED = 10

INITIAL_POPULATION = 100
CROSSOVER_PROBABILITY = 0.65
MUTATION_PROBABILITY = 0.15
SEED = 8

duration = 0
iteration = 0
mutations = 0
not_improved_iteration = 0

# UI
while True:
    option = input("Wybierz plik: 1. net4.txt  2. net12_1.txt  3. net12_2.txt: ")
    print(option)
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
        print("Zły plik! Wybierz ponownie.")
exit(0)

dupa = input()
INITIAL_POPULATION = int(dupa)

#except:
#    INITIAL_POPULATION = INITIAL_POPULATION
print(INITIAL_POPULATION)
'''try:
    CROSSOVER_PROBABILITY = float(input("Określ prawdopodobieństwo krzyżowania (float): "))
except:
    CROSSOVER_PROBABILITY = CROSSOVER_PROBABILITY
try:
    MUTATION_PROBABILITY = float(input("Określ prawdopodobieństwo mutacji (float): "))
except:
    MUTATION_PROBABILITY = MUTATION_PROBABILITY
try:
    SEED = int(input("Określ ziarno dla generatora liczb pseudolosowych (int): "))
except:
    SEED = SEED
'''
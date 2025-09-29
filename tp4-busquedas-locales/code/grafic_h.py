import matplotlib.pyplot as plt
import time
import collections
import random
import math

f = collections.Counter()



def h(board):

    dicts = [0,0,0]
    dicts[0] = row_count = collections.Counter()
    dicts[1] = diag1_count = collections.Counter()
    dicts[2] = diag2_count = collections.Counter()
    threateneds = 0
    size = len(board)

    if size == 0:
        return 0

    for i in range(0,size):
        row = board[i]
        colum = i

        row_count[row] += 1
        diag1_count[row - colum] += 1
        diag2_count[row+colum] += 1

    for dic in dicts:

        for operator in dic.values():

            if operator > 1:
                comb = operator * (operator - 1) // 2
                threateneds += comb

    return threateneds

def hill_climbing(board, states, limit):

    size = len(board)
    best_board = board.copy()
    best_value = h(board)
    global f

    for colum in range(0,size):

        board_aux = board.copy()

        for row in range(0, size):

            if states == limit:
                return (best_board, best_value, states)

            if board[colum] == row:
                continue
            
            states += 1
            board_aux[colum] = row
            value = h(board_aux)
            f[states] = best_value

            if value < best_value:
                best_board = board_aux.copy()
                best_value = value

    return (best_board, best_value, states)

def execute_HC(board, limit):

    states = 0
    best_board = board
    last_board = board

    start = time.time()

    while states < limit:

        best_board, best_value, states = hill_climbing(last_board, states, limit)

        if best_board == last_board:
            break

        last_board = best_board.copy()

    return ("HC",best_board, best_value, states,time.time() - start)


def schedule(t):
    return 100 * (0.97 ** t)

def pick_neighbor(board):

    colum = random.randint(0,len(board)-1)
    new_row = board[colum]
    while new_row == board[colum]:
        new_row = random.randint(0,len(board)-1)

    new_board = board.copy()
    new_board[colum] = new_row

    return new_board

def execute_SA(board, limit, seed):

    states = 0
    current_board = board
    next_board = []

    random.seed(seed)

    start = time.time()
    t = 0
    while states < limit and h(current_board) != 0:
        t_high = schedule(states)
        if round(t_high,10) == 0:
            break
        
        neighbor = pick_neighbor(current_board)
        states += 1
        f[states] = h(current_board)

        delta_e = h(neighbor) - h(current_board)

        if delta_e < 0:
            current_board = neighbor
        else:
            try:
                prob = math.exp(-delta_e/t_high)
            except OverflowError:
                prob = float("inf")

            if random.random() < prob:
                current_board = neighbor

    return ("SA",current_board, h(current_board), states,time.time() - start)

def tournament_selection(population, fitness_map):
    tournament_size = 3
    candidates = random.sample(population, tournament_size)

    best_candidate = min(candidates, key=lambda candidate: fitness_map[tuple(candidate)])

    return best_candidate.copy()

def mutation(candidate):
    
    column1, column2 = random.sample(range(len(candidate)), 2)
    candidate[column1], candidate[column2] = candidate[column2], candidate[column1]
    return candidate

def PMX(p1, p2):
    size = len(p1)
    c1, c2 = random.sample(range(size), 2)
    if c1 > c2:
        c1, c2 = c2, c1

    changes1 = {}
    changes2 = {}

    for i in range(c1,c2+1):
        changes1[p1[i]] = p2[i]
        changes2[p2[i]] = p1[i]

    offspring1 = [-1] * size
    offspring2 = [-1] * size

    for i in range(size):
        if i >= c1 and i <= c2:
            offspring1[i] = p1[i]
            offspring2[i] = p2[i]
        else:
            if p1[i] not in changes1:
                offspring1[i] = p1[i]
            else:
                val = changes1[p1[i]]
                offspring1[i] = val
            
            if p2[i] not in changes2:
                offspring2[i] = p2[i]
            else:
                val = changes2[p2[i]]
                offspring2[i] = val

    return offspring1, offspring2

def execute_GA(board, limit, seed):

    population_size = 80
    cross_rate = 0.8 
    mutation_rate = 0.1
    states = 0
    size = len(board)

    random.seed(seed)

    population = []
    population_values = {}

    def evaluate(candidate):
        nonlocal states
        states += 1
        return h(candidate)

    for _ in range(population_size):
        individual = [random.randint(0,size-1) for _ in range(size)]
        fitness = evaluate(individual)
        population.append(individual)
        population_values[tuple(individual)] = fitness

    best_board = min(population, key=lambda ind: population_values[tuple(ind)])
    best_value = population_values[tuple(best_board)]
    best_board = best_board.copy()

    print(population)

    start = time.time()
    while states < limit and best_value > 0:

        new_population = []
        new_population_values = {}

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, population_values)
            parent2 = tournament_selection(population, population_values)

            if random.random() < cross_rate:
                offspring1, offspring2 = PMX(parent1, parent2)
            else:
                offspring1, offspring2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                offspring1 = mutation(offspring1)
            if random.random() < mutation_rate:
                offspring2 = mutation(offspring2)

            new_population.append(offspring1)
            new_population.append(offspring2)

            new_population_values[tuple(offspring1)] = evaluate(offspring1)
            new_population_values[tuple(offspring2)] = evaluate(offspring2)

            f[states] = best_value


        population = new_population[:population_size]
        population_values = {
            tuple(ind): new_population_values[tuple(ind)] for ind in population
        }

        current_best = min(population, key=lambda ind: population_values[tuple(ind)])
        current_best_value = population_values[tuple(current_best)]


        if current_best_value < best_value:
            best_board = current_best.copy()
            best_value = current_best_value
            f[states] = best_value
        

    end = time.time()
    total_time = end - start

    return ("GA", best_board, best_value, states, total_time)

def random_algorithm(board, limit, seed):
    random.seed(seed)
    size = len(board)
    best_candidate = board
    best_value = h(board)
    states = 0
    f[states] = best_value
    start = time.time()

    while states < limit and best_value > 0:
        candidate = [random.randint(0, size-1) for _ in range(size)]
        candidate_value = h(candidate)
        states += 1
        if candidate_value < best_value:
            best_value = candidate_value
            best_candidate = candidate.copy()
        f[states] = best_value

    end = time.time()
    return ("Random", best_candidate, best_value, states, end-start)

# Diccionario con los valores de la función

seed = 1298374610
limit = 1000
random.seed(seed)
board = [random.randint(0,10) for i in range(0,10)]

#execute_HC(board, limit)
#execute_SA(board, limit, seed)
#execute_GA(board, limit, seed)
#random_algorithm(board, limit, seed)

print(f)

# Separar claves (x) y valores (y)
x = list(f.keys())
y = list(f.values())

# Crear gráfico
plt.plot(x, y, marker="o", linestyle="-", color="b", label="h(x)", markersize=0)

# Personalizar gráfico
plt.title(f"Gráfico de la función H(x) en Hill Climbing de tamaño 10,\n con seed={seed} y límite={limit}")
plt.xlabel("Iteracion")
plt.ylabel("H(board)")
plt.grid(True)
plt.legend()

# Mostrar
plt.show()

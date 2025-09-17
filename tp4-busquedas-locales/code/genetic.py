import collections
import time
import random

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

def tournament_selection(population_values):
    tournament_size = 3
    candidates = random.sample(sorted(population_values.keys()), tournament_size)

    min = float("inf")

    for candidate in candidates:
        value = population_values[candidate]
        if value < min:
            min = value
            best_candidate = candidate
            
    return list(best_candidate)

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

    population_size = 200
    cross_rate = 0.8 
    mutation_rate = 0.1
    states = 0
    size = len(board)

    random.seed(seed)

    population = []
    population_values = {}

    for _ in range(population_size):
        individual = list(random.sample(range(size), size))
        population.append(individual)
        population_values[tuple(individual)] = h(individual)
        states += 1

    best_board = min(population, key=lambda ind: h(ind))
    best_value = h(best_board)

    start = time.time()
    while states < limit and best_value > 0:

        new_population = []

        while len(new_population) < population_size:
            parent1 = tournament_selection(population_values)
            parent2 = tournament_selection(population_values)

            if random.random() < cross_rate:
                offspring1, offspring2 = PMX(parent1, parent2)
                states += 2
            else:
                offspring1, offspring2 = parent1, parent2

            if random.random() < mutation_rate:
                offspring1 = mutation(offspring1)
                states += 1
            if random.random() < mutation_rate:
                offspring2 = mutation(offspring2)
                states += 1

            new_population.append(offspring1)
            new_population.append(offspring2)

            population_values[tuple(offspring1)] = h(offspring1)
            population_values[tuple(offspring2)] = h(offspring2)

        population = new_population[:population_size]

        current_best = min(population, key=lambda ind: h(ind))
        current_best_value = h(current_best)

        if current_best_value < best_value:
            best_board = current_best
            best_value = current_best_value

    end = time.time()
    total_time = end - start

    return ("GA", best_board, best_value, states, total_time)
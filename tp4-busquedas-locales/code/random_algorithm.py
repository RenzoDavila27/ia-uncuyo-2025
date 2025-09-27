import random
import collections
import time

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

def random_algorithm(board, limit, seed):
    random.seed(seed)
    size = len(board)
    best_candidate = board
    best_value = h(board)
    states = 0
    start = time.time()

    while states < limit and best_value > 0:
        candidate = [random.randint(0, size-1) for _ in range(size)]
        candidate_value = h(candidate)
        states += 1
        if candidate_value < best_value:
            best_value = candidate_value
            best_candidate = candidate.copy()

    end = time.time()
    return ("Random", best_candidate, best_value, states, end-start)
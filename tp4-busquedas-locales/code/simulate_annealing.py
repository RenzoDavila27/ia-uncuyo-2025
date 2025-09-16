import collections
import time
import random
import math

def schedule(t):
    return 100 * (0.97 ** t)


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
    while states < limit:
        t_high = schedule(states)
        if round(t_high,10) == 0:
            break
        
        neighbor = pick_neighbor(current_board)
        states += 1

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

    
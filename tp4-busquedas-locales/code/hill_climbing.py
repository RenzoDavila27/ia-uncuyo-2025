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

def hill_climbing(board, states, limit):

    size = len(board)
    best_board = board.copy()
    best_value = h(board)

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
import time

global states, size

def check_consistency(asig, var, value):
    for key in asig.keys():
        if asig[key] == value or abs(asig[key] - value) == abs(key - var):
            return False
    return True

def mrv(asig, board):
    global size
    min_var = None
    min_count = float('inf')

    for i in range(size):
        if i not in asig:
            count = len(board[i])
            if count < min_count:
                min_count = count
                min_var = i

    return min_var

def lcv(board, var):
    value_counts = {}
    for value in board[var]:
        count = 0
        for i in range(len(board)):
            if i != var and value in board[i]:
                count += 1
        value_counts[value] = count
    return sorted(value_counts, key=value_counts.get)

def forward_checking(asig, board):

    global states, size

    if len(asig) == size:
        return asig
    
    var = mrv(asig, board)

    for value in lcv(board, var):

        states += 1

        if check_consistency(asig, var, value):

            asig[var] = value
            temp_board = [list(values) for values in board]

            for i in range(size):
                if i != var and value in temp_board[i]:
                    temp_board[i].remove(value)
                diff = abs(i - var)
                if i != var and (value - diff) in temp_board[i]:
                    temp_board[i].remove(value - diff)
                if i != var and (value + diff) in temp_board[i]:
                    temp_board[i].remove(value + diff)

            if all(temp_board[i] for i in range(size) if i not in asig):
                result = forward_checking(asig, temp_board)
                if result is not None:
                    return result

            del asig[var]

def asig_to_board(asig):
    board = [0 for _ in range(len(asig))]
    for column, row in asig.items():
        board[column] = row
    return board

def run(board, seed, fixed_assignment=None):
    global states, size
    size = len(board)
    asig = fixed_assignment if fixed_assignment is not None else {}
    states = 0
    start = time.time()
    asig = forward_checking(asig, board)
    end = time.time()
    if asig is None:
        return "forward_checking", None, end-start, states
    board = asig_to_board(asig)
    name = "forward_checking"
    return name, board, end-start, states
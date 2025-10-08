import time

global states
global size

def choose_variable(asig):

    global size

    for i in range(size):
        if i not in asig.keys():
            return i
        
def check_consistency(asig, var, value):
    for key in asig.keys():
        if asig[key] == value or abs(asig[key] - value) == abs(key - var):
            return False
    return True

def recursive(asig, board):

    global states
    global size

    if len(asig.keys()) == size:
        return asig

    var = choose_variable(asig)

    for value in board[var]:

        states += 1

        if check_consistency(asig, var, value):

            asig[var] = value

            result = recursive(asig, board)

            if result is not None:
                return result

            del asig[var]
        
    return None

def asig_to_board(asig):
    board = [0 for _ in range(len(asig))]
    for column, row in asig.items():
        board[column] = row
    return board

def run(board, seed, fixed_assignment=None):
    global states, size
    asig = fixed_assignment if fixed_assignment is not None else {}
    states = 0
    size = len(board)
    start = time.time()
    asig = recursive(asig, board)
    end = time.time()
    if asig is None:
        return ("backtracking", None, end - start, states)

    board = asig_to_board(asig)
    return ("backtracking", board, end - start, states)
        

    
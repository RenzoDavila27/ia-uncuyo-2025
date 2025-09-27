import hill_climbing
import random
import argparse
import simulate_annealing
import genetic
import random_algorithm

def random_board(n):
    return [random.randint(0, n-1) for _ in range(n)]


if __name__ == "__main__":

    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="Semilla para reproducibilidad")
    parser.add_argument("--size", type=int, required=True, help="Tamaño del tablero")
    args = parser.parse_args()

    seed = args.seed
    size = args.size


    limit = 1000
    random.seed(seed)
    board = random_board(size)
    #result = hill_climbing.execute_HC(board,limit)
    #result = simulate_annealing.execute_SA(board,limit,seed)
    #result = genetic.execute_GA(board,limit,seed)
    result = random_algorithm.random_algorithm(board,limit,seed)
    name, best_board, best_value, states, time = result
    print(f"{name}, {seed}, {size}, {best_board}, {best_value}, {states}, {time}")

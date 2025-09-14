import hill_climbing
import random
import argparse


def random_board(n):
    return [random.randint(0, n-1) for _ in range(n)]


if __name__ == "__main__":

    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="Semilla para reproducibilidad")
    args = parser.parse_args()

    seed = args.seed

    random.seed(seed)
    board = random_board(15)
    print(board)
    print(hill_climbing.execute_HB(board, 10000))

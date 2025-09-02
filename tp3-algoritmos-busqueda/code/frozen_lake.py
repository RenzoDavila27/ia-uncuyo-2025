import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from gymnasium.error import DependencyNotInstalled
from gymnasium.utils import seeding
from gymnasium import wrappers
import random_search
import argparse
import bfs
import dfs
import uniform_cost
import dfs_limit
import a_star1
import a_star2



def generate_random_map_custom(
    size: int = 8, p: float = 0.8, seed: int | None = None
) -> list[str]:
    
    board = []  # initialize to make pyright happy

    np_random, _ = seeding.np_random(seed)

    p = min(1, p)
    board = np_random.choice(["F", "H"], (size, size), p=[p, 1 - p])
    
    posiciones_F = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 'F']

    s_pos, f_pos = np_random.choice(posiciones_F, size=2, replace=False)

    board[s_pos[0]][s_pos[1]] = 'S'
    board[f_pos[0]][f_pos[1]] = 'G'

    return ["".join(x) for x in board]

if __name__ == "__main__":
    # Parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="Semilla para reproducibilidad")
    args = parser.parse_args()

    seedd = args.seed

    env = gym.make(
        "FrozenLake-v1",
        desc=generate_random_map_custom(size=100, p=0.92, seed=seedd),
        render_mode="human",
        is_slippery=False,
        max_episode_steps=1000
    )

    # Ejecutar algoritmo de busqueda
    # random_search.random_search(env, seedd)
    # bfs.executeBFS(env,seedd)
    # dfs.executeDFS(env, seedd)
    # dfs_limit.executeDFS_limit(env,seedd,100)
    # uniform_cost.executeUniformCost(env,seedd)
    # a_star1.executeA_star(env, seedd)
    a_star2.executeA_star(env, seedd)






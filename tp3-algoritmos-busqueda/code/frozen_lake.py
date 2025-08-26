import gymnasium as gym
import random
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from gymnasium.error import DependencyNotInstalled
from gymnasium.utils import seeding


#env = gym.make('FrozenLake-v1', render_mode='human', is_slippery=False)
env = gym.make('FrozenLake-v1', desc=generate_random_map(size=3, p=0.01), render_mode='human')
print("Numero de estados:", env.observation_space.n)
print("Numero de acciones:", env.action_space.n)

state = env.reset()
print("Posicion inicial del agente:", state[0])
done = truncated = False
i=0
while not (done or truncated):
    action = env.action_space.sample()
    i+=1
    # Accion aleatoria
    next_state, reward, done, truncated, _ = env.step(action)
    print(f"Accion: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
    if not reward == 1.0:
        print(f"¿Gano? (encontro el objetivo): False")
        print(f"¿Perdio? (se cayo): {done}")
        print(f"¿Freno? (alcanzo el maximo de pasos posible): {truncated}\n")
    else:
        print(f"¿Gano? (encontro el objetivo): {done}")
    state = next_state

def generate_random_map(
    size: int = 8, p: float = 0.8, seed: int | None = None
) -> list[str]:
    """Generates a random valid map (one that has a path from start to goal)

    Args:
        size: size of each side of the grid
        p: probability that a tile is frozen
        seed: optional seed to ensure the generation of reproducible maps

    Returns:
        A random valid map
    """
    valid = False
    board = []  # initialize to make pyright happy

    np_random, _ = seeding.np_random(seed)

    pos_initial = (random.randint(0,size),random.randint(0,size))
    pos_final = (random.randint(0,size),random.randint(0,size))

    while not valid:
        p = min(1, p)
        board = np_random.choice(["F", "H"], (size, size), p=[p, 1 - p])
    
    

    return ["".join(x) for x in board]
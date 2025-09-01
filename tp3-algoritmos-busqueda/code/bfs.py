import time
from collections import deque

start = None
visited = set()

def BFS(env):

    global visited, start
    desc = env.unwrapped.desc
    rows, cols = desc.shape

    # Encontrar la posición de inicio
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if desc[r, c] == b'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
    

    queue = deque([(start_pos, [])])

    actions = {
        0: (0, -1),  # Izquierda
        1: (1, 0),   # Abajo
        2: (0, 1),   # Derecha
        3: (-1, 0)   # Arriba
    }

    start = time.time()

    while queue:
        (row, col), path = queue.popleft()

        if desc[row, col] == b'G':
            # ¡Encontraste el objetivo!
            return path

        if (row, col) in visited:
            continue

        visited.add((row, col))

        for action, (dr, dc) in actions.items():
            new_row, new_col = row + dr, col + dc

            # Verifica los límites de la cuadrícula
            if 0 <= new_row < rows and 0 <= new_col < cols:

                if desc[new_row, new_col] != b'H':
                    new_path = path + [action]
                    queue.append(((new_row, new_col), new_path))

    return None # No se encontró un camino
                
def executeBFS(env,seed):
        
        global start
        global visited

        path = BFS(env)
        end = time.time()
        cost = 0
        env.reset()
        if path == None:

            print(f"BFS,{seed},{len(visited)},{0},{0},{end-start},False")
            return

        for action in path:
            _, _, done, _, _ = env.step(action)
            if action in [1,3]:
                cost+=10
            else:
                cost+=1

            if done:
                break

        end = time.time()
        print(f"BFS,{seed},{len(visited)},{len(path)},{cost},{end-start},True")
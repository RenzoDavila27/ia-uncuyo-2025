import time
import heapq

start = None
visited = set()

def uniformCost(env):

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
    

    prior_queue = []
    heapq.heappush(prior_queue, (0,(start_pos,[])))

    actions = {
        0: (0, -1),  # Izquierda
        1: (1, 0),   # Abajo
        2: (0, 1),   # Derecha
        3: (-1, 0)   # Arriba
    }

    start = time.time()
    i=0
    while prior_queue:
        cost, ((row, col), path) = heapq.heappop(prior_queue)

        if desc[row, col] == b'G':
            # ¡Encontraste el objetivo!
            return (path, cost)

        if (row, col) in visited:
            continue

        visited.add((row, col))

        for action, (dr, dc) in actions.items():
            new_row, new_col = row + dr, col + dc

            if action in [1,3]:
                cost_action = 10
            else:
                cost_action = 1

            # Verifica los límites de la cuadrícula
            if 0 <= new_row < rows and 0 <= new_col < cols:

                if desc[new_row, new_col] != b'H':
                    new_path = path + [action]
                    heapq.heappush(prior_queue ,(cost + cost_action,((new_row, new_col), new_path)))

    return (None,None)# No se encontró un camino
                
def executeUniformCost(env,seed):
        
        global start
        global visited

        count_actions = 0
        path, cost = uniformCost(env)
        end = time.time()
        env.reset()
        if path == None:

            print(f"UniformCost,{seed},{len(visited)},{0},{0},{end-start},False")
            return

        for action in path:
            count_actions+=1
            _, _, done, limit, _ = env.step(action)

            if done:
                finish = True
                break

            if limit:
                finish = False
                break
        
        end = time.time()
        print(f"UniformCost,{seed},{len(visited)},{count_actions},{cost},{end-start},{finish}")


        
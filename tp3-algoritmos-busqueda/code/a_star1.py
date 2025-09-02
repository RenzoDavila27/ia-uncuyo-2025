import time
import heapq
import math

start = None
visited = set()

def h(start, end):
    A = abs(start[0]-end[0])
    B = abs(start[1]-end[1])

    return math.sqrt(A**2+B**2)


def a_start(env):

    global visited, start
    desc = env.unwrapped.desc
    rows, cols = desc.shape
    s = e = False
    
    # Encontrar la posición de inicio
    start_pos = None
    end_pos = None
    for r in range(rows):
        for c in range(cols):
            if desc[r, c] == b'S':
                start_pos = (r, c)
                s = True
            if desc[r, c] == b'G':
                end_pos = (r,c)
                e = True
            if s and e:
                break
        if s and e:
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
                    heapq.heappush(prior_queue ,(cost+1+h((new_row,new_col), end_pos),((new_row, new_col), new_path)))

    return None# No se encontró un camino
                
def executeA_star(env,seed):
        
        global start
        global visited

        path  = a_start(env)
        end = time.time()
        count_actions = 0
        cost = 0
        env.reset()
        if path == None:

            print(f"A*_esc1,{seed},{len(visited)},{0},{0},{end-start},False")
            return

        for action in path:
            count_actions+=1
            _, _, done, limit, _ = env.step(action)
            if action in [1,3]:
                cost+=10
            else:
                cost+=1

            if done:
                finish = True
                break

            if limit:
                finish = False
                break
        
        end = time.time()
        print(f"A*_esc1,{seed},{len(visited)},{count_actions},{cost},{end-start},{finish}")


        
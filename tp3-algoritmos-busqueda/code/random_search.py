import time
import numpy as np

def random_search(env, seed):

    rng = np.random.default_rng(seed)
    inicio = time.time()
    actions = 0 
    cost = 0


    state = env.reset()
    states_explored = [state]
    end = limit_actions = False

    while not (end or limit_actions):

        action = rng.choice([0,1,2,3])
        new_state, goal, end, limit_actions, _= env.step(action)
        if not (new_state in states_explored):
            states_explored.append(new_state)
        actions += 1 
        if action in [1,3]:
            cost+=10
        else:
            cost+=1
    
    final = time.time()

    if goal == 1:
        end = True
    else:
        end = False  
    print(f"Random,{seed},{len(states_explored)},{actions},{cost},{final-inicio},{end}")

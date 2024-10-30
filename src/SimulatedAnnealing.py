import numpy as np
import math
import random
from ObjFunct import objFunc
from Tools import RandomCube

def schedule(t, initial_temperature, cooling_rate):
    return max(initial_temperature * math.pow(cooling_rate, t), 0)

def SimulatedAnnealing(init_cube, initial_temperature=1000, cooling_rate = 0.9, schedule=schedule):
    current_cube = init_cube
    current_value = objFunc(current_cube)
    t = 1
    
    cubes = [current_cube]
    values = [current_value]
    count_iter = 0
    e_probs = []
    count_stuck = 0
    
    while True:
        count_iter += 1
        T = schedule(t, initial_temperature, cooling_rate)
        if T == 0:
            break
        
        random_neighbor = np.copy(current_cube)

        a, b, c = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        while (a, b, c) == (i, j, k):
            i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        random_neighbor[a, b, c], random_neighbor[i, j, k] = random_neighbor[i, j, k], random_neighbor[a, b, c]
        random_value = objFunc(random_neighbor)
        deltaE = random_value - current_value
        p = math.exp(deltaE / T)
        e_probs.append(p)

        if deltaE > 0:
            current_cube = random_neighbor
            current_value = random_value
        else:
            if random.random() < p:
                count_stuck += 1
                current_cube = random_neighbor
                current_value = random_value
        
        print("curr val", current_value)
        print("T", T)
        

        t += 1

    return cubes, values, count_iter, e_probs, count_stuck

# res_cube, val = SimulatedAnnealing(1000, 0.999, schedule)

# print(val)
# for level in res_cube:
#     print(level)
import numpy as np
import math
import random
from ObjFunct import objFunc
from Tools import RandomCube

def SimulatedAnnealing(schedule, initial_temperature, cooling_rate):
    current_cube = RandomCube()
    current_value = objFunc(current_cube)
    t = 1
    
    while True:
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

        if deltaE > 0:
            current_cube = random_neighbor
            current_value = random_value
        else:
            if random.random() < math.exp(deltaE / T):
                current_cube = random_neighbor
                current_value = random_value
        
        print("curr val", current_value)
        print("T", T)
        

        t += 1

    return current_cube, current_value

def schedule(t, initial_temperature, cooling_rate):
    return max(initial_temperature * math.pow(cooling_rate, t), 0)

res_cube, val = SimulatedAnnealing(schedule, 200, 0.999)

print(val)
for level in res_cube:
    print(level)
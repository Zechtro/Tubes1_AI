import random
import numpy as np
from ObjFunct import objFunc
from Tools import RandomCube

def StochasticHillClimbing(max_iter):
    current_cube = RandomCube()
    current_value = objFunc(current_cube)
    iter = 1
    
    while iter <= max_iter:
        random_neighbor = np.copy(current_cube)

        a, b, c = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        while (a, b, c) == (i, j, k):
            i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        random_neighbor[a, b, c], random_neighbor[i, j, k] = random_neighbor[i, j, k], random_neighbor[a, b, c]
        random_value = objFunc(random_neighbor)

        if random_value > current_value:
            current_cube = random_neighbor
            current_value = random_value
        print("Val:", current_value)
        
        iter += 1
    
    return current_cube, current_value

cubet, val = StochasticHillClimbing(10000)
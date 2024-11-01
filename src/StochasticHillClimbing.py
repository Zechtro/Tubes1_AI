import random
import numpy as np
from ObjFunct import objFunc
from Tools import RandomCube

def StochasticHillClimbing(init_cube, max_iter):
    current_cube = init_cube
    current_value = objFunc(current_cube)
    iter = 0
    
    values = [current_value]
    cubes = [current_cube]
    
    while iter <= max_iter:
        iter += 1
        random_neighbor = np.copy(current_cube)

        z1, x1, y1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        z2, x2, y2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        while (z1, x1, y1) == (z2, x2, y2):
            z2, x2, y2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        random_neighbor[z1, x1, y1], random_neighbor[z2, x2, y2] = random_neighbor[z2, x2, y2], random_neighbor[z1, x1, y1]
        random_value = objFunc(random_neighbor)

        if random_value > current_value:
            current_cube = random_neighbor
            current_value = random_value
        print("Val:", current_value)
        
        values = np.append(values, current_value)
        cubes = np.append(cubes, current_cube)
        
    return cubes.tolist(), values.tolist(), iter
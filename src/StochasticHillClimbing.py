import random
import numpy as np
from Cube import Cube
  
def StochasticHillClimbingCube(init_cube, max_iter):
    current_cube = Cube(5, 5, 5, False, init_cube)
    current_value = current_cube.state_value
    iter = 0
    
    values = [current_value]
    cubes = [current_cube]
    
    while iter <= max_iter:
        iter += 1
        random_neighbor = current_cube.copy()

        z1, x1, y1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        z2, x2, y2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        while (z1, x1, y1) == (z2, x2, y2):
            z2, x2, y2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        temp = random_neighbor.get_value(z1, x1, y1)
        random_neighbor.insert_value(z1, x1, y1, random_neighbor.get_value(z2, x2, y2))
        random_neighbor.insert_value(z2, x2, y2, temp)
        random_neighbor.calculate_state_value()

        random_value = random_neighbor.state_value

        if random_value > current_value:
            current_cube = random_neighbor
            current_value = random_value
        print("Val:", current_value)
        
        values.append(current_value)
        cubes.append(current_cube)
        
    return cubes, values, iter
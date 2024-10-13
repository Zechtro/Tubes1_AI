import numpy as np
from ObjFunct import objFunc
from Tools import GenerateNeighbor, RandomCube

def SteepestAscentHillClimbing():
    cube = RandomCube()
    current_cube = cube
    current_value = objFunc(cube)

    while True:  
        neighbors, neighbors_value = GenerateNeighbor(current_cube, 5)
        best_neighbor = neighbors[np.argmax(neighbors_value)]
        best_value = max(neighbors_value)
        print(best_value)
        
        if best_value > current_value:
            current_cube = best_neighbor
            current_value = best_value
        else:
            return current_cube, current_value

    return current_cube, current_value

SteepestAscentHillClimbing()
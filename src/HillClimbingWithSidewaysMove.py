import numpy as np
from ObjFunct import objFunc
from Tools import GenerateNeighbor, RandomCube

def HillClimbingWithSidewaysMove():
    cube = RandomCube()
    current_cube = cube
    current_value = objFunc(cube)
    best_value = -110

    while best_value <= current_value:  
        neighbors, neighbors_value = GenerateNeighbor(current_cube, 5)
        best_neighbor = neighbors[np.argmax(neighbors_value)]
        best_value = max(neighbors_value)
        
        if best_value <= current_value:
            current_cube = best_neighbor
            current_value = best_value

    return current_cube, current_value

HillClimbingWithSidewaysMove()
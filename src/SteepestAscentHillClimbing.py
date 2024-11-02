import numpy as np
from ObjFunct import objFunc
from Tools import GenerateNeighbor, RandomCube
from Cube import Cube, generate_successor

def SteepestAscentHillClimbing(init_cube):
    cube = init_cube
    current_cube = cube
    current_value = objFunc(cube)
    cubes = [current_cube]
    values = [current_value]
    count_iter = 0

    while True:
        count_iter += 1
        neighbors, neighbors_value = GenerateNeighbor(current_cube, 5)
        best_neighbor = neighbors[np.argmax(neighbors_value)]
        best_value = max(neighbors_value)
        
        if best_value > current_value:
            current_cube = best_neighbor
            current_value = best_value
        else:
            return cubes, values, count_iter
        
        cubes.append(current_cube)
        values.append(current_value)

    return cubes, values, count_iter
  
def SteepestAscentHillClimbingCube(init_cube):
    current_cube = Cube(5, 5, 5, False, init_cube)
    current_value = current_cube.state_value
    cubes = [current_cube]
    values = [current_value]
    count_iter = 0

    while True:
        count_iter += 1
        neighbors = generate_successor(current_cube.array)
        neighbors_value = [cube.state_value for cube in neighbors]
        best_neighbor = neighbors[np.argmax(neighbors_value)]
        best_value = max(neighbors_value)
        
        if best_value > current_value:
            current_cube = best_neighbor
            current_value = best_value
        else:
            return cubes, values, count_iter
        
        cubes.append(current_cube)
        values.append(current_value)

    return cubes, values, count_it
  
  
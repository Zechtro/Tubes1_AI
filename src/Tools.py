import numpy as np
from copy import deepcopy
from ObjFunct import objFunc

def GenerateNeighbor(cube, size):
    neighbors = []
    neighbors_value = []

    for x1 in range(size):
        for y1 in range(size):
            for z1 in range(size):
                for x2 in range(size):
                    for y2 in range(size):
                        for z2 in range(size):
                            if (x1, y1, z1) != (x2, y2, z2):
                                new_cube = deepcopy(cube)
                                new_cube[x1][y1][z1], new_cube[x2][y2][z2] = new_cube[x2][y2][z2], new_cube[x1][y1][z1]
                                new_cube_value = objFunc(new_cube)
                                if new_cube not in neighbors:
                                    neighbors.append(new_cube)
                                    neighbors_value.append(new_cube_value)
    return neighbors, neighbors_value

import random

def RandomCube():
    numbers = list(range(1, 126))
    random.shuffle(numbers)
    
    cube = [[[0,0,0,0,0] for _ in range (5)] for _ in range (5)]
        
    idx = 0  
    for x in range(5):
        for y in range(5):
            for z in range(5):
                cube[x][y][z] = numbers[idx]
                idx += 1
    
    return cube



# TEST
# cube = [[[0,0,0,0,0] for j in range (5)] for i in range (5)]
# val = 1
# for x in range(5):
#     for y in range(5):
#         for z in range(5):
#             cube[x][y][z] = val
#             val += 1

# cube = [[[1,2],[3,4]],[[5,6],[7,8]]]
# new, val = GenerateNeighbor(cube, 2)
# for i in new:
#     print(i)
#     print()
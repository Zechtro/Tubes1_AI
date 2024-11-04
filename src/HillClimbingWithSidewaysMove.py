import numpy as np
from Cube import Cube, generate_successor

def HillClimbingWithSidewaysMoveCube(init_cube, max_sideways):
    current_cube = Cube(5, 5, 5, False, init_cube)
    current_value = current_cube.state_value
    neighbor_value = current_value
    
    count_iter = 0
    sideways_count = 0
    
    cubes = [current_cube]
    values = [current_value]

    while neighbor_value >= current_value and sideways_count < max_sideways:
        count_iter += 1
        neighbors = generate_successor(current_cube.array)
        neighbors_value = [cube.state_value for cube in neighbors]
        best_neighbor = neighbors[np.argmax(neighbors_value)]
        neighbor_value = max(neighbors_value)
        
        if neighbor_value >= current_value:
            if neighbor_value > current_value:
                sideways_count = 0
            elif neighbor_value == current_value:
                sideways_count += 1
            current_cube = best_neighbor
            current_value = neighbor_value
        print("Current val:", current_value, "| Neighbor Val:", neighbor_value, "| Sideways Count:", sideways_count)

    return cubes, values, count_iter
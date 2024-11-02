from ObjFunct import objFunc
from SteepestAscentHillClimbing import SteepestAscentHillClimbing, SteepestAscentHillClimbingCube
from Tools import RandomCube
from Cube import random_1d_array, Cube

def RandomRestartHillClimbing(init_cube, max_restart):
    current_cube = init_cube
    current_value = objFunc(current_cube)
    restart = 0
    cubes, values, count_iter = SteepestAscentHillClimbing(init_cube)
    
    cubes_per_restart = [cubes]
    values_per_restart = [values]
    iteration_per_restart = [count_iter]
    
    print(f"best value restart ke-{restart} = {values[-1]}")
    if values[-1] < current_value:
        current_value = values[-1]
        current_cube = cubes[-1]
    
    while restart <= max_restart:
        restart += 1
        cubes, values, count_iter = SteepestAscentHillClimbing(RandomCube())
        
        cubes_per_restart.append(cubes)
        values_per_restart.append(values)
        iteration_per_restart.append(count_iter)
        
        print(f"best value restart ke-{restart} = {values[-1]}")
        if values[-1] < current_value:
            current_value = values[-1]
            current_cube = cubes[-1]

    return cubes_per_restart, values_per_restart, iteration_per_restart, restart

def RandomRestartHillClimbingCube(init_cube, max_restart):

    
    restart = 0
    cubes, values, count_iter = SteepestAscentHillClimbingCube(init_cube)
    
    current_cube = cubes[0]
    current_value = current_cube.state_value   
    
    cubes_per_restart = [cubes]
    values_per_restart = [values]
    iteration_per_restart = [count_iter]
    
    print(f"Best value at restart {restart} = {values[-1]}")
    if values[-1] < current_value:
        current_value = values[-1]
        current_cube = cubes[-1]
    
    while restart < max_restart:
        restart += 1
        new_cube = random_1d_array(5) # Generate a new random Cube instance
        cubes, values, count_iter = SteepestAscentHillClimbingCube(new_cube)
        
        cubes_per_restart.append(cubes)
        values_per_restart.append(values)
        iteration_per_restart.append(count_iter)
        
        print(f"Best value at restart {restart} = {values[-1]}")
        if values[-1] < current_value:
            current_value = values[-1]
            current_cube = cubes[-1]

    return cubes_per_restart, values_per_restart, iteration_per_restart, restart
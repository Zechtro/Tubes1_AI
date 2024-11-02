from ObjFunct import objFunc
from SteepestAscentHillClimbing import SteepestAscentHillClimbing
from Tools import RandomCube

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
    current_cube = init_cube
    current_value = current_cube.state_value
    restart = 0
    cubes, values, count_iter = SteepestAscentHillClimbing(current_cube)
    
    cubes_per_restart = [cubes]
    values_per_restart = [values]
    iteration_per_restart = [count_iter]
    
    print(f"Best value at restart {restart} = {values[-1]}")
    if values[-1] < current_value:
        current_value = values[-1]
        current_cube = cubes[-1]
    
    while restart < max_restart:
        restart += 1
        new_cube = RandomCube()  # Generate a new random Cube instance
        cubes, values, count_iter = SteepestAscentHillClimbing(new_cube)
        
        cubes_per_restart.append(cubes)
        values_per_restart.append(values)
        iteration_per_restart.append(count_iter)
        
        print(f"Best value at restart {restart} = {values[-1]}")
        if values[-1] < current_value:
            current_value = values[-1]
            current_cube = cubes[-1]

    return cubes_per_restart, values_per_restart, iteration_per_restart, restart
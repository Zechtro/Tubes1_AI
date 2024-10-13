from ObjFunct import objFunc
from SteepestAscentHillClimbing import SteepestAscentHillClimbing
from Tools import RandomCube

def RandomRestartHillClimbing(max_iter):
    current_cube = RandomCube()
    current_value = objFunc(current_cube)
    iter = 1
    
    while iter <= max_iter:
        new_cube, new_value = SteepestAscentHillClimbing()
        print(f"best value iter ke-{iter} = {new_value}")
        if new_value < current_value:
            current_value = new_value
            current_cube = new_cube
        iter += 1

    return current_cube, current_value

best_cube, best_value =RandomRestartHillClimbing(50)
print(best_value)
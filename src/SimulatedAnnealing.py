import numpy as np
import math
import random
from ObjFunct import objFunc
from Tools import RandomCube
from Cube import Cube

def schedule(t, initial_temperature, cooling_rate):
    return max(initial_temperature * math.pow(cooling_rate, t), 0)

def SimulatedAnnealing(init_cube, initial_temperature=1000, cooling_rate = 0.9, schedule=schedule):
    current_cube = np.copy(init_cube) 
    current_value = objFunc(current_cube)
    t = 1
    
    cubes = [current_cube]
    values = [current_value]
    count_iter = 0
    e_probs = {}
    count_stuck = 0
    
    while True:
        T = schedule(t, initial_temperature, cooling_rate)
        if T == 0:
            break
        count_iter += 1
        
        random_neighbor = np.copy(current_cube)

        a, b, c = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        while (a, b, c) == (i, j, k):
            i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        random_neighbor[a, b, c], random_neighbor[i, j, k] = random_neighbor[i, j, k], random_neighbor[a, b, c]
        random_value = objFunc(random_neighbor)
        deltaE = random_value - current_value
        
        if deltaE > 0:
            current_cube = random_neighbor
            current_value = random_value
        else:
            if deltaE < 0:
                e_probs[count_iter] = math.exp(deltaE / T)
            if random.random() < math.exp(deltaE / T):
                count_stuck += 1
                current_cube = random_neighbor
                current_value = random_value
        
        cubes.append(current_cube)
        values.append(current_value)
        t += 1

    return cubes, values, count_iter, e_probs, count_stuck
  
def SimulatedAnnealingCube(init_cube, initial_temperature=1000, cooling_rate=0.9, schedule=schedule):
    current_cube = Cube(5, 5, 5, False, init_cube)
    current_value = current_cube.state_value
    t = 1
    
    cubes = [current_cube]
    values = [current_value]
    count_iter = 0
    e_probs = {}
    count_stuck = 0
    
    while True:
        T = schedule(t, initial_temperature, cooling_rate)
        if T == 0:
            break
        count_iter += 1

        random_neighbor = current_cube.copy()

        a, b, c = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        while (a, b, c) == (i, j, k):
            i, j, k = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

        temp = random_neighbor.get_value(a, b, c)
        random_neighbor.insert_value(a, b, c, random_neighbor.get_value(i, j, k))
        random_neighbor.insert_value(i, j, k, temp)
        random_neighbor.calculate_state_value()

        random_value = random_neighbor.state_value
        deltaE = random_value - current_value
        
        if deltaE > 0:
            current_cube = random_neighbor
            current_value = random_value
        else:
            if deltaE < 0:
                e_probs[count_iter] = math.exp(deltaE / T)
            if random.random() < math.exp(deltaE / T):
                count_stuck += 1
                current_cube = random_neighbor
                current_value = random_value
        
        cubes.append(current_cube)
        values.append(current_value)
        t += 1

    return cubes, values, count_iter, e_probs, count_stuck
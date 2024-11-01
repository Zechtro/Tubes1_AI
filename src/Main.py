import time
init_cube1 = [[[i+(5*j)+(25*k) for i in range(1,6)] for j in range(0,5)] for k in range(0,5)]
init_cube2 = [[[((i+(5*j)+(25*k)+42)%125 + 1) for i in range(1,6)] for j in range(0,5)] for k in range(0,5)]
init_cube3 = [[[((i+(5*j)+(25*k)+84)%125 + 1) for i in range(1,6)] for j in range(0,5)] for k in range(0,5)]
init_cubes = [init_cube1, init_cube2, init_cube3]
banyak_percobaan = 3

# Steepest Ascend Hill-climbing
from SteepestAscentHillClimbing import SteepestAscentHillClimbing
sum_time = 0
cubes_tiap_percobaan = []
values_tiap_percobaan = []
iteration_tiap_percobaan = []
for cube in init_cubes:
    start_time = time.perf_counter()
    cubes, values, count_iter = SteepestAscentHillClimbing(cube)
    end_time = time.perf_counter()
    sum_time += (end_time-start_time)
    
    cubes_tiap_percobaan.append(cubes)
    values_tiap_percobaan.append(values)
    iteration_tiap_percobaan.append(count_iter)
avg_time = sum_time/3

# Hill-climbing with Sideways Move
from HillClimbingWithSidewaysMove import HillClimbingWithSidewaysMove
param_max_sideways = 100
sum_time = 0
cubes_tiap_percobaan = []
values_tiap_percobaan = []
iteration_tiap_percobaan = []
for cube in init_cubes:
    start_time = time.perf_counter()
    cubes, values, count_iter = HillClimbingWithSidewaysMove(cube, param_max_sideways)
    end_time = time.perf_counter()
    sum_time += (end_time-start_time)
    
    cubes_tiap_percobaan.append(cubes)
    values_tiap_percobaan.append(values)
    iteration_tiap_percobaan.append(count_iter)
avg_time = sum_time/3

# Random Restart Hill-climbing
from RandomRestartHillClimbing import RandomRestartHillClimbing
param_max_restart = 3
sum_time = 0
cubesPerRestart_tiap_percobaan = []
valuesPerRestart_tiap_percobaan = []
iterationPerRestart_tiap_percobaan = []
restart_tiap_percobaan = []
for cube in init_cubes:
    start_time = time.perf_counter()
    cubes, values, iterations, restarts = RandomRestartHillClimbing(cube, param_max_restart)
    end_time = time.perf_counter()
    sum_time += (end_time-start_time)
    
    cubesPerRestart_tiap_percobaan.append(cubes)
    valuesPerRestart_tiap_percobaan.append(values)
    iterationPerRestart_tiap_percobaan.append(iterations)
    restart_tiap_percobaan.append(restarts)
avg_time = sum_time/3

# Stochastic Hill-climbing
from StochasticHillClimbing import StochasticHillClimbing
param_iteration = 100
sum_time = 0
cubes_tiap_percobaan = []
values_tiap_percobaan = []
iteration_tiap_percobaan = []
for cube in init_cubes:
    start_time = time.perf_counter()
    cubes, values, count_iter = StochasticHillClimbing(cube, param_iteration)
    end_time = time.perf_counter()
    sum_time += (end_time-start_time)
    
    cubes_tiap_percobaan.append(cubes)
    values_tiap_percobaan.append(values)
    iteration_tiap_percobaan.append(count_iter)
avg_time = sum_time/3

# Simulated Annealing
from SimulatedAnnealing import SimulatedAnnealing
param_initial_T = 900
param_cooling_rate = 0.99
sum_time = 0
cubes_tiap_percobaan = []
values_tiap_percobaan = []
iteration_tiap_percobaan = []
e_probs_tiap_percobaan = [] # nilai e^(deltaE/T) per iterasi tiap percobaan
count_stuck_tiap_percobaan = []
for cube in init_cubes:
    start_time = time.perf_counter()
    cubes, values, count_iter, e_probs, count_stuck = SimulatedAnnealing(cube, param_initial_T, param_cooling_rate)
    end_time = time.perf_counter()
    sum_time += (end_time-start_time)
    
    cubes_tiap_percobaan.append(cubes)
    values_tiap_percobaan.append(values)
    iteration_tiap_percobaan.append(count_iter)
    e_probs_tiap_percobaan.append(e_probs)
    count_stuck_tiap_percobaan(count_stuck)
avg_time = sum_time/3

# Genetic Algorithm

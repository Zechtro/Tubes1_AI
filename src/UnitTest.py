from Cube import Cube
import numpy as np
from HillClimbingWithSidewaysMove import HillClimbingWithSidewaysMoveCube
from SteepestAscentHillClimbing import SteepestAscentHillClimbingCube
from RandomRestartHillClimbing import RandomRestartHillClimbingCube
from SimulatedAnnealing import SimulatedAnnealingCube
from GeneticAlgorithm import genetic
from StochasticHillClimbing import StochasticHillClimbingCube
import time

def to_3d_array(cube_1d, x_size=5, y_size=5, z_size=5):
    cube_3d = []
    for x in range(x_size):
        layer = []
        for y in range(y_size):
            row = cube_1d[(x * y_size * z_size) + (y * z_size): (x * y_size * z_size) + (y * z_size) + z_size]
            layer.append(row)
        cube_3d.append(layer)
    
    return cube_3d

if __name__ == "__main__":  
  # Controlled test
  init_cube1 = [[[i+(5*j)+(25*k) for i in range(1,6)] for j in range(0,5)] for k in range(0,5)]
  init_cube2 = [[[((i+(5*j)+(25*k)+42)%125 + 1) for i in range(1,6)] for j in range(0,5)] for k in range(0,5)]
  init_cube3 = [[[((i+(5*j)+(25*k)+84)%125 + 1) for i in range(1,6)] for j in range(0,5)] for k in range(0,5)]
  magic_cube_3d_perfect = [
      # Layer 1
      [
          [25, 16, 80, 104, 90],
          [115, 98, 4, 1, 97],
          [42, 111, 85, 2, 75],
          [66, 72, 27, 102, 48],
          [67, 18, 119, 106, 5]
      ],
      
      # Layer 2
      [
          [91, 77, 71, 6, 70],
          [52, 64, 117, 69, 13],
          [30, 118, 21, 123, 23],
          [26, 39, 92, 44, 114],
          [116, 17, 14, 73, 95]
      ],
      
      # Layer 3
      [
          [47, 61, 45, 76, 86],
          [107, 43, 38, 33, 94],
          [89, 68, 63, 58, 37],
          [32, 93, 88, 83, 19],
          [40, 50, 81, 65, 79]
      ],
      
      # Layer 4
      [
          [31, 53, 112, 109, 10],
          [12, 82, 34, 87, 100],
          [103, 3, 105, 8, 96],
          [113, 57, 9, 62, 74],
          [56, 120, 55, 49, 35]
      ],
      
      # Layer 5
      [
          [121, 108, 7, 20, 59],
          [29, 28, 122, 125, 11],
          [51, 15, 41, 124, 84],
          [78, 54, 99, 24, 60],
          [36, 110, 46, 22, 101]
      ]
  ]
  cubes = [init_cube1, init_cube2, init_cube3, magic_cube_3d_perfect]
  cubes_flatten = [np.array(init_cube1).flatten().tolist(),
                  np.array(init_cube2).flatten().tolist(),
                  np.array(init_cube3).flatten().tolist(),
                  np.array(magic_cube_3d_perfect).flatten().tolist()]

  # Test, Pick cube and algorithm as you see fit
  cube_version = 0
      # 0 = init_cube1 
      # 1 = init_cube2
      # 2 = init_cube3
      # 3 = magic_cube_3d_perfect
    
  test_cube_3d = cubes[cube_version]
  test_cube_1d = cubes_flatten[cube_version]
    
  # Pick algorithm
  algorithm = 4
      # 0 = Hill Climbing sideways
      # 1 = Hill Climbing steepest ascent
      # 2 = Hill Climbing random restart
      # 3 = Simulated Annealing
      # 4 = Genetic Algorithm
      # 5 = Stochastic Hill Climbing Algorithm

  # Note : The results are done with init_cube1

  #  ===============================================================================================================================
  # Hill climbing Sideways Move Test ===============================================================================================
  if algorithm == 0:
    
    print('New code test hill climbing sideways')
    start_time = time.time()
    cubes_new, values_new, count_iter_new = HillClimbingWithSidewaysMoveCube(test_cube_1d, 100)
    end_time = time.time()
    print(f'Execution Time (New Code): {end_time - start_time:.4f} seconds')
    # Result: 
    # Current val: 45 | Neighbor Val: 45 | Sideways Count: 100
    # Execution Time (New Code): 108.7507 seconds
  
  #  =================================================================================================================================
  # Hill climbing Steepest Ascent Test ===============================================================================================

  if algorithm == 1 :
    print('New code test hill climbing steepest ascent')
    start_time = time.time()
    cubes_new, values_new, count_iter_new = SteepestAscentHillClimbingCube(test_cube_1d)
    end_time = time.time()
    print(f'Execution Time (New Code): {end_time - start_time:.4f} seconds')
    # Result:
    # Current val:  44
    # Execution Time (New Code): 23.9999 second

  #  =================================================================================================================================
  # Hill climbing Random Restart Test ===============================================================================================

  if algorithm == 2 :
    print('New code test hill climbing Random Restart')
    start_time = time.time()
    cubes_per_restart_new, values_per_restart_new, iteration_per_restart_new, restart_new= RandomRestartHillClimbingCube(test_cube_1d, 3)
    end_time = time.time()
    print(f'Execution Time (New Code): {end_time - start_time:.4f} seconds')
    # Result: 
    # Execution Time (New Code): 99.3183 seconds
    
  #  =================================================================================================================================
  # Simulated Annealing Test  ===============================================================================================

  if algorithm == 3 :
    print('New code test Simulated Annealing')
    start_time = time.time()
    cubes_new, values_new, count_iter_new, e_probs_new, count_stuck_new = SimulatedAnnealingCube(test_cube_1d, 10000, 0.99)
    end_time = time.time()
    print(f'Value {values_new[-1]}')
    print(f'Execution Time (New Code): {end_time - start_time:.4f} seconds')
    # Result:
    
    
  #  =================================================================================================================================
  # Genetic Algorithm Test ===============================================================================================

  if algorithm == 4 :
    print('Genetic Algorithm')
    start_time = time.time()
    current_max_fit, values, cubes, count_iter = genetic(400,3000)
    end_time = time.time()
    print(f'Value {values[-1]}')
    print(f'Execution Time: {end_time - start_time:.4f} seconds')
    
  #  =================================================================================================================================
  # Stochastic Algorithm Test ===============================================================================================

  if algorithm == 5 :
    print('New code test Stochastic Hill Climbing')
    start_time = time.time()
    cubes_new, values_new, iter_new = StochasticHillClimbingCube(test_cube_1d, 1000)
    end_time = time.time()
    print(f'Value {values_new[-1]}')
    print(f'Execution Time (New Code): {end_time - start_time:.4f} seconds')
    # Result:
    # Value 20
    # Execution Time (New Code): 0.4083 seconds
    
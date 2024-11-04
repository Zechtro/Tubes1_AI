import sys

from matplotlib import pyplot as plt
import numpy as np
from GeneticAlgorithm import genetic
from HillClimbingWithSidewaysMove import HillClimbingWithSidewaysMoveCube
from RandomRestartHillClimbing import RandomRestartHillClimbingCube
from SimulatedAnnealing import SimulatedAnnealingCube
from SteepestAscentHillClimbing import SteepestAscentHillClimbingCube
from StochasticHillClimbing import StochasticHillClimbingCube
from Cube import Cube, random_1d_array
import os
import json
from datetime import datetime


def output(cubes, current_max_fit, values):
    print("Initial state : ")
    cubes[0].print_cube()
    print(f"Initial state value : {values[0]}")

    print("Final state:")
    current_max_fit.print_cube()
    print(f"Final state value : {values[-1]}")
    
    generate_json(cubes)
    
    def displayPlotValuePerIteration(values):
        array = np.array(values)
        
        x = np.arange(1, len(array) + 1)

        plt.figure(figsize=(8, 5))
        plt.plot(x, array, marker='o', linestyle='-', color='b', label='Objective Function Value')
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Value')
        plt.title('Objective Function per Iteration')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    print("\n=== Displaying Values on each iteration ===\n")
    print("Pro Tip: Open another terminal and run the gui.py program and see the change on the iteration where the objective function value is also changing in the plot")
    displayPlotValuePerIteration(values)
    

def generate_json(cubes):
    cube_arrays = [cube.array for cube in cubes]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cubes_{timestamp}"
    json_file_path = os.path.join(os.path.dirname(__file__), f"../{filename}.json")
    with open(json_file_path, "w") as json_file:
        json.dump(cube_arrays, json_file, indent=4)
        
    print(f"Result written in {filename}.json")
    
def genetic_algorithm(N, max_generations):
    print(f"Running Genetic Algorithm with N={N}, max_generations={max_generations}")
    current_max_fit, values, avg_values, cubes, generation = genetic(N=N, max_generations=max_generations)
    output(cubes=cubes,current_max_fit=current_max_fit, values=values)

    return "Genetic Algorithm Result"

def hill_climbing_with_sideways(max_sideways):
    print(f"Running Hill Climbing with Sideways Move, max_sideways={max_sideways}")
    cubes, values, count_iter = HillClimbingWithSidewaysMoveCube(random_1d_array(5), max_sideways=max_sideways)
    output(cubes, cubes[-1] , values=values)
    return "Hill Climbing with Sideways Result"

def random_restart_hill_climbing(max_restart):
    print(f"Running Random Restart Hill Climbing, max_restart={max_restart}")
    cubes_per_restart, values_per_restart, iteration_per_restart, restart = RandomRestartHillClimbingCube(random_1d_array(5), max_restart=max_restart)
    cubes_per_restart = [inner_array for outer_array in cubes_per_restart for inner_array in outer_array]
    values_per_restart = [item for sublist in values_per_restart for item in sublist]
    current_max_fit = max(cubes_per_restart, key=lambda x: x.state_value)
    output(cubes_per_restart,current_max_fit,values_per_restart )
    return "Random Restart Hill Climbing Result"

def simulated_annealing(initial_temperature, cooling_rate):
    print(f"Running Simulated Annealing, initial temperature = {initial_temperature}, cooling rate = {cooling_rate}")
    cubes, values, count_iter, e_probs, count_stuck = SimulatedAnnealingCube(random_1d_array(5), initial_temperature=initial_temperature, cooling_rate=cooling_rate)
    output(cubes, current_max_fit=cubes[-1], values=values )
    return "Simulated Annealing Result"

def steepest_ascent_hill_climbing():
    print("Running Steepest Ascent Hill Climbing")
    cubes, values, count_iter = SteepestAscentHillClimbingCube(random_1d_array(5))
    output(cubes, cubes[-1],values)
    return "Steepest Ascent Hill Climbing Result"

def stochastic_hill_climbing(max_iterations):
    print("Running Stochastic Hill Climbing")
    cubes, values, iter = StochasticHillClimbingCube(random_1d_array(5), max_iter=max_iterations )
    output(cubes,cubes[-1],values)
    return "Stochastic Hill Climbing Result"

# Main function for the menu
def main():
    print("Choose an algorithm to run:")
    print("1. Genetic Algorithm")
    print("2. Hill Climbing with Sideways Move")
    print("3. Random Restart Hill Climbing")
    print("4. Simulated Annealing")
    print("5. Steepest Ascent Hill Climbing")
    print("6. Stochastic Hill Climbing")

    choice = input("Enter the number of the algorithm you want to run (1-6): ")

    if choice == '1':
        N = int(input("Enter the maximum population size (N): "))
        max_generations = int(input("Enter the maximum number of generations: "))
        result = genetic_algorithm(N, max_generations)

    elif choice == '2':
        max_sideways = int(input("Enter the maximum number of sideways moves allowed: "))
        result = hill_climbing_with_sideways(max_sideways)

    elif choice == '3':
        max_restart = int(input("Enter the maximum number of restarts allowed: "))
        result = random_restart_hill_climbing(max_restart)

    elif choice == '4':
        initial_temperature = int(input("Enter Initial Temperature: "))
        cooling_rate = float(input("Enter cooling rate: "))
        result = simulated_annealing(initial_temperature=initial_temperature, cooling_rate=cooling_rate)

    elif choice == '5':
        result = steepest_ascent_hill_climbing()

    elif choice == '6':
        max_iter = int(input("Enter the maximum number of iterations allowed: "))
        result = stochastic_hill_climbing(max_iter)

    else:
        print("Invalid choice. Please select a number between 1 and 6.")
        sys.exit(1)

    print("\nAlgorithm result:")
    print(result)

if __name__ == "__main__":
    main()

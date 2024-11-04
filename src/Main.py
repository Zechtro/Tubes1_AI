import sys
from GeneticAlgorithm import genetic
from HillClimbingWithSidewaysMove import HillClimbingWithSidewaysMoveCube
from RandomRestartHillClimbing import RandomRestartHillClimbingCube
from SimulatedAnnealing import SimulatedAnnealingCube
from SteepestAscentHillClimbing import SteepestAscentHillClimbingCube
from StochasticHillClimbing import StochasticHillClimbingCube
from Cube import Cube

def genetic_algorithm(N, max_generations):
    print(f"Running Genetic Algorithm with N={N}, max_generations={max_generations}")
    current_max_fit, values, avg_values, cubes, generation = genetic(N=N, max_generations=max_generations)
    print("Final solution:")
    current_max_fit.print_cube()

    return "Genetic Algorithm Result"

def hill_climbing_with_sideways(max_sideways):
    print(f"Running Hill Climbing with Sideways Move, max_sideways={max_sideways}")
    cubes, values, count_iter = HillClimbingWithSidewaysMoveCube(Cube(5,5,5,True), max_sideways=max_sideways)
    return "Hill Climbing with Sideways Result"

def random_restart_hill_climbing(max_restart):
    print(f"Running Random Restart Hill Climbing, max_restart={max_restart}")
    cubes_per_restart, values_per_restart, iteration_per_restart, restart = RandomRestartHillClimbingCube(Cube(5,5,5,True), max_restart=max_restart)
    return "Random Restart Hill Climbing Result"

def simulated_annealing():
    print("Running Simulated Annealing")
    cubes, values, count_iter, e_probs, count_stuck = SimulatedAnnealingCube(Cube(5,5,5,True), 1000,0.99)
    return "Simulated Annealing Result"

def steepest_ascent_hill_climbing():
    print("Running Steepest Ascent Hill Climbing")
    cubes, values, count_iter = SteepestAscentHillClimbingCube(Cube(5,5,5,True))
    return "Steepest Ascent Hill Climbing Result"

def stochastic_hill_climbing(max_iterations):
    print("Running Stochastic Hill Climbing")
    cubes, values, iter = StochasticHillClimbingCube(Cube(5,5,5,True), max_iter=max_iterations )
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
        result = simulated_annealing()

    elif choice == '5':
        result = steepest_ascent_hill_climbing()

    elif choice == '6':
        max_restart = int(input("Enter the maximum number of iterations allowed: "))
        result = stochastic_hill_climbing()

    else:
        print("Invalid choice. Please select a number between 1 and 6.")
        sys.exit(1)

    print("\nAlgorithm result:")
    print(result)

if __name__ == "__main__":
    main()

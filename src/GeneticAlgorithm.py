import random
import heapq
import multiprocessing as mp
import Cube as c

def mutate(child, mutation_rate=0.01):
    size = len(child.array)
    if random.random() < mutation_rate:
        i, j = random.sample(range(size), 2)
        child.array[i], child.array[j] = child.array[j], child.array[i]
    child.calculate_state_value()
    return child

def crossover(parent1, parent2):
    size = len(parent1.array)
    child1_array = [None] * size
    child2_array = [None] * size
    start, end = sorted(random.sample(range(size), 2))
    
    child1_array[start : end+1] = parent1.array[start : end+1]
    child2_array[start : end+1] = parent2.array[start : end+1]

    used1 = set(child1_array[start : end+1])
    used2 = set(child2_array[start : end+1])
    
    # Create remaining values lists
    remaining1 = [x for x in parent2.array if x not in used1]
    remaining2 = [x for x in parent1.array if x not in used2]

    idx1 = idx2 = 0
    for i in range(size):
        if i < start or i > end:
            child1_array[i] = remaining1[idx1]
            child2_array[i] = remaining2[idx2]
            idx1 += 1
            idx2 += 1
    
    child1 = c.Cube(parent1.x_size, parent1.y_size, parent1.z_size, array=child1_array)
    child2 = c.Cube(parent2.x_size, parent2.y_size, parent2.z_size, array=child2_array)
    
    return child1, child2

def roulette_wheel_selection(population):
    total_fitness = sum(ind.state_value for ind in population)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual in population:
        current += individual.state_value
        if current > pick:
            return individual

def create_child_task(args):
    parent1, parent2, mutation_rate = args
    child1, child2 = crossover(parent1, parent2)
    child1 = mutate(child1, mutation_rate)
    child2 = mutate(child2, mutation_rate)
    return child1 if child1.state_value > child2.state_value else child2

def genetic(N=100, max_generations=1000, initial_mutation_rate=0.05, stagnation_limit=100):
    population = [c.Cube(5, 5, 5, True) for _ in range(N)]
    current_max_fit = max(population, key=lambda x: x.state_value)
    values = [current_max_fit.state_value]
    avg_values = [sum(ind.state_value for ind in population) / N]
    no_improvement_count = 0
    mutation_rate = initial_mutation_rate
    elite_size = int(0.05 * N)
    cubes = []
    with mp.Pool(mp.cpu_count()) as pool:
        for generation in range(max_generations):
            new_population = heapq.nlargest(elite_size, population, key=lambda x: x.state_value)


            mutation_rate = min(0.3, mutation_rate * 1.2) if no_improvement_count > stagnation_limit / 2 else initial_mutation_rate

            tasks = [
                (roulette_wheel_selection(population), roulette_wheel_selection(population), mutation_rate)
                for _ in range((N - elite_size))
            ]

            children = pool.map(create_child_task, tasks)
            new_population.extend(children)

            population = heapq.nlargest(N, new_population, key=lambda x: x.state_value)

            best_child = population[0]

            if best_child.state_value > current_max_fit.state_value:
                current_max_fit = best_child
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if(generation%100 == 0):
                print(f"Generation {generation}: Current max fitness = {current_max_fit.state_value}")

            if no_improvement_count >= stagnation_limit:
                print("STAGNATION ALERT !!!")
                random_individuals = [c.Cube(5, 5, 5, True) for _ in range(int(0.5 * N))]
                population = population[:int(0.5 * N)] + random_individuals
                no_improvement_count = 0

            values.append(current_max_fit.state_value)
            cubes.append(current_max_fit)
            avg_values.append(sum(ind.state_value for ind in population) / N)

        print("Final solution:")
        current_max_fit.print_cube()

    return current_max_fit, values, avg_values, cubes, generation + 1

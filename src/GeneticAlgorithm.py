import random
import heapq
import Cube as c

def mutate(child, mutation_rate=0.01):
    size = len(child.array)
    if random.random() < mutation_rate:
        i, j = random.sample(range(size), 2)
        child.array[i], child.array[j] = child.array[j], child.array[i]
    child.calculate_state_value()
    # print('mutate')
    return child

def crossover(parent1, parent2):
    size = len(parent1.array)
    child1_array = [None] * size
    child2_array = [None] * size
    start, end = sorted(random.sample(range(size), 2))
    child1_array[start : end + 1] = parent1.array[start : end + 1]
    child2_array[start : end + 1] = parent2.array[start : end + 1]

    def fill_remaining(child, parent):
        current_pos = (end + 1) % size
        for gene in parent:
            if gene not in child:
                while child[current_pos] is not None:
                    current_pos = (current_pos + 1) % size
                child[current_pos] = gene

    fill_remaining(child1_array, parent2.array)
    fill_remaining(child2_array, parent1.array)
    
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

def genetic(N=100, max_generations=1000, initial_mutation_rate=0.05, stagnation_limit=100):
    population = [c.Cube(5, 5, 5, True) for _ in range(N)]
    current_max_fit = max(population, key=lambda x: x.state_value)
    values = [current_max_fit.state_value]
    no_improvement_count = 0
    mutation_rate = initial_mutation_rate
    elite_size = int(0.05 * N)
    cubes = []
    for generation in range(max_generations):
        new_population = heapq.nlargest(elite_size, population, key=lambda x: x.state_value)
        

        if no_improvement_count > stagnation_limit / 2:
            mutation_rate = min(0.3, mutation_rate * 1.2)
        else:
            mutation_rate = initial_mutation_rate

        while len(new_population) < N:
            parent1, parent2 = roulette_wheel_selection(population), roulette_wheel_selection(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])

        population = heapq.nlargest(N, new_population, key=lambda x: x.state_value)
        best_child = population[0]
        print(f"largest {population[0].state_value}")
        print(f"smallest {population[-1].state_value}")

        if best_child.state_value > current_max_fit.state_value:
            current_max_fit = best_child
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        print(f"Generation {generation}: Current max fitness = {current_max_fit.state_value}")

        if no_improvement_count >= stagnation_limit:
            print("STAGNATION ALERT !!!")
            random_individuals = [c.Cube(5, 5, 5, True) for _ in range(int(0.3 * N))]
            population = population[:int(0.7 * N)] + random_individuals
            no_improvement_count = 0

        values.append(current_max_fit.state_value)
        cubes.append(current_max_fit)

    print("Final solution:")
    current_max_fit.print_cube()
    return current_max_fit, values, cubes, generation + 1

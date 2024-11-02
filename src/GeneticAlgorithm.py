
import random
import multiprocessing as mp
import Cube as c

def mutate(child, mutation_rate=0.01):
    size = len(child.array)
    if random.random() < mutation_rate:
        i, j = random.sample(range(size), 2)
        child.array[i], child.array[j] = child.array[j], child.array[i]
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

def create_child_task(args):
    parent1, parent2, mutation_rate = args
    child1, child2 = crossover(parent1, parent2)
    # Apply mutation to both children
    child1 = mutate(child1, mutation_rate)
    child2 = mutate(child2, mutation_rate)
    return child1, child2

# N : Total Population
# max_generations : Total maximum Iteration

def genetic(N=100, max_generations=1000, mutation_rate=0.01, stagnation_limit=1000, pool=None):
    population = [c.Cube(5, 5, 5, True) for _ in range(N)]
    population = sorted(population, key=lambda x: x.state_value)
    values = []
    count_iter = 0
    
    current_max_fit = population[-1]
    values.append(current_max_fit.state_value)
    no_improvement_count = 0

    for generation in range(max_generations):
        count_iter += 1
        new_population = []
        elite_size = int(0.15 * N)
        new_population.extend(population[-elite_size:])

        tasks = [(roulette_wheel_selection(population), roulette_wheel_selection(population), mutation_rate) for _ in range((N - elite_size) // 2)]

        if pool:
            children_pairs = pool.map(create_child_task, tasks)
        else:
            children_pairs = [create_child_task(task) for task in tasks]

        for child1, child2 in children_pairs:
            if child1 is not None and child2 is not None:
                new_population.extend([child1, child2])

        new_population = sorted(new_population, key=lambda x: x.state_value)[:N]
        best_child = new_population[-1]

        if best_child.state_value > current_max_fit.state_value:
            current_max_fit = best_child
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        print(f"Generation {generation}: Current max fitness = {current_max_fit.state_value}")

        if current_max_fit.state_value == 109:
            print("Solution found!")
            break
        if no_improvement_count >= stagnation_limit:
            print("No improvement for several generations, stopping early.")
            break

        population = new_population
        values.append(current_max_fit.state_value)

    print("Final solution:")
    current_max_fit.print_cube()
    return current_max_fit, values, count_iter

# Only create the pool and run the function if this file is executed directly
if __name__ == "__main__":
    pool = mp.Pool(mp.cpu_count())
    try:
        genetic(1000, pool=pool)
    finally:
        pool.close()
        pool.join()
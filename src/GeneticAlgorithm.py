
import random
import copy
import multiprocessing as mp


def objective_function(cube):
    arr = []
    arr += (
        check_rows(cube)
        + check_columns(cube)
        + check_pillars(cube)
        + check_plane_diagonals(cube)
        + check_space_diagonals(cube)
    )
    return sum(1 for el in arr if el == cube.magic_number)

# To reduce load, decided to create Class cube, represents cube as 1D array
class Cube:
    def __init__(self, x_size, y_size, z_size, random=False, array=None):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.array = [None] * (self.x_size * self.y_size * self.z_size)
        self.magic_number = (
            x_size * (x_size**3 + 1) // 2
            if x_size == y_size and y_size == z_size
            else None
        )
        if random:
            self.random_cube()
            self.state_value = objective_function(self)
        if array:
            self.array = array
            self.state_value = objective_function(self)

    def random_cube(self):
        numbers = list(range(1, self.x_size**3 + 1))
        random.shuffle(numbers)
        self.array = numbers

    def to_index(self, x, y, z):
        return x * (self.y_size * self.z_size) + y * (self.z_size) + z

    def insert_value(self, x, y, z, value):
        self.array[self.to_index(x, y, z)] = value

    def get_value(self, x, y, z):
        return self.array[self.to_index(x, y, z)]

    def delete_value(self, x, y, z):
        index = self.to_index(x, y, z)
        value = self.array[index]
        self.array[index] = None
        return value

    def print_cube(self):
        for x in range(self.x_size):
            print(f"Layer {x}:")
            for y in range(self.y_size):
                row = [self.array[self.to_index(x, y, z)] for z in range(self.z_size)]
                print(row)
            print()

    def copy(self):
        new_array = copy.deepcopy(self.array)
        new_cube = Cube(self.x_size, self.y_size, self.z_size, array=new_array)
        new_cube.state_value = self.state_value
        return new_cube


def check_rows(cube):
    size = cube.x_size
    arr = []
    for x in range(size):
        for y in range(size):
            row_sum = sum(cube.get_value(x, y, z) for z in range(size))
            arr.append(row_sum)
    return arr


def check_columns(cube):
    size = cube.x_size
    arr = []
    for x in range(size):
        for z in range(size):
            col_sum = sum(cube.get_value(x, y, z) for y in range(size))
            arr.append(col_sum)
    return arr


def check_pillars(cube):
    size = cube.x_size
    arr = []
    for y in range(size):
        for z in range(size):
            pillar_sum = sum(cube.get_value(x, y, z) for x in range(size))
            arr.append(pillar_sum)
    return arr


def check_space_diagonals(cube):
    size = cube.x_size
    diag1 = sum(cube.get_value(i, i, i) for i in range(size))
    diag2 = sum(cube.get_value(i, i, size - i - 1) for i in range(size))
    diag3 = sum(cube.get_value(i, size - i - 1, i) for i in range(size))
    diag4 = sum(cube.get_value(i, size - i - 1, size - i - 1) for i in range(size))
    return [diag1, diag2, diag3, diag4]


def check_plane_diagonals(cube):
  arr = []
  size = cube.x_size
  for x in range(size):
      diag1 = sum(cube.get_value(x, i, i) for i in range(size))
      diag2 = sum(cube.get_value(x, i, size - i - 1) for i in range(size))
      arr.append(diag1)
      arr.append(diag2)
      
  for y in range(size):
      diag1 = sum(cube.get_value(i, y, i) for i in range(size))
      diag2 = sum(cube.get_value(size - i - 1, y, i) for i in range(size))
      arr.append(diag1)
      arr.append(diag2)
      
  for z in range(size):
      diag1 = sum(cube.get_value(i, i, z) for i in range(size))
      diag2 = sum(cube.get_value(size - i - 1, i, z) for i in range(size))
      arr.append(diag1)
      arr.append(diag2)
      
  return arr


def objective_function_view(cube):
    arr = []
    arr += (
        check_rows(cube)
        + check_columns(cube)
        + check_pillars(cube)
        + check_plane_diagonals(cube)
        + check_space_diagonals(cube)
    )
    print(arr)

def mutate(child, mutation_rate=0.01):

    size = len(child.array)
    if random.random() < mutation_rate:
        print("Mutation")
        i, j = random.sample(range(size), 2)
        child.array[i], child.array[j] = child.array[j], child.array[i]

    return child


def crossover(parent1, parent2):
    size = parent1.x_size * parent1.y_size * parent1.z_size
    child1_array = [None] * size
    child2_array = [None] * size
    start, end = sorted(random.sample(range(size), 2))
    child1_array[start : end + 1] = parent1.array[start : end + 1]
    child2_array[start : end + 1] = parent2.array[start : end + 1]

    def fill_remaining(child, parent):
        current_pos = (end + 1) % size
        for gene in parent:
            if gene not in child:
                child[current_pos] = gene
                current_pos = (current_pos + 1) % size

    fill_remaining(child1_array, parent2.array)
    fill_remaining(child2_array, parent1.array)
    child1 = Cube(5, 5, 5, False, child1_array)
    child2 = Cube(5, 5, 5, False, child2_array)
    return child1 if child1.state_value > child2.state_value else child2


def roulette_wheel_selection(population):
    total_fitness = sum(ind.state_value for ind in population)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual in population:
        current += individual.state_value
        if current > pick:
            return individual


def create_child_task(args):
    """Task to create a child in parallel"""
    parent1, parent2, mutation_rate = args
    child = mutate(crossover(parent1, parent2), mutation_rate)
    return child


def genetic(N=100, mutation_rate=0.01):
    # Generate N population
    population = [Cube(5, 5, 5, True) for _ in range(N)]
    population = sorted(population, key=lambda x: x.state_value)
    current_max_fit = population[-1]
    is_fit_enough = current_max_fit.state_value == 109

    pool = mp.Pool(mp.cpu_count())

    while not is_fit_enough:
        new_population = []
        elite_size = int(0.15 * N)
        new_population.extend(population[-elite_size:])

        tasks = [
            (
                roulette_wheel_selection(population),
                roulette_wheel_selection(population),
                mutation_rate,
            )
            for _ in range(N - elite_size)
        ]

        children = pool.map(create_child_task, tasks)

        for child in children:
            if len(child.array) != len(set(child.array)):
                print("Something went wrong")
                pool.close()
                pool.join()
                return

            new_population.append(child)

            if child.state_value > current_max_fit.state_value:
                current_max_fit = child

            print("Current max " + str(current_max_fit.state_value))

        population = sorted(new_population, key=lambda x: x.state_value)
        is_fit_enough = current_max_fit.state_value == 109

    pool.close()
    pool.join()
    print("Final child:")
    current_max_fit.print_cube()


if __name__ == "__main__":
    genetic(1000)
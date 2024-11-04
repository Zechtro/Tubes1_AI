import random
import copy
import time

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
    
    def calculate_state_value(self):
        self.state_value = objective_function(self)

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


def generate_successor(curr_cube_arr):
    successors = []
    n = len(curr_cube_arr)
    for i in range(n):
        for j in range(i + 1, n):
            new_arr = curr_cube_arr[:]
            new_arr[i], new_arr[j] = new_arr[j], new_arr[i]
            successors.append(Cube(5, 5, 5, False, new_arr))
    return successors

def random_1d_array(n):
  numbers = list(range(1, n**3 + 1))
  random.shuffle(numbers)
  return numbers

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

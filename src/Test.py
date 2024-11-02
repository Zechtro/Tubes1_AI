from ObjFunct import objFunc
from Cube import Cube
import numpy as np

def to_3d_array(cube_1d, x_size=5, y_size=5, z_size=5):
    cube_3d = []
    for x in range(x_size):
        layer = []
        for y in range(y_size):
            row = cube_1d[(x * y_size * z_size) + (y * z_size): (x * y_size * z_size) + (y * z_size) + z_size]
            layer.append(row)
        cube_3d.append(layer)
    
    return cube_3d
  
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
cubes = [magic_cube_3d_perfect]


# Using previous objective function
print('Old objective function')
for index, cube in enumerate(cubes):
    print(f"Value cube {index + 1} : {objFunc(cube)}")

print()
print()
print('New objective function')
# Using new objective function
cubes_obj = [
    Cube(5, 5, 5, False, np.array(magic_cube_3d_perfect).flatten().tolist()),

]
print(f"Value cube 1: {cubes_obj[0].state_value}")
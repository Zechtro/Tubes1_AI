import time
import numpy as np

# start = time.time()

# cube = [[[0,0,0,0,0] for _ in range (5)] for _ in range (5)]

# val = 1
# for x in range(5):
#     for y in range(5):
#         for z in range(5):
#             cube[x][y][z] = val
#             val += 1
            
# end = time.time()
# print("Cube created in", end-start, "second(s)")

# for level in cube:
#     print(level)
##### 5
##### 4
##### 3
##### 2
##### 1
magicNumber = 315

def sumRow(xIdx, level):
    sum = 0
    for elmt in level[xIdx]:
        sum += elmt
    return sum

def countX(cube):
    val = 0
    for level in cube:
        for rowIdx in range(5):
            sum = sumRow(rowIdx, level)
            if(sum != magicNumber):
                val += 1
    return val

def sumCol(yIdx, level):
    sum = 0
    for x in range(5):
        sum += level[x][yIdx]
    return sum

def countY(cube):
    val = 0
    for level in cube:
        for colIdx in range(5):
            sum = sumCol(colIdx, level)
            if(sum != magicNumber):
                val += 1
    return val

def countZ(cube):
    sumTemp = [[0 for _ in range(5)] for _ in range(5)]
    for z in range(5):
        for x in range(5):
            for y in range(5):
                sumTemp[x][y] += cube[z][x][y]
                
    val = 0
    for i in range(5):
        for j in range(5):
            if(sumTemp[i][j] !=  magicNumber):
                val += 1
                
    return val
            
def countDiagXY(cube):
    val = 0
    
    for level in cube:
        sum1 = 0
        sum2 = 0
        
        for x in range(5):
            for y in range(5):
                if(x != y):
                    sum1 += level[x][y]
                    sum2 += level[x][4-y]
        
        if(sum1 != magicNumber):
            val += 1
        if(sum2 != magicNumber):
            val += 1
    
    return val

def countDiagXZ(cube):
    val = 0
    
    for y in range(5):
        sum2 = 0
        sum1 = 0
        for z in range(5):
            for x in range(5):
                if(z != x):
                    sum1 += cube[z][x][y]
                    sum2 += cube[z][4-x][y]
        
        if(sum1 != magicNumber):
            val += 1
        if(sum2 != magicNumber):
            val += 1
    
    return val
    

def countDiagYZ(cube):
    val = 0
    
    for x in range(5):
        sum2 = 0
        sum1 = 0
        for z in range(5):
            for y in range(5):
                if(z != y):
                    sum1 += cube[z][x][y]
                    sum2 += cube[z][x][4-y]
        
        if(sum1 != magicNumber):
            val += 1
        if(sum2 != magicNumber):
            val += 1
    
    return val

def countDiagRuang(cube):
    val = 0
    
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    
    for z in range(5):
        for x in range(5):
            for y in range(5):
                if(z != x != y):
                    sum1 += cube[z][x][y]
                    sum2 += cube[4-z][x][y]
                    sum3 += cube[z][4-x][y]
                    sum4 += cube[z][x][4-y]
    
    if(sum1 != magicNumber):
        val += 1
    if(sum2 != magicNumber):
        val += 1
    if(sum3 != magicNumber):
        val += 1
    if(sum4 != magicNumber):
        val += 1
    
    return val

def objFunc(cube):
    val = 0
    
    val += countX(cube)
    val += countY(cube)
    val += countZ(cube)
    val += countDiagXY(cube)
    val += countDiagYZ(cube)
    val += countDiagXZ(cube)
    val += countDiagRuang(cube)
    
    return -val
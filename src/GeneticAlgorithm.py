import random
from ObjFunct import *

totalRule = 109

def GeneratePopulation(k=4):
    population = []
    fitnessValPopulation = []
    for _ in range(k):
        cube = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]
        initX = random.randint(0,4)
        initY = random.randint(0,4)
        initZ = random.randint(0,4)
        elmt = 1
        for z in range(5):
            for x in range(5):
                for y in range(5):
                    zIdx = (initZ+z)%5
                    xIdx = (initX+x)%5
                    yIdx = (initY+y)%5
                    cube[zIdx][xIdx][yIdx] = elmt
                    elmt += 1
        population.append(cube)
        valCube = totalRule + objFunc(cube)
        fitnessValPopulation.append(valCube)
        
    return population, fitnessValPopulation

def Roulete(fitnessValPopulation):
    fitnessProb = []
    sumVal = sum(fitnessValPopulation)
    print("FitnessValPop:",fitnessValPopulation)
    for val in fitnessValPopulation:
        if(sumVal == 0):
            fitnessProb.append(round(100/len(fitnessValPopulation)))
        else:
            fitnessProb.append(round(val*100/sumVal))
    
    print("fitness prob:", fitnessProb)
        
    wheel = [0 for _ in range(100)]
    wheelIdx = 0
    for i in range(len(fitnessProb)):
        for _ in range(fitnessProb[i]):
            wheel[wheelIdx%100] = i
            wheelIdx += 1
            
    return wheel

def RouleteSelect(roulete):
    randIdx = random.randint(0,99)
    return roulete[randIdx]

def SelectParent(population, fitnessValPopulation):
    roulete = Roulete(fitnessValPopulation)
    parent1Idx = RouleteSelect(roulete)
    parent2Idx = RouleteSelect(roulete)
    while(parent1Idx == parent2Idx):
        parent2Idx = RouleteSelect(roulete)
    return population[parent1Idx], population[parent2Idx]

def Flatten(cube):
    flattenCube = []
    for z in range(5):
        for x in range(5):
            for y in range(5):
                flattenCube.append(cube[z][x][y])
    #             if(x+y <= z):
    #                 flattenCube.append(cube[z][x][y])
    # for z in range(5):
    #     for x in range(5):
    #         for y in range(5):
    #             if(x+y > z):
    #                 flattenCube.append(cube[z][x][y])
    return flattenCube

def Unflatten(flattenCube):
    cube = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]
    flattenCubeIdx = 0
    for z in range(5):
        for x in range(5):
            for y in range(5):
                cube[z][x][y] = flattenCube[flattenCubeIdx]
                flattenCubeIdx += 1
    #             if(x+y <= z):
    #                 cube[z][x][y] = flattenCube[flattenCubeIdx]
    #                 flattenCubeIdx += 1
    # for z in range(5):
    #     for x in range(5):
    #         for y in range(5):
    #             if(x+y > z):
    #                 cube[z][x][y] = flattenCube[flattenCubeIdx]
    #                 flattenCubeIdx += 1
    return cube

def CrossOver(parent1, parent2):
    flattenParent1 = Flatten(parent1)
    flattenParent2 = Flatten(parent2)
    randomCrossIdx = random.randint(25,99)
    flattenParent1[randomCrossIdx:], flattenParent2[randomCrossIdx:] = (flattenParent2[randomCrossIdx:]), (flattenParent1[randomCrossIdx:])
    
    offspring1 = flattenParent1
    offspring2 = flattenParent2
    
    return offspring1, offspring2
    
def Mutate(offspring):
    
    unassignedNumber = [e for e in range(1,126)]
    duplicateElmtIdx = []
    
    for i, number in enumerate(offspring):
        if(number in unassignedNumber):
            unassignedNumber.remove(number)
        else:
            duplicateElmtIdx.append(i)
    
    for idx in duplicateElmtIdx:
        randIdx = random.randint(0,len(unassignedNumber)-1)
        number = unassignedNumber[randIdx]
        offspring[idx] = number
        unassignedNumber.remove(number)
    
    cubeOffspring = Unflatten(offspring)
    return cubeOffspring

def GeneticAlgorithm(k, maxIter):
    population, fitnessValPopulation = GeneratePopulation(k)
    
    iter = 0
    bestVal = -1
    bestCube = []
    bestCubeCurrPopulationIdx = -1
    
    while(iter < maxIter):
        print("Iteration:",iter)
        
        newPopulation = []
        newfitnessValPopulation = []
        bestVal = -1
        bestCubeCurrPopulationIdx = -1
        currNewPopulationIdx = 0
        
        while(len(newPopulation) < k):
            parent1, parent2 = SelectParent(population, fitnessValPopulation)
            
            offspring1, offspring2 = CrossOver(parent1, parent2)
            
            offspring1 = Mutate(offspring1)
            fitnessValOffspring1 = totalRule+objFunc(offspring1)
            
            if(bestVal == -1 or bestVal < fitnessValOffspring1):
                bestVal = fitnessValOffspring1
                bestCube = offspring1[:]
                bestCubeCurrPopulationIdx = currNewPopulationIdx
            
            newPopulation.append(offspring1)
            newfitnessValPopulation.append(fitnessValOffspring1)
            currNewPopulationIdx += 1
            
            # Untuk menghandle jika jumlah populasi ganjil
            if(len(newPopulation) < k):
                offspring2 = Mutate(offspring2)
                fitnessValOffspring2 = totalRule+objFunc(offspring2)
                
                if(bestVal == -1 or bestVal < fitnessValOffspring2):
                    bestVal = fitnessValOffspring2
                    bestCube = offspring2[:]
                    bestCubeCurrPopulationIdx = currNewPopulationIdx
                
                newPopulation.append(offspring2)
                newfitnessValPopulation.append(fitnessValOffspring2)
                currNewPopulationIdx += 1
                
        population = newPopulation[:]
        fitnessValPopulation = newfitnessValPopulation[:]
        print("NewFitnessValPop:", newfitnessValPopulation)
        
        iter += 1
        
        print("Fitness Funct:", fitnessValPopulation)
    
    print("Best fitness funct:",bestVal)
    return population[bestCubeCurrPopulationIdx], fitnessValPopulation[bestCubeCurrPopulationIdx]

for level in (GeneticAlgorithm(40,10000)):
    print(level)
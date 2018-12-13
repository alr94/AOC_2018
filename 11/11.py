import math

def BuildGrid(gridSerialNumber, gridSize):
    
    grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]
    
    for x in range(gridSize):
        for y in range(gridSize):
            rackId = (x + 1) + 10
            powerLevel = rackId * (y + 1)
            powerLevel += gridSerialNumber
            powerLevel *= rackId
            powerLevel = math.floor(powerLevel / 100) % 10
            powerLevel = powerLevel - 5
            grid[x][y] = powerLevel
            
    return grid

def CumulativeAt(cumulatives, x, y):
    if x < 0 or y < 0: return 0
    return cumulatives[x][y]

def FindMaxSquare(grid, gridSize):
    
    cumulatives = [[0 for x in range(gridSize)] for y in range(gridSize)]
    
    for x in range(gridSize):
        for y in range(gridSize):
            cumulatives[x][y] = (grid[x][y] + 
                                 CumulativeAt(cumulatives, x - 1, y) +
                                 CumulativeAt(cumulatives, x, y - 1) -
                                 CumulativeAt(cumulatives, x - 1, y - 1))
            
    maxSquare   = None
    maxLocation = None
    for sqauresize in range(1, gridSize + 1):
        for x in range(gridSize - sqauresize):
            for y in range(gridSize - sqauresize):
                
                if x >= sqauresize - 1 and y >= sqauresize - 1:
                    thisSquare = (CumulativeAt(cumulatives, x, y) +
                                  CumulativeAt(cumulatives, x - sqauresize, 
                                               y - sqauresize) -
                                  CumulativeAt(cumulatives, x - sqauresize, y) -
                                  CumulativeAt(cumulatives, x, y - sqauresize))
                    
                    if maxSquare == None:
                        maxSquare = thisSquare
                        maxLocation = [x + 1, y + 1, sqauresize]
                    elif thisSquare > maxSquare:
                        maxSquare = thisSquare
                        maxLocation = [(x + 1) - (sqauresize - 1), 
                                       (y + 1) - (sqauresize - 1), 
                                       sqauresize]
            
    return maxLocation

gridSerialNumber = 1955
gridSize         = 300

grid = BuildGrid(gridSerialNumber, gridSize)
print (FindMaxSquare(grid, gridSize))

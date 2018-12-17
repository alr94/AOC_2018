import collections
################################################################################
# Map 

def BuildMap(inputLines):
    
    clayDeposits = collections.defaultdict(bool)
    
    for line in inputLines:
        
        if line[0] == 'x':
            
            xVal = int(line.split(',')[0].split('=')[1])
            yMin = int(line.split(',')[1].split('=')[1].split('..')[0])
            yMax = int(line.split(',')[1].split('=')[1].split('..')[1])
            
            for yVal in range(yMin, yMax + 1):
                clayDeposits[(xVal, yVal)] = True
                
        else:
            
            yVal = int(line.split(',')[0].split('=')[1])
            xMin = int(line.split(',')[1].split('=')[1].split('..')[0])
            xMax = int(line.split(',')[1].split('=')[1].split('..')[1])
            
            for xVal in range(xMin, xMax + 1):
                clayDeposits[(xVal, yVal)] = True
    
    xRange       = [min([x[0] for x in clayDeposits.keys()]),
                    max([x[0] for x in clayDeposits.keys()])] 
    
    yRange       = [min([x[1] for x in clayDeposits.keys()]),
                    max([x[1] for x in clayDeposits.keys()])]
    
    return clayDeposits, xRange, yRange
    
def PrintMap(clayDeposits, waterLocations, staticWaterLocations, xRange, 
             yRange):
    
    for y in range(0, yRange[1] + 2):
        line = ''
        for x in range(xRange[0] - 2, xRange[1] + 3):
            
            if [x, y] == [500, 0]: line += '+'
            elif clayDeposits[(x, y)]: line += '#'
            elif ( x, y ) in staticWaterLocations: line += '~'
            elif ( x, y ) in waterLocations: line += '|'
            else: line += '.'
            
        print (line)
        
################################################################################
# Water propagation

def PropagateWater(clayDeposits, xRange, yRange):
    
    waterFronts          = [[500, 0]]
    waterLocations       = set()
    staticWaterLocations = set()
    spawnPoints          = set()
    
    while len(waterFronts) > 0:
        
        for i in range(len(waterFronts) - 1, -1, -1):
            
            if waterFronts[i][1] > yRange[1]: 
                del waterFronts[i]
                continue
            
            # Try down first
            movedDown = False
            while True:
                
                newLocation = [waterFronts[i][0] + 0, waterFronts[i][1] + 1]
                
                if newLocation[1] > yRange[1]:
                    waterFronts[i] = newLocation
                    movedDown = True
                    break
                    
                elif ((not clayDeposits[newLocation[0], newLocation[1]]) and 
                      ((newLocation[0], newLocation[1]) not in staticWaterLocations)):
                        waterFronts[i] = newLocation
                        if (waterFronts[i][0], waterFronts[i][1]) not in waterLocations: 
                            waterLocations.add((waterFronts[i][0], waterFronts[i][1]))
                        movedDown = True
                else:
                    break
                    
            if not movedDown: 
                
                canHaveLeftWall, canHaveRightWall = True, True
                
                while canHaveLeftWall and canHaveRightWall:
                    
                    leftWall, rightWall               = None, None
                    
                    newLocation = waterFronts[i]
                    while canHaveLeftWall and leftWall == None:
                        
                        # Try down
                        newLocation = [newLocation[0] + 0, newLocation[1] + 1]
                        if ((not clayDeposits[newLocation[0], newLocation[1]]) and 
                            ((newLocation[0], newLocation[1]) not in staticWaterLocations)):
                               canHaveLeftWall = False
                               leftWall = newLocation
                               break
                           
                        # Try left
                        newLocation = [newLocation[0] - 1, newLocation[1] - 1]
                        if clayDeposits[newLocation[0], newLocation[1]]: 
                            leftWall = newLocation
                        
                    newLocation = waterFronts[i]
                    while canHaveRightWall and rightWall == None:
                        
                        # Try down
                        newLocation = [newLocation[0] + 0, newLocation[1] + 1]
                        if ((not clayDeposits[newLocation[0], newLocation[1]]) and 
                            ((newLocation[0], newLocation[1]) not in staticWaterLocations)):
                               canHaveRightWall = False
                               rightWall = newLocation
                               break
                           
                        # Try left
                        newLocation = [newLocation[0] + 1, newLocation[1] - 1]
                        if clayDeposits[newLocation[0], newLocation[1]]: 
                            rightWall = newLocation
                        
                    if canHaveLeftWall and canHaveRightWall:
                        
                        for x in range(leftWall[0] + 1, rightWall[0]):
                            location = [x, waterFronts[i][1]]
                            if (location[0], location[1]) not in waterLocations:
                                waterLocations.add(( x, waterFronts[i][1] ))
                            if (location[0], location[1]) not in staticWaterLocations:
                                staticWaterLocations.add(( x, waterFronts[i][1] ))
                            
                        waterFronts[i] = [waterFronts[i][0], waterFronts[i][1] - 1]
                        
                    elif canHaveLeftWall:
                        
                        for x in range(leftWall[0] + 1, rightWall[0] + 1):
                            location = [x, waterFronts[i][1]]
                            if (location[0], location[1]) not in waterLocations:
                                waterLocations.add(( x, waterFronts[i][1] ))
                            
                        del waterFronts[i]
                        
                        if ((rightWall not in waterFronts) and
                            ((rightWall[0], rightWall[1]) not in spawnPoints)):
                            waterFronts.append(rightWall)
                            spawnPoints.add((rightWall[0], rightWall[1]))
                        
                    elif canHaveRightWall:
                        
                        for x in range(leftWall[0], rightWall[0]):
                            location = [x, waterFronts[i][1]]
                            if (location[0], location[1]) not in waterLocations:
                                waterLocations.add(( x, waterFronts[i][1] ))
                        
                        del waterFronts[i]
                            
                        if ((leftWall not in waterFronts) and
                            ((leftWall[0], leftWall[1]) not in spawnPoints)):
                            waterFronts.append(leftWall)
                            spawnPoints.add((leftWall[0], rightWall[1]))
                        
                    else:
                        
                        for x in range(leftWall[0], rightWall[0] + 1):
                            location = [x, waterFronts[i][1]]
                            if (location[0], location[1]) not in waterLocations:
                                waterLocations.add(( x, waterFronts[i][1] ))
                            
                        del waterFronts[i]
                        
                        if ((leftWall not in waterFronts) and
                            ((leftWall[0], leftWall[1]) not in spawnPoints)):
                            waterFronts.append(leftWall)
                            spawnPoints.add((leftWall[0], leftWall[1]))
                        if ((rightWall not in waterFronts) and
                            ((rightWall[0], rightWall[1]) not in spawnPoints)):
                            waterFronts.append(rightWall)
                            spawnPoints.add((rightWall[0], rightWall[1]))
                    
        for i in range(len(waterFronts)):
            if (waterFronts[i][0], waterFronts[i][1]) not in waterLocations: 
                if ((waterFronts[i][1] <= yRange[1]) and
                    (waterFronts[i][1] >= yRange[0])):
                    waterLocations.add((waterFronts[i][0], waterFronts[i][1]))
        
        # PrintMap(clayDeposits, waterLocations, staticWaterLocations, xRange, 
        #          yRange)
        # print()
    
    return waterLocations, staticWaterLocations

################################################################################
# Run program

inputLines = [line.rstrip("\n") for line in open("input.txt")]
#inputLines = [line.rstrip("\n") for line in open("testInput.txt")]

clayDeposits, xRange, yRange = BuildMap(inputLines)

waterLocations, staticWaterLocations = PropagateWater(clayDeposits, xRange, 
                                                      yRange) 
# PrintMap(clayDeposits, waterLocations, staticWaterLocations, xRange, yRange)

print (len([location for location in waterLocations if yRange[0] <= location[1] <= yRange[1]]))
print (len(staticWaterLocations))

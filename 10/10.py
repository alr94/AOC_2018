inputLines = [ line.rstrip("\n") for line in open("input.txt") ]

positions  = []
velocities = []
for line in inputLines:
    
    positionString = line.split('<')[1].split('>')[0]
    velocityString = line.split('<')[2].split('>')[0]
    
    positions.append([int(positionString.split(',')[0]), 
                      int(positionString.split(',')[1])])
    
    velocities.append([int(velocityString.split(',')[0]),
                       int(velocityString.split(',')[1])])

prevArea               = 0
numberLargerAreasInRow = 0
numberIters            = 0

while numberLargerAreasInRow < 100:
    
    minX = maxX = minY = maxY = None
    
    for index in range(len(positions)):
        
        for coordIndex in range(len(positions[index])):
            positions[index][coordIndex] += velocities[index][coordIndex]
        
        if minX == None:
            minX = positions[index][0]
            maxX = positions[index][0]
            minY = positions[index][1]
            maxY = positions[index][1]
        else:
            if positions[index][0] < minX: minX = positions[index][0]
            if positions[index][0] > maxX: maxX = positions[index][0]
            if positions[index][1] < minY: minY = positions[index][1]
            if positions[index][1] > maxY: maxY = positions[index][1]
        
    numberIters += 1
    
    area = (maxX - minX) * (maxY - minY)
    
    if area > prevArea: numberLargerAreasInRow += 1
    
    prevArea = area
    
minPositions  = []
for line in inputLines:
    positionString = line.split('<')[1].split('>')[0]
    minPositions.append([int(positionString.split(',')[0]), 
                                int(positionString.split(',')[1])])
    
numberIters -= (numberLargerAreasInRow + 3)
for index in range(len(positions)):
    for coordIndex in range(len(positions[index])):
        minPositions[index][coordIndex] += (
                numberIters * velocities[index][coordIndex])
    
for iterIndex in range(6):
    
    numberIters += 1
    
    minX = maxX = minY = maxY = None
    
    for index in range(len(minPositions)):
        
        for coordIndex in range(len(minPositions[index])):
            minPositions[index][coordIndex] += velocities[index][coordIndex]
        
        if minX == None:
            minX = minPositions[index][0]
            maxX = minPositions[index][0]
            minY = minPositions[index][1]
            maxY = minPositions[index][1]
        else:
            if minPositions[index][0] < minX: minX = minPositions[index][0]
            if minPositions[index][0] > maxX: maxX = minPositions[index][0]
            if minPositions[index][1] < minY: minY = minPositions[index][1]
            if minPositions[index][1] > maxY: maxY = minPositions[index][1]
    
    area = (maxX - minX) * (maxY - minY)
    print (numberIters)
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if [x, y] in minPositions: print('#', end=' ')
            else: print ('.', end=' ')
        print ()
    print ('\n')
    

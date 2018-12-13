def ManhattanDistance(coordinate, location):
    return (abs(location[0] - coordinate[0]) + abs(location[1] - coordinate[1]))

def ManhattanAreas(coordinates):
    
    maxX = max([x[0] for x in coordinates])
    maxY = max([x[1] for x in coordinates])
    
    areas = {}
    infiniteCoordinates = set()
    
    for x in range(maxX + 1):
        for y in range(maxY + 1):
            
            distanceCounter = {}
            for index, coordinate in enumerate(coordinates):
                
                manhatanDistance = ManhattanDistance(coordinate, [x, y])
                if manhatanDistance in distanceCounter:
                    distanceCounter[manhatanDistance].append(index)
                else:
                    distanceCounter[manhatanDistance] = [index]
                    
            minDist = min([dist[0] for dist in distanceCounter.items()])
            
            if len(distanceCounter[minDist]) > 1:
                minIndex = -1
            else:
                minIndex = distanceCounter[minDist][0]
            
            if x == 0 or x == maxX or y == 0 or y == maxY:
                infiniteCoordinates.add(minIndex)
                
            if minIndex not in areas:
                areas[minIndex] = 1
            else:
                areas[minIndex] += 1

            
    return max(area[1] for area in areas.items() if area[0] not in infiniteCoordinates)

def SharedRegion(coordinates, rangeLimit=10000):
    
    maxX = max([x[0] for x in coordinates])
    maxY = max([x[1] for x in coordinates])
    
    sharedArea = 0
    for x in range(maxX + 1):
        for y in range(maxY + 1):
            summedDistance = sum(ManhattanDistance(coordinate,[x,y]) for
                                 coordinate in coordinates)
            if summedDistance < rangeLimit:
                sharedArea += 1
            
    return sharedArea

coordinateChars = [ line.rstrip("\n").split(',')   for line in open("input.txt") ]
coordinates = []
for coordinateChar in coordinateChars:
    coordinates.append([int(coordinateChar[0]), int(coordinateChar[1])])

print (ManhattanAreas(coordinates))
print (SharedRegion(coordinates, 10000))
    

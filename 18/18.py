import copy

openTile   = '.'
treeTile   = '|'
lumberTile = '#'

def BuildMap(inputLines):
    lumberMap = []
    for line in inputLines:
        lumberMap.append(list(line))
    return lumberMap

def PrintMap(lumberMap):
    print()
    for  line in lumberMap:
        mapLine = ''
        for entry in line:
            mapLine += str(entry)
        print (mapLine)
        
def NumberAdjacent(lumberMap, x, y, tileType):
    
    n = 0
    
    for dy in [-1, 0, 1]:
        
        if ((y + dy < 0) or (y + dy >= len(lumberMap))): continue
        
        for dx in [-1, 0, 1]:
            
            if dx == 0 and dy == 0: continue
            
            if ((x + dx < 0) or (x + dx >= len(lumberMap[y]))): continue
            
            if lumberMap[y + dy][x + dx] == tileType: n += 1
            
    return n
        

inputLines = [line.rstrip("\n") for line in open("testInput.txt")]
inputLines = [line.rstrip("\n") for line in open("input.txt")]

################################################################################
# Part 1
lumberMap = BuildMap(inputLines)
for _ in range(10):
    
    newMap     = copy.deepcopy(lumberMap)
    
    for y in range(len(lumberMap)):
        for x in range(len(lumberMap[y])):
            
            if lumberMap[y][x] == openTile:
                if NumberAdjacent(lumberMap, x, y, treeTile) >= 3:
                    newMap[y][x] = treeTile
            
            if lumberMap[y][x] == treeTile:
                if NumberAdjacent(lumberMap, x, y, lumberTile) >= 3:
                    newMap[y][x] = lumberTile
                    
            if lumberMap[y][x] == lumberTile:
                if (NumberAdjacent(lumberMap, x, y, treeTile) < 1 or
                    NumberAdjacent(lumberMap, x, y, lumberTile) < 1):
                    newMap[y][x] = openTile
            
    lumberMap = newMap

numberLumber, numberTrees = 0, 0
for y in range(len(lumberMap)):
    for x in range(len(lumberMap[y])):
        
        if lumberMap[y][x] == lumberTile: numberLumber += 1
        elif lumberMap[y][x] == treeTile: numberTrees += 1

print (numberLumber, numberTrees, numberLumber * numberTrees)

################################################################################
# Part 2

lumberMap = BuildMap(inputLines)

prevMaps        = []
mostRecentIndex = 0

timeToGo = 1000000000
for i in range(timeToGo):
    
    mostRecentIndex = i
    if lumberMap in prevMaps: break
    
    prevMaps.append(lumberMap)
    
    newMap     = copy.deepcopy(lumberMap)
    
    for y in range(len(lumberMap)):
        for x in range(len(lumberMap[y])):
            
            if lumberMap[y][x] == openTile:
                if NumberAdjacent(lumberMap, x, y, treeTile) >= 3:
                    newMap[y][x] = treeTile
            
            if lumberMap[y][x] == treeTile:
                if NumberAdjacent(lumberMap, x, y, lumberTile) >= 3:
                    newMap[y][x] = lumberTile
                    
            if lumberMap[y][x] == lumberTile:
                if (NumberAdjacent(lumberMap, x, y, treeTile) < 1 or
                    NumberAdjacent(lumberMap, x, y, lumberTile) < 1):
                    newMap[y][x] = openTile
            
    lumberMap = newMap
    

equalIndex = 0
for i, prevMap in enumerate(prevMaps):
    if lumberMap == prevMap: 
        equalIndex = i
        break

frequency = mostRecentIndex - equalIndex
recurentMaps = prevMaps[-frequency:]

numberToGoModFrequency = (timeToGo - mostRecentIndex) % frequency

lumberMap = recurentMaps[numberToGoModFrequency]
numberLumber, numberTrees = 0, 0
for y in range(len(lumberMap)):
    for x in range(len(lumberMap[y])):
        
        if lumberMap[y][x] == lumberTile: numberLumber += 1
        elif lumberMap[y][x] == treeTile: numberTrees += 1

print (numberLumber, numberTrees, numberLumber * numberTrees)

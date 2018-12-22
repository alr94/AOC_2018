import heapq

depth  = 510
tX, tY = 10, 10
depth  = 11541
tX, tY = 14,778
    
# 0 = None, 1 = Torch, 2 = Climbing Gear
toolsByRegionType = {0: [1, 2],
                     1: [0, 2],
                     2: [0, 1]}

def BuildMap(geoIndex, eroLevel, regionType, depth, tX, tY):
    
    if geoIndex == None:
        geoIndex   = {}
        eroLevel   = {}
        regionType = {}
        
    for x in range(tX + 1):
        for y in range(tY + 1):
            if (x, y) not in geoIndex:
                GeoIndex(x, y, geoIndex, eroLevel)
                EroLevel(x, y, geoIndex, eroLevel)
                RegionType(x, y, eroLevel, regionType)
    
    return geoIndex, eroLevel, regionType

def UpdateMapX(geoIndex, eroLevel, regionType, depth, X, Y):
    
    for y in range(Y + 1):
        GeoIndex(X, y, geoIndex, eroLevel)
        EroLevel(X, y, geoIndex, eroLevel)
        RegionType(X, y, eroLevel, regionType)
        
    return geoIndex, eroLevel, regionType

def UpdateMapY(geoIndex, eroLevel, regionType, depth, X, Y):
        
    for x in range(X + 1):
        GeoIndex(x, Y, geoIndex, eroLevel)
        EroLevel(x, Y, geoIndex, eroLevel)
        RegionType(x, Y, eroLevel, regionType)
    
    return geoIndex, eroLevel, regionType

def GeoIndex(x, y, geoIndex, eroLevel):
    if x == 0 and y == 0: geoIndex[(x, y)] = 0
    elif [x, y] == [tX, tY]: geoIndex[(x, y)] = 0
    elif y == 0: geoIndex[(x, y)] = x * 16807 
    elif x == 0: geoIndex[(x, y)] = y * 48271 
    else: geoIndex[(x, y)] = eroLevel[(x - 1, y)] * eroLevel[(x, y - 1)]

def EroLevel(x, y, geoIndex, eroLevel):
    eroLevel[(x, y)]   = (geoIndex[(x, y)] + depth) % 20183
    
def RegionType(x, y, eroLevel, regionType):
    regionType[(x, y)] = eroLevel[(x, y)] % 3

def CanUseTool(regionType, currentTool):
    if currentTool in toolsByRegionType[regionType]: return True
    return False

def TotalRisk(regionType, tX, tY, depth):
    return sum([val for val in regionType.values()])

def ShortestPath(geoIndex, eroLevel, regionType, tX, tY):
    
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
    
    states = [(0, 0, 0, 1)]
    times  = {(0, 0, 1): 0}
        
    maxX, maxY = tX, tY
    while states:
        
        time, x, y, tool = heapq.heappop(states)
        
        if (x, y, tool) == (tX, tY, 1): return times
        
        for direction in directions:
            
            newX, newY = x + direction[0], y + direction[1]
            
            manhattan = 8 * ((tX + tY) / 2)
            if newX < 0 or newY < 0: continue
            if newX > manhattan or newY > manhattan: continue
            
            if newX > maxX: 
                maxX = newX
                geoIndex, eroLevel, regionType = UpdateMapX(geoIndex, eroLevel,
                                                            regionType, depth, 
                                                            maxX, maxY)
            elif newY > maxY:
                maxY = newY
                geoIndex, eroLevel, regionType = UpdateMapY(geoIndex, eroLevel,
                                                            regionType, depth, 
                                                            maxX, maxY)
            
            for newTool in range(3):
                
                if not CanUseTool(regionType[(newX, newY)], newTool): continue
                if not CanUseTool(regionType[(x, y)], newTool): continue
                
                if direction == [0, 0]:
                    if newTool == tool: newTime = time
                    else:               newTime = time + 7
                else:
                    if newTool == tool: newTime = time + 1
                    else:               newTime = time + 8
                
                if newTime < times.get((newX, newY, newTool), float('inf')): 
                    times[(newX, newY, newTool)] = newTime
                    heapq.heappush(states, (newTime, newX, newY, newTool))

def PrintTimeMap(times):
    maxX = max([val[0] for val in times.keys()])
    maxY = max([val[1] for val in times.keys()])
    for y in range(maxY + 1):
        line = ''
        for x in range(maxX + 1): 
            if (x, y, 1) in times.keys(): line +=  str(times[(x, y, 1)]).ljust(5)
            else: line +=  str(-1).ljust(5)
        line += '     ' + str(y)
        print (line)
    
    line = ''
    for x in range(maxX + 1): 
        line += str(x).ljust(5)
    print (line)

def PrintMap(regionType):
    maxX = max([val[0] for val in regionType.keys()])
    maxY = max([val[1] for val in regionType.keys()])
    for y in range(maxY + 1):
        line = ''
        for x in range(maxX + 1):
            if [x, y] == [0, 0]: line += 'M'
            elif [x, y] == [tX, tY]: line += 'T'
            elif (x, y) not in regionType.keys(): line += 'x'
            elif regionType[(x, y)] == 0: line += '.'
            elif regionType[(x, y)] == 1: line += '='
            elif regionType[(x, y)] == 2: line += '|'
        print (line)
        
geoIndex, eroLevel, regionType = BuildMap(None, None, None, depth, 
                                          tX, tY)

# PrintMap(regionType)
print(TotalRisk(regionType, tX, tY, depth))

times = ShortestPath(geoIndex, eroLevel, regionType, tX, tY)
# PrintTimeMap(times)
print (times[ (tX, tY, 1) ])

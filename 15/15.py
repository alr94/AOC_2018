from collections import deque
################################################################################
# Classes for units

class Unit:
    def __init__(self, location):
        
        self.Location         = location
        self.Directions       = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        self.Alive            = True
        self.HP               = 200
        self.AP               = 3

        self.Targets          = []
        self.OpenSquares      = []
        self.ReachableSquares = []
        self.NearestSquares   = []
        self.ChosenSquare     = None
        
        self.BestSteps = []
        
        self.Distances        = {}

        self.Type             = ''

    def IdentifyTargets(self, units):
        
        self.Targets = []
        
        for unit in units: 
            if unit.Alive and unit.Type != self.Type: self.Targets.append(unit)
    
    def NextToEnemy(self, units):
        for unit in units: 
            
            if unit.Alive and unit.Type != self.Type: 
                
                for direction in self.Directions:
                    tileCoord  = self.Location[0] + direction[0]
                    lineCoord  = self.Location[1] + direction[1]
                    coord = [tileCoord, lineCoord]
                    
                    if unit.Location == coord: return True
                    
        return False
        
                
    
    def IdentifyOpenSquares(self, cavernMap, units):
        
        self.OpenSquares = []
        
        for target in self.Targets:
            
            for direction in self.Directions:
                
                tileCoord  = target.Location[0] + direction[0]
                lineCoord  = target.Location[1] + direction[1]
                coord = [tileCoord, lineCoord]
                
                if cavernMap[lineCoord][tileCoord] == '.':
                    
                    if not any(unit.Location == coord for unit in units if
                            unit.Alive):
                            self.OpenSquares.append(coord)
                            
    # Use DFS
    def IdentifyReachableSquares(self, cavernMap, units):
        
        self.ReachableSquares = []
        
        currentLocation = self.Location
        
        availableLocations = []
        for direction in self.Directions:
            
            tileCoord  = currentLocation[0] + direction[0]
            lineCoord  = currentLocation[1] + direction[1]
            coord      = [tileCoord, lineCoord]
            
            if cavernMap[lineCoord][tileCoord] == '.':
                if not any(unit.Location == coord for unit in units 
                           if unit.Alive):
                    availableLocations.append(coord)
                        
        while len(availableLocations) > 0:
            
            if currentLocation == None: continue
            
            for direction in self.Directions:
                
                tileCoord  = currentLocation[0] + direction[0]
                lineCoord  = currentLocation[1] + direction[1]
                coord      = [tileCoord, lineCoord]
                
                if cavernMap[lineCoord][tileCoord] == '.':
                    if not any(unit.Location == coord for 
                               unit in units if unit.Alive):
                        availableLocations.append(coord)
                            
            newLocation = availableLocations.pop()
            while (newLocation in self.ReachableSquares and 
                   len(availableLocations) > 0):
                newLocation = availableLocations.pop()
                
            if newLocation not in self.ReachableSquares:  
                currentLocation = newLocation
                self.ReachableSquares.append(currentLocation)
    
    # Use Dijkstra's algorithm
    def FindShortestPaths(self, cavernMap, units):
        
        squares = [self.Location]
        for square in self.ReachableSquares: squares.append(square)
        
        self.Distances = {}
        self.Distances[SquareAsInt(self.Location)] = 0
        for square in self.ReachableSquares:
            self.Distances[SquareAsInt(square)] = float('inf')
        
        currentSquare = None
        while len(squares) > 0:
            
            squares.sort(key=lambda square:-self.Distances[SquareAsInt(square)])
            currentSquare = squares.pop()
            
            for direction in self.Directions:
                
                tileCoord  = currentSquare[0] + direction[0]
                lineCoord  = currentSquare[1] + direction[1]
                coord = [tileCoord, lineCoord]
                
                if cavernMap[lineCoord][tileCoord] == '.':
                    
                        if not any(unit.Location == coord for unit in units if
                                unit.Alive):
                            
                            if coord in squares:
                                
                                dist = int(self.Distances[SquareAsInt(
                                                           currentSquare)] + 1)
                                
                                if dist < self.Distances[SquareAsInt(coord)]:
                                    self.Distances[SquareAsInt(coord)] = dist
    
    def IdentifyNearestSquares(self, cavernMap, units):
        
        self.FindShortestPaths(cavernMap, units)
        
        self.NearestSquares = []
        
        distArray = [ self.Distances[squareAsInt] for squareAsInt in 
                        self.Distances.keys() if IntToSquare(squareAsInt) in
                        self.ReachableSquares if IntToSquare(squareAsInt) in 
                        self.OpenSquares ]
        
        if len(distArray) == 0: return
        
        minDist = min(distArray)
        
        for squareAsInt in self.Distances.keys():
            
            if (IntToSquare(squareAsInt) in self.ReachableSquares and 
                IntToSquare(squareAsInt) in self.OpenSquares):
            
                dist = self.Distances[squareAsInt]
                
                if dist == minDist and dist != 0: 
                    self.NearestSquares.append(IntToSquare(squareAsInt))
                    
    def IdentifyChosenSquare(self):
        
        if len(self.NearestSquares) == 0:
            self.ChosenSquare = None
            return
        
        SortLocations(self.NearestSquares)
        self.ChosenSquare = self.NearestSquares[0]
    
    # DFS from aim along paths of least distance
    def FindShortestSteps(self):
        
        self.BestSteps = []
        
        currentSquare = self.ChosenSquare
        
        minDist = None
        for direction in self.Directions:
            
            tileCoord  = currentSquare[0] + direction[0]
            lineCoord  = currentSquare[1] + direction[1]
            coord      = [tileCoord, lineCoord]
            
            if coord == self.Location: 
                self.BestSteps.append(currentSquare)
                return
            
            if coord in self.ReachableSquares:
                dist = self.Distances[SquareAsInt(coord)]
                if minDist == None: minDist = dist
                elif dist < minDist : minDist = dist
        
        locationsVisited = []
        availableSquares = []
        for direction in self.Directions:
            
            tileCoord  = currentSquare[0] + direction[0]
            lineCoord  = currentSquare[1] + direction[1]
            coord      = [tileCoord, lineCoord]
            
            if coord in self.ReachableSquares:
                dist = self.Distances[SquareAsInt(coord)]
                if dist == minDist: availableSquares.append(coord)
        
        while len(availableSquares) > 0:
            
            currentSquare = availableSquares.pop()
            while (currentSquare in locationsVisited and 
                   len(availableSquares) > 0):
                currentSquare = availableSquares.pop()
                
            if currentSquare in locationsVisited: return
            
            locationsVisited.append(currentSquare)
            
            for direction in self.Directions:
                tileCoord  = currentSquare[0] + direction[0]
                lineCoord  = currentSquare[1] + direction[1]
                coord      = [tileCoord, lineCoord]
                if coord == self.Location: self.BestSteps.append(currentSquare)
                if coord in self.ReachableSquares:
                    dist = self.Distances[SquareAsInt(coord)]
                    if minDist == None: minDist = dist
                    elif dist < minDist : minDist = dist
        
            for direction in self.Directions:
                tileCoord  = currentSquare[0] + direction[0]
                lineCoord  = currentSquare[1] + direction[1]
                coord      = [tileCoord, lineCoord]
                if coord in self.ReachableSquares:
                    dist = self.Distances[SquareAsInt(coord)]
                    if dist == minDist: availableSquares.append(coord)
            
        SortLocations(self.BestSteps)
    
    def Move(self):
        
        if self.ChosenSquare == None: return
        
        self.FindShortestSteps()
        
        if len(self.BestSteps) > 0: self.Location = self.BestSteps[0]
    
    def SelectAttackTarget(self):
        
        adjacentTargets = []
        
        for target in self.Targets:
            for direction in self.Directions:
            
                tileCoord  = self.Location[0] + direction[0]
                lineCoord  = self.Location[1] + direction[1]
                coord = [tileCoord, lineCoord]
            
                if target.Location == coord: adjacentTargets.append(target)
        
        
        SortUnitsHP(adjacentTargets)
        if len(adjacentTargets) == 0: self.AttackTarget = None
        else: self.AttackTarget = adjacentTargets[0]
    
    def Attack(self):
        
        if self.AttackTarget != None: 
            self.AttackTarget.HP -= self.AP
            if self.AttackTarget.HP <= 0: self.AttackTarget.Alive = False
        
        
class Goblin(Unit):
    def __init__(self, location):
        Unit.__init__(self, location)
        self.Type = 'goblin'
        
class Elf(Unit):
    def __init__(self, location):
        Unit.__init__(self, location)
        self.Type = 'elf'
        
################################################################################
# Print functions        

def PrintMap(cavernMap):
    for lineCoord, line in enumerate(cavernMap):
        for tileCoord, tile in enumerate(line):
            print (tile, end='')
        print()


def PrintMapAndUnits(cavernMap, units):

    for x in range(len(inputLines[0])):
        if x / 10 < 1: print (x, end=' ')
        else: print (x, end='')
    
    print()
        
    for lineIndex, line in enumerate(cavernMap):
        for tileIndex, tile in enumerate(line):
            
            hasUnit = False
            for unit in units:
                if unit.Location == [tileIndex, lineIndex] and unit.Alive:
                    hasUnit = True
                    if unit.Type == 'goblin': print ('G', end=' ')
                    elif unit.Type == 'elf':  print ('E', end=' ')
                
            
            if not hasUnit: print (tile, end=' ')
        print (lineIndex)
        
def PrintTargets(unit, cavernMap):
    
    for x in range(len(inputLines[0])):
        if x / 10 < 1: print (x, end=' ')
        else: print (x, end='')
    
    print()

    for lineIndex, line in enumerate(cavernMap):
        for tileIndex, tile in enumerate(line):
            
            hasUnit = False
                
            if unit.Location == [tileIndex, lineIndex]:
                
                hasUnit = True
                if unit.Type == 'goblin': print ('G', end='')
                elif unit.Type == 'elf':  print ('E', end='')
            
            for target in unit.Targets:
                
                if target.Location == [tileIndex, lineIndex]:
                    hasUnit = True
                    if target.Type == 'goblin': print ('G', end='')
                    elif target.Type == 'elf':  print ('E', end='')
            
            if not hasUnit: print (tile, end='')
            
        print (lineIndex)

def PrintOpenSquares(unit, cavernMap):
    
    for x in range(len(inputLines[0])):
        if x / 10 < 1: print (x, end=' ')
        else: print (x, end='')
    
    print()

    for lineIndex, line in enumerate(cavernMap):
        for tileIndex, tile in enumerate(line):
            
            hasUnit = False
                
            if unit.Location == [tileIndex, lineIndex]:
                
                hasUnit = True
                if unit.Type == 'goblin': print ('G', end='')
                elif unit.Type == 'elf':  print ('E', end='')
            
            for target in unit.Targets:
                
                if target.Location == [tileIndex, lineIndex]:
                    hasUnit = True
                    if target.Type == 'goblin': print ('G', end='')
                    elif target.Type == 'elf':  print ('E', end='')
                    
            for location in unit.OpenSquares:
                if location == [tileIndex, lineIndex]:
                    hasUnit = True
                    print ('?', end='')
            
            if not hasUnit: print (tile, end='')
            
        print (lineIndex)

def PrintReachableSquares(unit, cavernMap):
    
    for x in range(len(inputLines[0])):
        if x / 10 < 1: print (x, end=' ')
        else: print (x, end='')
    
    print()

    for lineIndex, line in enumerate(cavernMap):
        for tileIndex, tile in enumerate(line):
            
            hasUnit = False
                
            if unit.Location == [tileIndex, lineIndex]:
                
                hasUnit = True
                if unit.Type == 'goblin': print ('G', end='')
                elif unit.Type == 'elf':  print ('E', end='')
            
            for target in unit.Targets:
                
                if target.Location == [tileIndex, lineIndex]:
                    hasUnit = True
                    if target.Type == 'goblin': print ('G', end='')
                    elif target.Type == 'elf':  print ('E', end='')
                    
            for location in unit.ReachableSquares:
                
                if location == [tileIndex, lineIndex]:
                #if location in unit.OpenSquares:
                        hasUnit = True
                        print ('@', end='')
            
            if not hasUnit: print (tile, end='')
            
        print (lineIndex)

def PrintNearestSquares(unit, units, cavernMap):
    
    for x in range(len(inputLines[0])):
        if x / 10 < 1: print (x, end=' ')
        else: print (x, end='')
    
    print()

    for lineIndex, line in enumerate(cavernMap):
        for tileIndex, tile in enumerate(line):
            
            hasUnit = False
                
            if unit.Location == [tileIndex, lineIndex]:
                
                hasUnit = True
                if unit.Type == 'goblin': print ('G', end='')
                elif unit.Type == 'elf':  print ('E', end='')
            
            if hasUnit == False:
                for target in unit.Targets:
                    
                    if target.Location == [tileIndex, lineIndex]:
                        hasUnit = True
                        if target.Type == 'goblin': print ('G', end='')
                        elif target.Type == 'elf':  print ('E', end='')
            
            if hasUnit == False:
                for location in unit.NearestSquares:
                    if location == [tileIndex, lineIndex]:
                        hasUnit = True
                        print ('!', end='')
                        
            if hasUnit == False:
                for unit2 in units:
                    if unit2.Location == [tileIndex, lineIndex]:
                        hasUnit = True
                        if unit2.Type == 'goblin': print ('g', end='')
                        elif unit2.Type == 'elf':  print ('e', end='')
                    
            
            if not hasUnit: print (tile, end='')
            
        print (lineIndex)

def PrintChosenSquare(unit, cavernMap):
    
    for x in range(len(inputLines[0])):
        if x / 10 < 1: print (x, end=' ')
        else: print (x, end='')
    
    print()

    for lineIndex, line in enumerate(cavernMap):
        for tileIndex, tile in enumerate(line):
            
            hasUnit = False
                
            if unit.Location == [tileIndex, lineIndex]:
                
                hasUnit = True
                if unit.Type == 'goblin': print ('G', end='')
                elif unit.Type == 'elf':  print ('E', end='')
            
            for target in unit.Targets:
                
                if target.Location == [tileIndex, lineIndex]:
                    hasUnit = True
                    if target.Type == 'goblin': print ('G', end='')
                    elif target.Type == 'elf':  print ('E', end='')
            
            if unit.ChosenSquare == [tileIndex, lineIndex]:
                hasUnit = True
                print ('+', end='')
            
            if not hasUnit: print (tile, end='')
            
        print (lineIndex)
        
################################################################################
# Initial build funtions

def BuildMapAndUnits(inputLines):
    
    cavernMap = [[None for tile in line] for line in inputLines]
    
    units = []
    
    for lineIndex, line in enumerate(inputLines):
        for tileIndex, tile in enumerate(line):
            
            if tile == 'G': 
                units.append(Goblin([tileIndex, lineIndex]))
                cavernMap[lineIndex][tileIndex] = '.'
                
            elif tile == 'E': 
                units.append(Elf([tileIndex, lineIndex]))
                cavernMap[lineIndex][tileIndex] = '.'
            
            else:
                cavernMap[lineIndex][tileIndex] = tile
        
    return cavernMap, units
    
################################################################################
# General utils
def SortUnits(units):
    units.sort(key = lambda unit: (unit.Location[1], unit.Location[0]))

def SortUnitsHP(units):
    units.sort(key = lambda unit: (unit.HP, unit.Location[1], unit.Location[0]))

def SortLocations(locations):
    locations.sort(key = lambda coord: (coord[1], coord[0]))

def SquareAsInt(square):
    return square[0] + len(cavernMap) * square[1]

def IntToSquare(squareAsInt):
    tileCoord = squareAsInt % len(cavernMap)
    lineCoord = int((squareAsInt - tileCoord) / len(cavernMap))
    return [tileCoord, lineCoord]

def NumberAlive(units, unitType):
    n = 0
    for unit in units:
        if unit.Type == unitType and unit.Alive == True: n += 1
    return n

################################################################################
# Run battle

for i in range(1):
    
    inputLines = [line.rstrip("\n") for line in open("input"+str(i)+".txt")]
    
    cavernMap, units = BuildMapAndUnits(inputLines)
    
    numberGoblins = NumberAlive(units, 'goblin')
    numberElves   = NumberAlive(units, 'elf')
    
    numberRounds = 0
    while numberGoblins > 0 and numberElves > 0:
        
        numberGoblins = NumberAlive(units, 'goblin')
        numberElves   = NumberAlive(units, 'elf')
        
        units = [ unit for unit in units if unit.Alive ]
        
        SortUnits(units)
        
        for index, unit in enumerate(units):
            
            largestUsedIndex = index
            
            if not unit.Alive: continue
            
            unit.IdentifyTargets(units)
            unit.IdentifyOpenSquares(cavernMap, units)
            unit.IdentifyReachableSquares(cavernMap, units)
            unit.IdentifyNearestSquares(cavernMap, units)
            unit.IdentifyChosenSquare()
            
            if not unit.NextToEnemy(units): 
                unit.Move()
                
            unit.SelectAttackTarget()
            unit.Attack()
        
        PrintMapAndUnits(cavernMap, units)
            
        numberRounds += 1
    
    units = [ unit for unit in units if unit.Alive ]
    
    remainingHealth = sum(unit.HP for unit in units if unit.Alive)
            
    print (numberRounds - 1, remainingHealth, (numberRounds - 1) * remainingHealth)

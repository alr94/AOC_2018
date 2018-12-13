patchesAsText = [ line.rstrip("\n")  for line in open("input.txt") ]

patchIds = []
patchXRanges, patchYRanges = [], []
for patchString in patchesAsText:
    patchIds.append(patchString.split(' ')[0][1:])
    
    xLow  = int(patchString.split(' ')[2].split(',')[0])
    xRange = int(patchString.split(' ')[3].split('x')[0])
    patchXRanges.append([xLow, xLow + xRange])
    
    yLow  = int(patchString.split(' ')[2].split(',')[1].split(':')[0])
    yRange = int(patchString.split(' ')[3].split('x')[1])
    patchYRanges.append([yLow, yLow + yRange])

def NumberDoubleClaims(patchXRanges, patchYRanges, patchIds):
    
    claimedSquares = {}
    numberDoubleClaimed = 0
    
    for patchIndex in range(len(patchIds)):
        
        xLow, xHigh = patchXRanges[patchIndex]
        yLow, yHigh = patchYRanges[patchIndex]
        
        for x in range(xLow, xHigh):
            for y in range(yLow, yHigh):
                locationIndex = x + 1000 * y
                if locationIndex in claimedSquares:
                    claimedSquares[locationIndex] += 1
                    if claimedSquares[locationIndex] == 2:
                        numberDoubleClaimed += 1
                else:
                    claimedSquares[locationIndex] = 1
    return numberDoubleClaimed

def NoneOverlapping(patchXRanges, patchYRanges, patchIds):
    
    claimedSquares = {}
    
    for patchIndex in range(len(patchIds)):
        
        xLow, xHigh = patchXRanges[patchIndex]
        yLow, yHigh = patchYRanges[patchIndex]
        
        for x in range(xLow, xHigh):
            for y in range(yLow, yHigh):
                locationIndex = x + 1000 * y
                if locationIndex in claimedSquares:
                    claimedSquares[locationIndex] += 1
                else:
                    claimedSquares[locationIndex] = 1
                    
    for patchIndex in range(len(patchIds)):
        
        xLow, xHigh = patchXRanges[patchIndex]
        yLow, yHigh = patchYRanges[patchIndex]
        
        numberOverlaps = 0
        for x in range(xLow, xHigh):
            for y in range(yLow, yHigh):
                locationIndex = x + 1000 * y
                if claimedSquares[locationIndex] > 1:
                    numberOverlaps += 1
                
        if numberOverlaps == 0:
            return patchIds[patchIndex]
                    
    return -1
                
print (NumberDoubleClaims(patchXRanges, patchYRanges, patchIds))
print (NoneOverlapping(patchXRanges, patchYRanges, patchIds))

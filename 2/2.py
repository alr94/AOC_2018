def Checksum(boxids):
    numberDoubles = 0
    numberTriples = 0
    for boxid in boxids:
        
        letterCounts = {}
        for letter in boxid:
            if letter in letterCounts:
                letterCounts[letter] += 1
            else:
                letterCounts[letter] = 1
                
        hasDouble, hasTriple = False, False
        for key in iter(letterCounts):
            if letterCounts[key] == 2:
                hasDouble = True
            if letterCounts[key] == 3:
                hasTriple = True
                
        if hasDouble:
            numberDoubles += 1
        if hasTriple:
            numberTriples += 1
            
    return numberDoubles * numberTriples

def FindCloseBoxIds(boxids):
    for boxid1 in boxids:
        for boxid2 in boxids:
            
            if boxid2 == boxid1:
                break
            
            nDiffs, diffIndex = 0, 0
            for index in range(len(boxid1)):
                if  boxid1[index] != boxid2[index]:
                    nDiffs += 1
                    diffIndex = index
                    if nDiffs > 1:
                        break
            if nDiffs == 1:
                return boxid1[0:diffIndex] + boxid1[diffIndex + 1:]
    
boxids = [ line.rstrip("\n")  for line in open("input.txt") ]

print( Checksum(boxids) )
print( FindCloseBoxIds(boxids) )

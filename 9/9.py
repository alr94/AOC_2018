# This was ok for the first part but much too slow for the second due to the
# O(n) insert operations
def SolveSlow(numberPlayers, lastMarble):
    
    playerScores = [0 for _ in range(numberPlayers)]
    marbleCircle = [0]

    currentMarble, currentPlayer = 0, 0
    currentMarbleIndex = 0

    while currentMarble < lastMarble:
        
        nextMarble = currentMarble + 1
        
        if nextMarble % 23 != 0:
            
            nextIndex = currentMarbleIndex + 2
            
            if nextIndex > len(marbleCircle):
                nextIndex =  nextIndex - len(marbleCircle)
                
            marbleCircle.insert(nextIndex, nextMarble)
            currentMarbleIndex = nextIndex
            
        else: 
            
            playerScores[currentPlayer] += nextMarble
            
            removalIndex = currentMarbleIndex - 7
            if removalIndex < 0:
                removalIndex = len(marbleCircle) + removalIndex
                
            playerScores[currentPlayer] += marbleCircle[removalIndex]
            
            del marbleCircle[removalIndex]
            
            currentMarbleIndex = removalIndex
            if currentMarbleIndex > len(marbleCircle) - 1:
                currentMarbleIndex = 0
            
        currentMarble = nextMarble
        currentPlayer = (currentPlayer + 1) % numberPlayers

    print (max(playerScores))


# Faster implementation based on deque and rotations
# Credit to /u/marcusandrews on the subreddit for the inspiration
from collections import deque
def SolveFast(numberPlayers, lastMarble):
    
    playerScores = [0 for _ in range(numberPlayers)]
    marbleCircle = deque([0])
    
    currentMarble, currentPlayer = 0, 0
    currentMarbleIndex = 0

    while currentMarble < lastMarble:
        
        nextMarble = currentMarble + 1
        
        if nextMarble % 23 == 0:
            marbleCircle.rotate(7)
            playerScores[currentPlayer] += nextMarble + marbleCircle.pop()
            marbleCircle.rotate(-1)
        else:
            marbleCircle.rotate(-1)
            marbleCircle.append(nextMarble)
            
        currentMarble = nextMarble
        currentPlayer = (currentPlayer + 1) % numberPlayers
    
    print (max(playerScores))
        
inputLines = [ line.rstrip("\n").split() for line in open("input.txt") ][0]
numberPlayers, lastMarble = int(inputLines[0]), int(inputLines[6])

SolveFast(numberPlayers, lastMarble)
SolveFast(numberPlayers, 100 * lastMarble)

def PrintBoard(scores, chefLocations):
    for index in range(len(scores)):
        if index in chefLocations:
            if chefLocations[0] == index:
                print ('(', end='')
                print(scores[index], end='')
                print(')', end='')
            else:
                print ('[', end='')
                print(scores[index], end='')
                print(']', end='')
        else:
            print (' ', end='')
            print (scores[index], end=' ')
            
    print()

def ScoresAfterImprovement (scores, chefLocations, numberRecipes):
    
    while len(scores) < numberRecipes + 10:
        
        sumOfCurrent = 0
        for location in chefLocations:
            sumOfCurrent += scores[location]
        
        for digit in str(sumOfCurrent):
            scores.append(int(digit))
        
        for index, location in enumerate(chefLocations):
            newLocation = location + scores[location] + 1
            while newLocation >= len(scores):
                newLocation -= len(scores)
            chefLocations[index] = newLocation
            
        # PrintBoard(scores, chefLocations)

    for score in scores[numberRecipes:numberRecipes + 10]: print (score, end='')
    print()
    
def LeftOfScore(scores, chefLocations, scoreGoal):
    
    lenScoreGoal = len(scoreGoal)
    scoreGoalAsIntArray = []
    for score in scoreGoal: scoreGoalAsIntArray.append(int(score))
    
    while True:
        
        sumOfCurrent = 0
        for location in chefLocations:
            sumOfCurrent += scores[location]
        
        for digit in str(sumOfCurrent):
            scores.append(int(digit))
            
        # Max summed score is 18 so only need to check two possibilities
        if scores[- lenScoreGoal:] == scoreGoalAsIntArray:
            print (len(scores) - lenScoreGoal)
            break
        if scores[- lenScoreGoal - 1: -1] == scoreGoalAsIntArray:
            print (len(scores) - lenScoreGoal - 1)
            break
        
        for index, location in enumerate(chefLocations):
            newLocation = location + scores[location] + 1
            while newLocation >= len(scores):
                newLocation -= len(scores)
            chefLocations[index] = newLocation
            

scores        = [3, 7]
chefLocations = [0, 1]
numberRecipes = 147061
ScoresAfterImprovement(scores, chefLocations, numberRecipes)

scores        = [3, 7]
chefLocations = [0, 1]
scoreGoal     = '147061'
LeftOfScore(scores, chefLocations, scoreGoal)

from collections import defaultdict

# This initial attempt is inefficient due to the bracket matching which could be 
# done on the go which adds an O(n) factor to the running time
#
# def LongestPath(directions):
#     
#     numberSteps = 0
#     
#     index = 0
#     while index < len(directions): 
#         
#         if directions[index] == '(': 
#             subDirections = MatchBracket(directions[index:])
#             numberSteps += LongestPath(subDirections)
#             index += len(subDirections) + 1
#             continue
#         
#         elif directions[index] == '|': 
#             alternateDirections = directions[index + 1:]
#             if min(numberSteps, LongestPath(alternateDirections)) == 0:
#                 numberSteps = 0
#             else:
#                 numberSteps = max(numberSteps, LongestPath(alternateDirections))
#             break
#             
#         elif directions[index] != ')': numberSteps += 1
#         index += 1
#             
#     
#     return numberSteps
# 
# def MatchBracket(string):
#     
#     counter = 0
#     
#     start, end = None, None
#     for i in range(len(string)):
#         if string[i] == '(': 
#             if counter == 0: start = i
#             counter += 1
#         if string[i] == ')':
#             counter -= 1
#             if counter == 0: 
#                 end = i
#                 break
#             
#     if start != None and end != None: return string[start + 1:end]
#     else: return ''

# Keeping a stack of offshoot locations acts as the "Bracket matching" I did 
# in my first attempt. Then I can just keep track of my location and update 
# shortest paths to each location
def ShortestPaths(directions):
    
    unitVectors = {'N': [0, 1], 'E': [1, 0], 'S': [0, -1], 'W': [-1, 0]}
    
    splitPoints = []
    distances   = defaultdict(int)
    distance    = 0
    
    x, y = 0, 0
    prev_x, prev_y = x, y
    
    for character in directions:
        
        # Entering a loop where I explore ofshoots from current location
        if character == '(': splitPoints.append((x, y))
        
        # I have explored all offshoots and can carry on along the main path
        elif character == ')': x, y = splitPoints.pop()
        
        # Offshoot of the most recent split point
        elif character == '|': x, y = splitPoints[-1]
        
        # Normal movement
        else:
            
            direction = unitVectors[character]
            x += direction[0]
            y += direction[1]
            
            # I have been here before, I need the shortest path to here
            if distances[(x, y)] != 0:
                distances[(x, y)] = min(distances[(x, y)], 
                                        distances[(prev_x, prev_y)] + 1)
                
            # I haven't been here before
            else: distances[(x, y)] = distances[(prev_x, prev_y)] + 1
        
        prev_x, prev_y = x, y
    
    return distances

################################################################################
# Run program
startDirections = [line.rstrip("\n") for line in open("testInput1.txt")][0][1:-1]
startDirections = [line.rstrip("\n") for line in open("input.txt")][0][1:-1]

distances = ShortestPaths(startDirections)
print (max(distances.values()))
print (len([distance for distance in distances.values() if distance >= 1000]))

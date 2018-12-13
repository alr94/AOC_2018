inputLines = [ line.rstrip("\n") for line in open("testInput.txt") ]
inputLines = [ line.rstrip("\n") for line in open("input.txt") ]

configurationString = inputLines[0].split(':')[1].split(' ')[1]
configuration = [x == '#' for x in configurationString]
zeroIndex = 0

rules = []
for line in inputLines:
    if '=>' in line:
        ruleString = line.split('=>')[0].split(' ')[0]
        ruleString += line.split('=>')[1].split(' ')[1]
        rules.append([x=='#' for x in ruleString])

def PrintConfig(configuration):
    for value in configuration:
        if value: print ('#', end='')
        else: print ('.', end='')
    print()
    
        
def NextGeneration(configuration, zeroIndex, rules):
    
    newConfiguration = [False for _ in range(len(configuration))]
    
    numberAddedAtStart = 0
    
    for index in range(-3, len(configuration) + 3):
        
        thisConfig = configuration[index -2:index + 3]
        if len(thisConfig) != 5:
            if (index < 2): 
                thisConfig = configuration[:index + 3]
                for i in range(5 - len(thisConfig)): 
                    thisConfig.insert(0, False)
            else:
                for i in range(5 - len(thisConfig)): 
                    thisConfig.append(False)
        
        for rule in rules:
            
            if thisConfig == rule[:5]:
                
                if index < 0:
                    if numberAddedAtStart > -index:
                        newConfiguration[numberAddedAtStart + index] = rule[-1]
                    else:
                        for _ in range(-index - 1):
                            newConfiguration.insert(0, False)
                            numberAddedAtStart += 1
                        newConfiguration.insert(0, rule[-1])
                        numberAddedAtStart += 1
                    
                elif index >= len(configuration):
                    for _ in range(index - len(configuration) -
                            numberAddedAtStart - 1):
                        newConfiguration.append(False)
                    newConfiguration.append(rule[-1])
                    
                else: 
                    newConfiguration[index + numberAddedAtStart] = rule[-1]
                    
                break
                    
            elif index > 0 and index < len(configuration):
                newConfiguration[index + numberAddedAtStart] = False
                
    return (newConfiguration, zeroIndex + numberAddedAtStart)
    
prevSum   = None
prevDiff  = None
for i in range(50000000000):
    
    configuration, zeroIndex = NextGeneration(configuration, zeroIndex,  rules)
    
    sum = 0
    for index in range(len(configuration)):
        if configuration[index]: sum += index - zeroIndex
        
    diff = None
    if prevSum != None: diff = (sum - prevSum) 
    if diff != None and diff == prevDiff:
        print (sum + (50000000000 - i - 1) * diff)
        break
        
    prevSum  = sum
    prevDiff = diff

def OrderToComplete(requirements, ordering, unfinishedSteps):
    
    unavailableSteps = [requirement[1] for requirement in requirements]
    
    if len(unfinishedSteps) == 0: return ordering
    
    nextStep = sorted([step for step in unfinishedSteps if step not in
                       unavailableSteps])[0]
    
    ordering += nextStep
    unfinishedSteps.remove(nextStep)
    
    newRequirements = [requirement for requirement in requirements if 
                       requirement[0] != nextStep]
    
    return OrderToComplete(newRequirements, ordering, unfinishedSteps) 

def TimeToComplete(requirements, numberWorkers):
    
    unfinishedSteps = set()
    for requirement in requirements:
        unfinishedSteps.add(requirement[0])
        unfinishedSteps.add(requirement[1])
    
    workers = {id: None for id in range(numberWorkers)}
    workerTimes = [0]  * numberWorkers
    workerSteps = [''] * numberWorkers
    
    time = 0
    
    while len(unfinishedSteps) != 0:
        
        # check for finished workers
        for index in range(len(workerTimes)):
            
            if workerTimes[index] == time:
                if workerSteps[index] != '':
                    
                    unfinishedSteps.remove(workerSteps[index])
                    
                    requirements = [requirement for requirement in requirements 
                                    if requirement[0] != workerSteps[index]]
        
        # Find next available steps
        unavailableSteps =  [requirement[1] for requirement in requirements]
        
        nextSteps = sorted([step for step in unfinishedSteps if ((step not in
                            unavailableSteps) and (step not in workerSteps))])
        
        # Assign steps
        for step in nextSteps:
            for index in range(len(workerTimes)):
                if workerTimes[index] <= time:
                    workerTimes[index] = time + StepToTime(step)
                    workerSteps[index] = step
                    break
        
        time += 1
        
    return (time - 1)
    
def StepToTime(step):
    return (60 + ord(step.lower()) - 96)
    # return (ord(step.lower()) - 96)

################################################################################

inputLines = [ line.rstrip("\n")   for line in open("input.txt") ]

requirements = []
for line in inputLines:
    toDo = line.split(' ')[1]
    after = line.split(' ')[7]
    requirements.append([toDo, after])

    
ordering = ''

unfinishedSteps = set()
for requirement in requirements:
    unfinishedSteps.add(requirement[0])
    unfinishedSteps.add(requirement[1])
    
print(OrderToComplete(requirements, ordering, unfinishedSteps))
print(TimeToComplete(requirements, 5))

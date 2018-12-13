def OrderEvents(events):
    dateTimeNums = [None] * len(events)
    for index, event in enumerate(events):
        
        dateStrings = event.split("[")[1].split(" ")[0].split("-")
        timeStrings = event.split("]")[0].split(" ")[1].split(":")
        
        dateTimeNum = int(dateStrings[0] + dateStrings[1] + dateStrings[2] + 
                          timeStrings[0] + timeStrings[1])
        
        dateTimeNums[index] = dateTimeNum
        
    orderedEvents = [event for _, event in sorted(zip(dateTimeNums, events))]
    return orderedEvents

def GetSleepDetails(events):
    totalTimeAsleep = {}
    sleepShedule = {}
    
    currentGaurd = 0
    sleepStart = 0
    
    for event in events:
        
        if "Guard #" in event:
            currentGaurd = event.split("#")[1].split(" ")[0]
            if currentGaurd not in totalTimeAsleep:
                totalTimeAsleep[currentGaurd] = 0
            if currentGaurd not in sleepShedule:
                sleepShedule[currentGaurd] = [0] * 60
                
        if "falls asleep" in event:
            sleepStart = int(event.split(":")[1].split("]")[0])
            
        if "wakes up" in event:
            sleepEnd = int(event.split(":")[1].split("]")[0])
            
            if currentGaurd in totalTimeAsleep:
                totalTimeAsleep[currentGaurd] += sleepEnd - sleepStart
                
            if currentGaurd in totalTimeAsleep:
                for time in range(sleepStart, sleepEnd):
                    sleepShedule[currentGaurd][time] += 1 
    return totalTimeAsleep, sleepShedule

def MostTimeAsleep(totalTimeAsleep, sleepShedule):
    
    maxTime = 0
    sleepiestGaurd = 0
    for gaurdID in totalTimeAsleep.keys():
        
        if totalTimeAsleep[gaurdID] > maxTime:
            maxTime = totalTimeAsleep[gaurdID]
            sleepiestGaurd = gaurdID
    
    maxFreq = 0
    sleepiestTime = 0
    for time, frequency in enumerate(sleepShedule[sleepiestGaurd]):
        
        if frequency > maxFreq:
            maxFreq = frequency
            sleepiestTime = time
        
    return  int(sleepiestGaurd) * int(sleepiestTime)

def MostAsleepTime(totalTimeAsleep, sleepShedule):
    
    maxFreq = 0
    sleepiestTime = 0
    mostConsistentSleeper = 0
    
    for gaurdID in sleepShedule.keys():
        for time, frequency in enumerate(sleepShedule[gaurdID]):
            if frequency > maxFreq:
                maxFreq = frequency
                sleepiestTime = time
                mostConsistentSleeper = gaurdID
        
    return  int(mostConsistentSleeper) * int(sleepiestTime)
            
events = [ line.rstrip("\n")  for line in open("input.txt") ]
orderedEvents = OrderEvents(events)

totalTimeAsleep, sleepShedule = GetSleepDetails(orderedEvents)

print(MostTimeAsleep(totalTimeAsleep, sleepShedule))
print(MostAsleepTime(totalTimeAsleep, sleepShedule))

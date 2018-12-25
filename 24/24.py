class Army:
    def __init__(self, armyLines):
        self.Name   = armyLines[0][:-1]
        self.groups = []
        ID = 0
        for index in range(1, len(armyLines)):
            ID += 1
            self.groups.append(Group(self.Name, armyLines[index], ID))
        
class Group:
    def __init__(self, army, groupLines, ID):
        
        self.Army           = army
        
        self.ID             = army + ' ' + str(ID)
        
        self.NumberUnits    = int(groupLines.split()[0])
        
        self.Target         = None
        
        self.UnitHP         = int(groupLines.split()[4])
        
        self.UnitWeaknesses = []
        self.UnitImunities  = []
        
        if len(groupLines.split('(')) > 1 :
            
            weaknessLines = groupLines.split('(')[1].split(')')[0].split(';')
            
            for line in weaknessLines:
                
                if 'weak' in line:
                    for weakness in line.split('weak ')[1].split()[1:]:
                        weakness = weakness.replace(',', '')
                        if weakness != '': self.UnitWeaknesses.append(weakness)
                        
                elif 'immune' in line:
                    for weakness in line.split('immune ')[1].split()[1:]:
                        weakness = weakness.replace(',', '')
                        if weakness != '': self.UnitImunities.append(weakness)
                        
                    
            self.UnitAP         = int(groupLines.split(')')[1].split()[5])
            self.UnitAT         = groupLines.split(')')[1].split()[6]
            
        else:
            self.UnitAP         = int(groupLines.split()[12])
            self.UnitAT         = groupLines.split()[13]
        
        self.UnitInitiative = int(groupLines.split()[-1])
        
    def EP(self): return int(self.UnitAP * self.NumberUnits)
    
    def DamageTaken(self, EP, AT):
        if AT in self.UnitWeaknesses: return int(2 * EP)
        if AT in self.UnitImunities:  return int(0)
        return int(EP)
    
    def TakeDamage(self, EP, AT):
        damage = self.DamageTaken(EP, AT)
        unitsLost = min(self.NumberUnits, int(damage / self.UnitHP))
        self.NumberUnits -= unitsLost

def BuildArmies(inputLines):
    armies = []
    for index in range(len(inputLines)):
        
        if 'Immune System' in inputLines[index]: startLoc = index
        if 'Infection' in inputLines[index]:     startLoc = index
        
        if len(inputLines[index]) == 0: 
            armies.append(Army(inputLines[startLoc:index]))
        if index == len(inputLines) - 1:
            armies.append(Army(inputLines[startLoc:]))
            
    return armies

def Fight(armies):
    
    groups            = []
    
    for army in armies:
        for group in army.groups:
            if group.NumberUnits > 0: groups.append(group)
                
    TargetCollection(groups)
    Attack(groups)

def TargetCollection(groups):
    
    selected = set()
    
    groups.sort(key = lambda group: (- group.EP(), - group.UnitInitiative))
    
    for group in groups: 
        
        def orderKey(target):
            return (-target.DamageTaken(group.EP(), group.UnitAT), -target.EP(),
                    -target.UnitInitiative)
                    
        enemyGroups = sorted([eg for eg in groups 
                              if group.Army != eg.Army and eg.ID not in selected 
                              and eg.DamageTaken(group.EP(), group.UnitAT) > 0],
                              key = orderKey)
        
        if len(enemyGroups) > 0: 
            group.Target = enemyGroups[0]
            selected.add(enemyGroups[0].ID)

def Attack(groups):
    groups.sort(key = lambda group: (- group.UnitInitiative))
    for group in groups:
        if group.NumberUnits > 0 and group.Target != None:
            group.Target.TakeDamage(group.EP(), group.UnitAT)
        group.Target = None

def ArmySizes(armies):
    
    immuneArmySize    = 0
    infectionArmySize = 0
    
    for army in armies:
        for group in army.groups:
            if army.Name == 'Immune System': immuneArmySize += group.NumberUnits
            elif army.Name == 'Infection': infectionArmySize += group.NumberUnits
    
    return immuneArmySize, infectionArmySize
    
inputLines = [line.rstrip("\n") for line in open("testInput.txt")]
inputLines = [line.rstrip("\n") for line in open("input.txt")]

armies = BuildArmies(inputLines)
        
immuneArmySize, infectionArmySize = ArmySizes(armies)

while immuneArmySize > 0 and infectionArmySize > 0:
    Fight(armies)
    someDied = (ArmySizes(armies) != (immuneArmySize, infectionArmySize))
    if not someDied: break
    immuneArmySize, infectionArmySize = ArmySizes(armies)
print (immuneArmySize, infectionArmySize)
    
boost = 0
while True:
    
    boost += 1
    
    armies = BuildArmies(inputLines)
    for army in armies:
        if army.Name == 'Immune System':
            for group in army.groups:
                group.UnitAP += boost
                
    immuneArmySize, infectionArmySize = ArmySizes(armies)
    while immuneArmySize > 0 and infectionArmySize > 0:
        Fight(armies)
        someDied = (ArmySizes(armies) != (immuneArmySize, infectionArmySize))
        if not someDied: break
        immuneArmySize, infectionArmySize = ArmySizes(armies)
        
    if immuneArmySize > 0 and infectionArmySize == 0: 
        print (boost, immuneArmySize)
        break

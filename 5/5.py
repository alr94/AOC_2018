import string

def ContractPolymer(polymer, unitTypes):
    
    contractionTypes = []
    for unitType in unitTypes:
        contractionTypes.append(unitType + unitType.upper())
        contractionTypes.append(unitType.upper() + unitType)
    
    contractedPolymer = polymer
    
    didContract = True
    while didContract:
        
        didContract = False
        
        for contractionType in contractionTypes:
            if contractionType in contractedPolymer:
                contractedPolymer = contractedPolymer.replace(contractionType, "")
                didContract = True
        
    return contractedPolymer

def RemoveUnit(polymer, unit):
    return polymer.replace(unit, "").replace(unit.upper(), "")
    

polymer = [ line.rstrip("\n")  for line in open("input.txt") ][0]
unitTypes = list(string.ascii_lowercase)

contractedPolymer = ContractPolymer(polymer, unitTypes)
print (len(contractedPolymer))

lenWithoutUnit = {}
for unit in unitTypes:
    startPolymer = RemoveUnit(polymer, unit)
    contractedPolymer = ContractPolymer(startPolymer, unitTypes)
    lenWithoutUnit[unit] = len(contractedPolymer)
    
print (min(lenWithoutUnit.items(), key=lambda x: x[1]))

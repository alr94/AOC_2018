################################################################################
# Operations
def addr(reg, a, b, c): reg[c] = reg[a] + reg[b] 
def addi(reg, a, b, c): reg[c] = reg[a] + b

def mulr(reg, a, b, c): reg[c] = reg[a] * reg[b]
def muli(reg, a, b, c): reg[c] = reg[a] * b

def banr(reg, a, b, c): reg[c] = reg[a] & reg[b]
def bani(reg, a, b, c): reg[c] = reg[a] & b

def borr(reg, a, b, c): reg[c] = reg[a] | reg[b]
def bori(reg, a, b, c): reg[c] = reg[a] | b

def setr(reg, a, b, c): reg[c] = reg[a]
def seti(reg, a, b, c): reg[c] = a

def gtir(reg, a, b, c): reg[c] = 1 if a > reg[b] else 0
def gtri(reg, a, b, c): reg[c] = 1 if reg[a] > b else 0
def gtrr(reg, a, b, c): reg[c] = 1 if reg[a] > reg[b] else 0

def eqir(reg, a, b, c): reg[c] = 1 if a == reg[b] else 0
def eqri(reg, a, b, c): reg[c] = 1 if reg[a] == b else 0
def eqrr(reg, a, b, c): reg[c] = 1 if reg[a] == reg[b] else 0

availableOperations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, 
                       seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

################################################################################
# Operation calculations

def MatchingOps(before, instruction, after, availableOperations):
    
    opCode   = instruction[0]
    opInputs = instruction[1:]
    
    matchingOps = []
    for operation in availableOperations:
        reg = before.copy()
        operation(reg, *opInputs)
        if reg == after: matchingOps.append(operation)
        
    return matchingOps

def NumberMultiCodeInstructions(befores, instructions, afters, 
                                availableOperations):
    numberMultiCodeInstructions = 0
    for i in range(len(befores)):
        nMatching = len(MatchingOps(befores[i], instructions[i], afters[i], 
                                    availableOperations))
        if nMatching >= 3: numberMultiCodeInstructions += 1
    
    return numberMultiCodeInstructions

def AssignOpCodes(befores, instructions, afters, availableOperations):
    
    knownOperations = {}
    
    while len(knownOperations) < len(availableOperations):
        
        unusedOperations = [operation for operation in availableOperations if 
                            operation not in knownOperations.values()]
        
        minLen = None
        for i in range(len(instructions)):
            
            matchingOps = MatchingOps(befores[i], instructions[i], afters[i], 
                                      unusedOperations) 
            
            if minLen == None: minLen = len(matchingOps)
            if len(matchingOps) < minLen: minLen = len(matchingOps)
            
            if len(matchingOps) == 1:
                opCode = instructions[i][0] 
                knownOperations[opCode] = matchingOps[0]
                del befores[i]
                del instructions[i]
                del afters[i]
                break
    
    return knownOperations
    
        
################################################################################   
# Parsing

def BuildInstructions(inputLines):
    
    befores      = []
    instructions = []
    afters       = []
    
    for i in range(len(inputLines)):
        befores.append([int(x) for x in inputLines[i].split(':')[0].split()])
        instructions.append([int(x) for x in inputLines[i].split(':')[1].split()])
        afters.append([int(x) for x in inputLines[i].split(':')[2].split()])
    
    return befores, instructions, afters

def BuildProgram(inputLines):
    
    instructions = []
    for i in range(len(inputLines)):
        instructions.append([int(x) for x in inputLines[i].split()])
    
    return instructions 

################################################################################
# Run program
    
inputLines = [line.rstrip("\n") for line in open("inputPart1.txt")]
befores, instructions, afters = BuildInstructions(inputLines)

print (NumberMultiCodeInstructions(befores, instructions, afters, 
                                   availableOperations))

opCodes = AssignOpCodes(befores, instructions, afters, availableOperations)

inputLines = [line.rstrip("\n") for line in open("inputPart2.txt")]
instructions = BuildProgram(inputLines)

reg = [0, 0, 0, 0] 
for instruction in instructions:
    opCode   = instruction[0]
    opInputs = instruction[1:]
    
    operation = opCodes[opCode]
    
    operation(reg, *opInputs)
    
print (reg)


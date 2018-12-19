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

availableOperations = {'gtrr': gtrr, 'gtri': gtri, 'eqir': eqir, 'eqrr': eqrr, 
                       'eqri': eqri, 'gtir': gtir, 'setr': setr, 'bani': bani, 
                       'banr': banr, 'seti': seti, 'mulr': mulr, 'borr': borr, 
                       'addi': addi, 'addr': addr, 'bori': bori, 'muli': muli}

################################################################################
# Part 1
print ('Part 1')

inputLines = [line.rstrip("\n") for line in open("testInput.txt")]
inputLines = [line.rstrip("\n") for line in open("input.txt")]

ipReg = int(inputLines[0].split()[1])
del inputLines[0]

operationByIndex    = {}
instructionsByIndex = {}
for index, line in enumerate(inputLines):
    operationByIndex[index]    = line.split()[0]
    instructionsByIndex[index] = [int(x) for x in line.split()[-3:]]

registers    = [0 for _ in range(6)]
ip = registers[ipReg]

while True:
    
    registers[ipReg] = ip
    
    if ip < 0 or ip >= len(inputLines): break
    
    availableOperations[operationByIndex[ip]](registers, *instructionsByIndex[ip])
    
    ip = registers[ipReg] + 1

print (registers)

################################################################################
# Part 2
print ('Part 2')

registers    = [0 for _ in range(6)]
registers[0] = 1
ip = registers[ipReg]

regZeroValues = set()
while True:
    
    
    if registers[0] not in regZeroValues: 
        regZeroValues.add(registers[0])
        print(registers)
    
    registers[ipReg] = ip
    
    if ip < 0 or ip >= len(inputLines): break
    
    availableOperations[operationByIndex[ip]](registers, *instructionsByIndex[ip])
    
    ip = registers[ipReg] + 1

print (registers)

# This ran for a very long time so I assumed a reccurence
# Examining the operations there was an initial sequence
# (17) addi 5 2 5 [1, 0, 0, 0, 17, 0]
# (18) mulr 5 5 5 [1, 0, 0, 0, 18, 2]
# (19) mulr 4 5 5 [1, 0, 0, 0, 19, 4]
# (20) muli 5 11 5 [1, 0, 0, 0, 20, 76]
# (21) addi 1 4 1 [1, 0, 0, 0, 21, 836]
# (22) mulr 1 4 1 [1, 4, 0, 0, 22, 836]
# (23) addi 1 15 1 [1, 88, 0, 0, 23, 836]
# (24) addr 5 1 5 [1, 103, 0, 0, 24, 836]
# (25) addr 4 0 4 [1, 103, 0, 0, 25, 939]
# (27) setr 4 2 1 [1, 103, 0, 0, 27, 939]
# (28) mulr 1 4 1 [1, 27, 0, 0, 28, 939]
# (29) addr 4 1 1 [1, 756, 0, 0, 29, 939]
# (30) mulr 4 1 1 [1, 785, 0, 0, 30, 939]
# (31) muli 1 14 1 [1, 23550, 0, 0, 31, 939]
# (32) mulr 1 4 1 [1, 329700, 0, 0, 32, 939]
# (33) addr 5 1 5 [1, 10550400, 0, 0, 33, 939]
# (34) seti 0 8 0 [1, 10550400, 0, 0, 34, 10551339]
# (35) seti 0 4 4 [0, 10550400, 0, 0, 35, 10551339]
# (1) seti 1 3 3 [0, 10550400, 0, 0, 1, 10551339]
# (2) seti 1 4 2 [0, 10550400, 0, 1, 2, 10551339]
# (3) mulr 3 2 1 [0, 10550400, 1, 1, 3, 10551339]
# (4) eqrr 1 5 1 [0, 1, 1, 1, 4, 10551339]
# (5) addr 1 4 4 [0, 0, 1, 1, 5, 10551339]
# (6) addi 4 1 4 [0, 0, 1, 1, 6, 10551339]
# (8) addi 2 1 2 [0, 0, 1, 1, 8, 10551339]
# (9) gtrr 2 5 1 [0, 0, 2, 1, 9, 10551339]
# (10) addr 4 1 4 [0, 0, 2, 1, 10, 10551339]

# Followed by a repeating sequence
# (11) seti 2 2 4 [0, 0, 2, 1, 11, 10551339]
# (3) mulr 3 2 1 [0, 0, 2, 1, 3, 10551339]
# (4) eqrr 1 5 1 [0, 2, 2, 1, 4, 10551339]
# (5) addr 1 4 4 [0, 0, 2, 1, 5, 10551339]
# (6) addi 4 1 4 [0, 0, 2, 1, 6, 10551339]
# (8) addi 2 1 2 [0, 0, 2, 1, 8, 10551339]
# (9) gtrr 2 5 1 [0, 0, 3, 1, 9, 10551339]
# (10) addr 4 1 4 [0, 0, 3, 1, 10, 10551339]
# ...
# seti 2 2 4

# I kept track of the values of register 0 whenever it changed
# 0, 1, 4, 13, 30, 81, ...
# Which have differences
# 1, 3, 9, 17, 51, ...

# Which are prime factors of 10551339, or multiples of them
# primeFactors -> 3, 3, 17, 68963
# 1, 3, 3*3, 17, 3*17, ...

# So the answer is the sum of the products of combinations of these numbers
import itertools
primeFactors = [3, 3, 17, 68963]
sum = 1 
valuesFound = set()
valuesFound.add(1)
for x in range(1, len(primeFactors) + 1):
    for subset in itertools.combinations(primeFactors, x):
        product = 1
        for num in subset: product *= num
        if product not in valuesFound:
            print (product)
            valuesFound.add(product)
            sum += product

print (sum)
# ----> 16137576

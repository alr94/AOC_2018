from collections import defaultdict

inputLines = [line.rstrip("\n") for line in open("input.txt")]

class Nanobot:
    def __init__(self, location, strength):
        self.location = location
        self.strength = strength
    
    def Manhattan(self, loc):
        dist = 0
        for i in range(len(self.location)):
            dist += abs(self.location[i] - loc[i])
        return int(dist)

nanobots = []
for line in inputLines:
    location = [int(x) for x in line.split('<')[1].split('>')[0].split(',')]
    strength = int(line.split('r')[1].split('=')[1])
    nanobots.append(Nanobot(location, strength))

def NumberInRange(nanobots):
    
    nanobots.sort(key = lambda bot: - bot.strength)
    
    numberInRange = 0
    for bot in nanobots:
        if bot.Manhattan(nanobots[0].location) <= nanobots[0].strength: 
            numberInRange += 1
    
    return numberInRange

print (NumberInRange(nanobots))

# Never seen z3 before but after struggling for a long time on this problem I 
# saw a number of people using it on the subreddit so I am trying it out here
# based on the solution by /u/mserrano
import z3

def z3_abs(x): return z3.If(x >= 0, x, -x)

(x, y, z) = (z3.Int('x'), z3.Int('y'), z3.Int('z'))

ranges = [ z3.Int('range_' + str(i)) for i in range(len(nanobots)) ]
n_ranges = z3.Int('sum')

optimize = z3.Optimize()
for i in range(len(nanobots)):
    
    (bx, by, bz), strength = nanobots[i].location, nanobots[i].strength
    
    optimize.add(ranges[i] == z3.If(z3_abs(x - bx) + z3_abs(y - by) + 
                                    z3_abs(z - bz) <= strength, 1, 0))
    
optimize.add(n_ranges == sum(ranges))

dist = z3.Int('dist')

optimize.add(dist == z3_abs(x) + z3_abs(y) + z3_abs(z))

opt1 = optimize.maximize(n_ranges)
opt2 = optimize.minimize(dist)

optimize.check()

print (optimize.lower(opt1), optimize.upper(opt2))

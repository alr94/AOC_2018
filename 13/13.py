class Cart:
    def __init__(self, location, direction):
        self.location  = location
        self.direction = direction
        self.nextTurn  = 0
        self.alive     = True
        
    def Move(self):
        for index in range(len(self.location)):
            self.location[index] += self.direction[index]
        
    def Turn(self, track):
        
        (x, y) = self.direction
        
        if track == '\\': self.direction = [y, x]
        if track == '/':  self.direction = [-y, -x]
        if track == '+':
            if self.nextTurn == 0: self.direction = [y, -x] 
            if self.nextTurn == 2: self.direction = [-y, x] 
            self.nextTurn = (self.nextTurn + 1) % 3
            
        return
            
def GetDirection(track):
    if track == '^': return [0, -1]
    if track == '>': return [1, 0]
    if track == 'v': return [0, 1]
    if track == '<': return [-1, 0]
    return [0, 0]

def GetHiddenTrack(track):
    if track in '<>': return '-'
    if track in '^v': return '|'
    return track

def NumberAlive(carts):
    numberAlive = 0
    for cart in carts:
        if cart.alive: numberAlive += 1
    return numberAlive

def BuildTracksAndCarts(inputlines):
    tracks = [[' ' for x  in range(len(line))] for y, line in
              enumerate(inputlines)]
    carts  = []
    for y, line in enumerate(inputlines):
        for x, track in enumerate(line):
            if track == '\n': continue
            
            location  = [x, y]
            
            if track in '^>v<':
                direction = GetDirection(track)
                carts.append(Cart(location, direction))
                track = GetHiddenTrack(track)
                
            tracks[y][x] = track
            
    return tracks, carts

def PrintGrid(tracks, carts):
    
    for y, line in enumerate(inputLines):
        for x in range(len(line)):
            
            hasCart = False
            
            for cart in carts:
                if not cart.alive: continue 
                if cart.location == [x, y]:
                    hasCart = True
                    print('x', end='')
                    break
                
            if not hasCart: print (tracks[y][x], end='')
        print ()
    
def FirstCrash(tracks, carts):
    while True:
        
        carts.sort(key=lambda c: (c.location[0], c.location[1]))
        
        for cartIndex, cart in enumerate(carts):
            
            cart.Move()
            
            if any(cart2.location == cart.location for cart2Index, cart2 in
                    enumerate(carts) if cart2Index != cartIndex):
                print ( cart.location )
                return
            
            x = cart.location[0]
            y = cart.location[1]
            track = tracks[y][x]
            cart.Turn(track)

def LastLocation(tracks, carts):
    
    while True:
        
        # PrintGrid(tracks, carts)
        numberAlive = NumberAlive(carts)
        
        if numberAlive <= 1:
            for cart in carts:
                if cart.alive: 
                    print ( cart.location )
            return
            
        carts.sort(key=lambda c: (c.location[0], c.location[1]))
        
        for cartIndex, cart in enumerate(carts):
            
            cart.Move()
            
            for cart2Index, cart2 in enumerate(carts):
                if cart.alive and cart2.alive and cart2Index != cartIndex:
                    if cart.location == cart2.location:
                        cart.alive  = False
                        cart2.alive = False
                    
            x = cart.location[0]
            y = cart.location[1]
            track = tracks[y][x]
            cart.Turn(track)

inputLines = [ line.rstrip("\n") for line in open("testInput2.txt") ]
inputLines = [ line.rstrip("\n") for line in open("input.txt") ]

tracks, carts = BuildTracksAndCarts(inputLines)

FirstCrash(tracks, carts)
LastLocation (tracks, carts)

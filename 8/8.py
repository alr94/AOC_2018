class Node:
    def __init__(self):
        self.NumberChildren = 0
        self.NumberMetaData = 0
        self.MetaData       = []
    
def FindAllNodes(treeArray, nodes):
    
    newNode                = Node()
    newNode.NumberChildren = treeArray[0]
    newNode.NumberMetaData = treeArray[1]
    
    newTreeArray           = treeArray[2:]
    
    scores = []
    
    for i in range(newNode.NumberChildren):
        newTreeArray, score = FindAllNodes(newTreeArray, nodes)
        scores.append(score)
    
    newNode.MetaData = newTreeArray[:newNode.NumberMetaData]
    nodes.append(newNode)
    
    if newNode.NumberChildren == 0:
        return (newTreeArray[newNode.NumberMetaData:], sum(newNode.MetaData))
    else: 
        return (
                newTreeArray[newNode.NumberMetaData:], 
                sum(scores[k - 1] for k in newNode.MetaData if k > 0 and k <=
                    len(scores))
                )

    
inputLines = [ line.rstrip("\n").split() for line in open("input.txt") ][0]
treeArray  = [ int(x) for x in inputLines ]

nodes = []
treeArray, score = FindAllNodes(treeArray, nodes)

sumOfMeta = 0
for node in nodes:
    for meta in node.MetaData:
        sumOfMeta += meta
        
print (sumOfMeta)
print (score)

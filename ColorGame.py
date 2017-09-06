# read the file
import sys
import operator

lines = []
with open(sys.argv[1]) as f:
    lines.extend(f.read().splitlines())
# read the file
#Depth and choice of colors
depth = lines[2];
colors = []
colorline = lines[0].split(',')
for color in colorline:
    colors.append(color.strip())
#Player 1's Priority of Colors:
P1Priority = {}
P1ColorValue = {}
player1colors = lines[3].split(',')
for player1color in player1colors:
    P1color = player1color.split(':')
    P1ColorValue[P1color[0].strip()] = int(P1color[1].strip())

P2Priority = {}
P2ColorValue = {}
player2colors = lines[4].split(',')
for player2color in player2colors:
    P2color = player2color.split(':')
    P2ColorValue[P2color[0].strip()] = int(P2color[1].strip())
#sorting color:weight pair first based on weight then on color
P1Priority=sorted(P1ColorValue.items(), key=operator.itemgetter(1,0))
P2Priority=sorted(P2ColorValue.items(), key=operator.itemgetter(1,0))

neighbourMap = {}
iterator = 5 #neighbor map starts from line 6 (from 5 in array)
listNo = 0
while iterator < len(lines):
    listNo += 1 #counting the number of lines in neighbor map for future iteration
    nodeLine = lines[iterator].split(':')
    neighbours = nodeLine[1].split(',')
    neighbourList = []
    #neighbours of : nodeLine[0].strip())
    for neighbour in neighbours:
        neighbourList.append(neighbour.strip())
    neighbourMap[nodeLine[0].strip()] = neighbourList
    iterator += 1

fo = open("output.txt", "w")
#create the node structure
#objects of this class will be created for min and max player for their steps in the game
class NodeInGame(object):
    def __init__(self, state, color, stateColorMap, maxScore, minScore, eval, alpha, beta, minormaxPlayer, depth,
                 parent, bestMove, isCutOff):
        self.state = state
        self.color = color
        self.stateColorMap = stateColorMap
        self.maxScore = maxScore
        self.minScore = minScore
        self.eval = eval
        self.alpha = alpha
        self.beta = beta
        self.minormaxPlayer = minormaxPlayer
        self.depth = depth
        self.parent = parent
        self.bestMove = bestMove
        self.isCutOff = isCutOff
#Every initial state will have even moves of Player 1 and Player 2 with Player 1 starting first
#define the initial state by reading the lines

# WA: R-1, SA: G-2 initial set of moves played in the game
initMovesLine = lines[1].split(',')
stateColor = {}  # holds the state and assigned color at any time in the game
latestState = ""
latestColor = ""
latestPlayer = ""
evaluation = float("-inf");#This acts as a unbounded upper value for comparison
maxScore = 0
minScore = 0
for initMove in initMovesLine:
    move = initMove.split(':')
    colorAndPlayer = move[1].strip().split('-')
    stateColor[move[0].strip()] = colorAndPlayer[0].strip()
    latestState = move[0].strip();
    latestColor = colorAndPlayer[0].strip();
    latestPlayer = colorAndPlayer[1].strip()
    if latestPlayer == "1":
        maxScore += int(P1ColorValue.get(colorAndPlayer[0].strip()))
    if latestPlayer == "2":
        minScore += int(P2ColorValue.get(colorAndPlayer[0].strip()))

#Player who played latest: Player, latestPlayer
# root depth=0, INIT root level eval=-inf, aplha=-inf, beta=inf
# Created the root node from the initial state"
# state,color,stateColorMap,eval,alpha,beta,minormaxPlayer,depth,parent
rootNode = NodeInGame(latestState, latestColor, stateColor, maxScore, minScore, evaluation, float("-inf"), float("inf"),
                      latestPlayer, 0, "NA", "None", 0)

#a function that will return the nodes to be expanded at each level
def findNodesToExpand(coloredNodes, stateColorMapping, depth):
    nodesToExpand = []
    stateColorToExpand = []
    for state in coloredNodes:
        neighbourNodes = neighbourMap.get(state)
        for neighbour in neighbourNodes:
            if (neighbour not in nodesToExpand) & (neighbour not in coloredNodes):
                if int(depth) % 2 == 1:
                    priorities = P1Priority
                else:
                    priorities = P2Priority
                # to find the state+color order
                # select player to play based on the depth of the game tree : P1 is max player, P2 is min player
                for key,values in priorities:
                    iNeighbours = neighbourMap.get(neighbour)# check neighbour of neighbours to assign color to neighboutr of the colored state
                    colorUsed = 0
                    for adjacent in coloredNodes:  # check if a neighbouring node already uses the color for key
                        if (adjacent in iNeighbours) & (key == stateColorMapping.get(adjacent)):
                            colorUsed = 1
                            break;
                    if colorUsed == 0:
                        nodesToExpand.append(neighbour)
                        stateColorToExpand.append(neighbour + "-" + key);
    return stateColorToExpand

def createExpansionList(nodesSorted, parentNode, nodeDepth, stateAndColorMap):
    nodeExpansion = []
    if int(nodeDepth) % 2 == 1:
        latestPlayer = 1
    else:
        latestPlayer = 2
    for nodeInLevel in nodesSorted:
        stateAndColor = nodeInLevel.split("-")
        stateAndColorMap[stateAndColor[0]] = stateAndColor[1]
        parent = parentNode.state + "-" + parentNode.color;
        if latestPlayer == 2:  # min
            minscore = parentNode.minScore + int(P2ColorValue.get(stateAndColor[1]))
            maxScore = parentNode.maxScore
            value = float("-inf")
        else:  # max
            maxScore = parentNode.maxScore + int(P1ColorValue.get(stateAndColor[1]))
            minscore = parentNode.minScore
            value = float("inf")
        levelNode = NodeInGame(stateAndColor[0], stateAndColor[1], stateAndColorMap, maxScore, minscore, value,
                               parentNode.alpha, parentNode.beta, latestPlayer, nodeDepth, parent, "None", 0)
        del stateAndColorMap[stateAndColor[0]]  # remove the state color added after creation of nodes
        nodeExpansion.append(levelNode)
    return nodeExpansion

def alphaBeta(samelevelNodes, prevParent, isMinOrMax, atDepth):
    isCutOff = 0
    for leaf in samelevelNodes:
        if (atDepth == maxDepth):
            leaf.alpha = prevParent.alpha
            leaf.beta = prevParent.beta
            leaf.depth = atDepth
            leaf.eval = leaf.maxScore - leaf.minScore
            fo.write(leaf.state + ", " + leaf.color + ", " + str(leaf.depth) + ", " + str(leaf.eval) + ", " + str(
                leaf.alpha) + ", " + str(leaf.beta))
            fo.write('\n')
        evalChanged = prevParent.eval
        if isMinOrMax == 1:  # max player
            prevParent.eval = max(prevParent.eval, leaf.eval)#-inf assigned to min node while creation #for max player - parent is min node
            prevParent.depth = atDepth - 1
            if evalChanged != prevParent.eval:
                prevParent.bestMove = leaf.state + ", " + leaf.color + ", " + str(leaf.eval)
            if (leaf.eval >= prevParent.beta):
                isCutOff = 1
                prevParent.isCutOff = isCutOff
                break;
            prevParent.alpha = max(prevParent.alpha, prevParent.eval)
            fo.write(prevParent.state + ", " + prevParent.color + ", " + str(prevParent.depth) + ", " + str(
                prevParent.eval) + ", " + str(prevParent.alpha) + ", " + str(prevParent.beta))
            fo.write('\n')
        else:
            prevParent.eval = min(prevParent.eval, leaf.eval)
            prevParent.depth = atDepth - 1
            if evalChanged != prevParent.eval:
                prevParent.bestMove = leaf.state + ", " + leaf.color + ", " + str(leaf.eval)
            if (leaf.eval <= prevParent.alpha):
                isCutOff = 1
                prevParent.isCutOff = isCutOff
                break;
            prevParent.beta = min(prevParent.beta, prevParent.eval)
            fo.write(prevParent.state + ", " + prevParent.color + ", " + str(prevParent.depth) + ", " + str(
                prevParent.eval) + ", " + str(prevParent.alpha) + ", " + str(prevParent.beta))
            fo.write('\n')
    if isCutOff == 1:
        fo.write(prevParent.state + ", " + prevParent.color + ", " + str(prevParent.depth) + ", " + str(
            prevParent.eval) + ", " + str(prevParent.alpha) + ", " + str(prevParent.beta))
        fo.write('\n')
    return prevParent


def playGame(countDepth, nodesExpansionMap, stateColorMapCopy, parentNode, isTraceback):
    nextAssign=0;
    while nodesExpansionMap:
        expandedNodesAtLevelSorted = [];
        if isTraceback!=1 or countDepth==maxDepth:
            expandedNodesAtLevel = findNodesToExpand(sorted(stateColorMapCopy), stateColorMapCopy,
                                                     countDepth)  # passing the sorted states that have already been colored
            expandedNodesAtLevelSorted = sorted(expandedNodesAtLevel)
            nodesOnALevel = [];
            if expandedNodesAtLevelSorted:
                if nextAssign==1:
                    fo.write(parentNode.state + ", " + parentNode.color + ", " + str(parentNode.depth) + ", " + str(
                            parentNode.eval) + ", " + str(parentNode.alpha) + ", " + str(parentNode.beta))
                    fo.write('\n')
                nodesOnALevel = createExpansionList(expandedNodesAtLevelSorted, parentNode, countDepth, stateColorMapCopy)
                if (countDepth < maxDepth) & (isTraceback != 1):
                    fo.write(nodesOnALevel[0].state + ", " + nodesOnALevel[0].color + ", " + str(
                        nodesOnALevel[0].depth) + ", " + str(nodesOnALevel[0].eval) + ", " + str(
                        nodesOnALevel[0].alpha) + ", " + str(nodesOnALevel[0].beta))
                    fo.write('\n')
                nodesExpansionMap[countDepth] = nodesOnALevel;
                parentNode = nodesOnALevel[0];
                if countDepth < maxDepth:
                    stateAndColor = expandedNodesAtLevelSorted[0].split("-")
                    stateColorMapCopy[stateAndColor[0].strip()] = stateAndColor[1].strip()
            else:
                parentNode.eval = parentNode.maxScore - parentNode.minScore
                countDepth=countDepth-1;
                fo.write(parentNode.state + ", " + parentNode.color + ", " + str(parentNode.depth) + ", " + str(
                    parentNode.eval) + ", " + str(parentNode.alpha) + ", " + str(parentNode.beta))
                fo.write('\n')
        nextAssign=0;
        if (not expandedNodesAtLevelSorted or countDepth == maxDepth):
            if countDepth==maxDepth:
                remainingPrevLevelNodes = updateParent(nodesExpansionMap, countDepth, nodesOnALevel, 1)
            else:
                isTraceback = 1;
                nodesOnALevel = {parentNode}
                remainingPrevLevelNodes = updateParent(nodesExpansionMap, countDepth, nodesOnALevel, 1)
            tempPrevNodes = []
            if (countDepth - 1) == 0:
                fo.write(remainingPrevLevelNodes[0].bestMove);
                fo.write("\n");
                del nodesExpansionMap[countDepth - 1]
                break;
            while not tempPrevNodes:
                tempPrevNodes, remainingPrevLevelNodes = updateUpwards(remainingPrevLevelNodes, stateColorMapCopy,
                                                                       countDepth);
                if tempPrevNodes:
                    parentNode = tempPrevNodes[0]
                    stateColorMapCopy[parentNode.state] = parentNode.color
                    isTraceback=0;
                    nextAssign = 1;
                    break;
                if (countDepth - 2) == 0:
                    fo.write(remainingPrevLevelNodes[0].bestMove);
                    fo.write("\n");
                    nodesExpansionMap={}
                    break;
                countDepth = countDepth - 1;
            if (countDepth - 1) == 0 and not nodesExpansionMap[countDepth]:
                fo.write(remainingPrevLevelNodes[0].bestMove);
                fo.write("\n");
                del nodesExpansionMap[countDepth - 1]
                break;
        else:
            countDepth += 1

def updateUpwards(remainingPrevLevelNodes, stateColorMapCopy, countDepth):
    tempPrevNodes = remainingPrevLevelNodes
    del stateColorMapCopy[remainingPrevLevelNodes[0].state]
    levelUpNodeList = {remainingPrevLevelNodes[0]}
    remainingPrevLevelNodes = updateParent(nodesExpansionMap, countDepth - 1, levelUpNodeList, 1)
    tempPrevNodes.pop(0)
    if (remainingPrevLevelNodes[0].isCutOff == 1):
        del tempPrevNodes[:]
    if tempPrevNodes:
        tempPrevNodes[0].alpha = remainingPrevLevelNodes[0].alpha
        tempPrevNodes[0].beta = remainingPrevLevelNodes[0].beta
        nodesExpansionMap[countDepth - 1] = tempPrevNodes;
    return tempPrevNodes, remainingPrevLevelNodes

def updateParent(nodesExpansionMap, countDepth, nodes, goBackLevel):
    isMinOrMax = 0
    if (countDepth - goBackLevel) % 2 == 0:  # max player's move at even depth
        isMinOrMax = 1

    remainingPrevLevelNodes = nodesExpansionMap.get(countDepth - goBackLevel)
    if nodes and remainingPrevLevelNodes and (
        countDepth - goBackLevel) >= 0:  # if nodes cannot expand further: update their parent on level-1
        remainingPrevLevelNodes[0] = alphaBeta( nodes, remainingPrevLevelNodes[0], isMinOrMax, countDepth)
        del nodesExpansionMap[countDepth - goBackLevel]
        nodesExpansionMap[countDepth - goBackLevel] = remainingPrevLevelNodes  # updating the level-nodes map with updated parent
    if countDepth in nodesExpansionMap and countDepth == maxDepth:
        del nodesExpansionMap[countDepth]  # after max level computation, remove the leaf nodes list from map for that max depth
    return remainingPrevLevelNodes;

#ordering the states in alphabetical order for expansion
orderedNeighbourMap = sorted(neighbourMap)
maxDepth = int(depth)

countDepth = 1;
# get a list of nodes to be expanded from the initial state
stateColorMapCopy = stateColor  # To update the nodes colored on the path of expansion and removed when the next same-level node is tried
nodesExpansionMap = {}  # use this expansion list as a stack and keep appending a node list to it, everytime a node is expanded
#add the node at Depth 0 first
rootNodeList = []
rootNodeList.append(rootNode)
nodesExpansionMap[0] = rootNodeList

fo.write(rootNode.state + ", " + rootNode.color + ", " + str(rootNode.depth) + ", " + str(rootNode.eval) + ", " + str(rootNode.alpha) + ", " + str(rootNode.beta))
fo.write('\n')

playGame(countDepth, nodesExpansionMap, stateColorMapCopy, rootNode, 0)

from filecmp import cmp
import random
import math
import sys
import os
import operator
from copy import deepcopy
import collections
'''                                                       16 PUZZLE SOLVER
_______________________________________________________________________________________________________________________________________
                                                    FORMULTION OF THE SEARCH PROBLEM
DESCRIPTION:
This program takes an input board configuration for 16 puzzle solver and solves the problem by generating all
the possible states at every node. It uses the A* search algorithm to calculate the optimal path for solving the problem. The inital and
goal nodes are taken and the path is computed by using the distance travelled in combination with the heuristic function.

PARAMETERS:             python3 solver16.py <input-board-file-name>

STATE SPACE:            The state space for this problem is the list of all 16 operation possible from one state.
                        right row 1 (R1) ,R2, R3, R4,
                        L1, L2, L3, L4
                        U1, U2, U3, U4
                        D1, D2, D3, D4

SUCCESSOR FUNCTION:     Successor functions will be same for each node, since we will be doing all 16 operations

EDGE WEIGHTS:           Edge weights will are considered as 1 between 2 nodes

HEURISTIC FUNCTION:     We have used the sum of manhattan distance as the heuristic function which gives the sum for each state.
                        Based on this then the minimum F(N) State is picked for expansion.
_______________________________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________________________
                                                      WORKING OF SEARCH ALGORITHM

APPROACH:
    1. Each node expands to 16 states since we have R1, R2 R3, R4, L1, L2, L3, L4, U1, U2, U3, U4,D1, D2, D3, D4
    2. Fetch the minimum value of F(N) = G(N)+Heuristic.
    3. Check if minimum node is the goal node. If yes stop and print path, If not continue
    3. Repeat steps 1,2,3 for the consecutive nodes till a goal node is reached.


PSEUDO CODE:
    1. Each level has 16 combinations since there are 16 moves possible.
    Level 1 representation : Example 1R1, 1R2, .... 1D3,1D4
                 For 1R1 1= level, R=Right, 1=row1
                     1R2 1= level, R=Right, 2=row2
    Level 2 representation : Example 2R1, 2R2,.....2D3, 2D4
                 For 2R1 2=level, R=Right, 1=row1
    2. "I" key for Initial state
       "G" key for Goal state

    1. Take user input text file for the Initial state.
    2. Create the Goal State.
    3. Call A* function:
        Initialize:
        Visited Nodes {List} : Lists all visited nodes which need to be skipped in future
        Fringe {List}        : Lists the traversal path
        Parent {Dict}        : Stores the parent of each node : key-state(Ex R1, R2..) value-parent of the key(Ex I,R1,R2)
        G(n) function {Dict} : Stores the g(N) Values
        F(n) function {Dict} : Stores the f(N) Values
    4. Assign Initial state to the fringe and let it be current node
        while FRINGE >0
    5. Check if the current state is goal state If yes print the path, If no continue
    6. pop fringe and add it to the visited nodes
    7. Get branches for current node:
        for each branch node
        Save the parent of the current node for  back tracking.
        Calculate g value of current node
        calculate f value of current node = g(N) + Heuristic
        Add branch nodes to FRINGE
Refered pseudoCode
___________________________________________________________________________________________________________________________________

_______________________________________________________________________________________________________________________________________
TEST CASES
We have used the files for testing the program.
The files are also present along with the program in the folder
_______________________________________________________________________________________________________________________________________
ISSUES:
1. Heuristic functions : we considered misplaced tiles 1st but later used the sum of manhattan distace due to performance issue.
_______________________________________________________________________________________________________________________________________
'''
def calModManhattanDistance(state):
    manhattanDistanceSum = 0
    for x in range(0, 3):                   # x-dimension, traversing rows (i)
        for y in range(0, 3):               # y-dimension, traversing cols (j)
            value = statesDictionary[state][x][y];     # tiles array contains board elements
            if (value != 0):
                targetX = math.floor((int(value) - 1) / 4);  # expected x-coordinate (row)
                targetY = (int(value) - 1) % 4;  # expected y-coordinate (col)
                
                if (targetX == 0 and x == 3) or (targetX == 3 and x == 0):
                    dx = 1
                else:
                    dx = x - targetX;           # x-distance to expected coordinate
                if (targetY == 0 and y == 3) or (targetY == 3 and y == 0):
                    dy = 1
                else:
                    dy = y - targetY;           # y-distance to expected coordinate
                manhattanDistanceSum = manhattanDistanceSum + abs(dx) + abs(dy);

    print("\nFor State: ", state," Modified Manhattan Distance is:",manhattanDistanceSum,"\n")
    return manhattanDistanceSum;

def calculateManhattanDistance(state):
    manhattanDistanceSum = 0
    for x in range(0, 4):                   # x-dimension, traversing rows (i)
        for y in range(0, 4):               # y-dimension, traversing cols (j)
            value = statesDictionary[state][x][y];     # tiles array contains board elements
            if (value != 0):
                targetX = int((int(value) - 1) / 4);  # expected x-coordinate (row)
                targetY = (int(value) - 1) % 4;  # expected y-coordinate (col)
                dx = x - targetX;           # x-distance to expected coordinate
                dy = y - targetY;           # y-distance to expected coordinate
                manhattanDistanceSum = manhattanDistanceSum + abs(dx) + abs(dy);
    return manhattanDistanceSum;

def calculateMisplacedTiles(currentState, goalState,parent,level):
    #stateToShift = parent[currentState]
    #state = deepcopy(statesDictionary.get(stateToShift))
    #shiftedState = calculateShift(state,currentState,parent,level)
    misplacedTilesCounter = 0
    for i in range(0,4):
        for j in range(0,4):
            if((int(statesDictionary[currentState][i][j]) - int(goalState[i][j])) == 0):
                continue
            else:
                misplacedTilesCounter = misplacedTilesCounter +1
    print("\nFor State: ", currentState," Misplaced tiles count is:",misplacedTilesCounter,"\n")
    return misplacedTilesCounter

def calculateShift(shiftState,shiftName,level):
    if shiftName == str(level)+"R1":
        tmp = shiftState[0][0]
        shiftState[0][0] = shiftState[0][3]
        shiftState[0][3] = shiftState[0][2]
        shiftState[0][2] = shiftState[0][1]
        shiftState[0][1] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"R2":
        tmp = shiftState[1][0]
        shiftState[1][0] = shiftState[1][3]
        shiftState[1][3] = shiftState[1][2]
        shiftState[1][2] = shiftState[1][1]
        shiftState[1][1] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"R3":
        tmp = shiftState[2][0]
        shiftState[2][0] = shiftState[2][3]
        shiftState[2][3] = shiftState[2][2]
        shiftState[2][2] = shiftState[2][1]
        shiftState[2][1] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"R4":
        tmp = shiftState[3][0]
        shiftState[3][0] = shiftState[3][3]
        shiftState[3][3] = shiftState[3][2]
        shiftState[3][2] = shiftState[3][1]
        shiftState[3][1] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"L1":
        tmp = shiftState[0][0]
        shiftState[0][0] = shiftState[0][1]
        shiftState[0][1] = shiftState[0][2]
        shiftState[0][2] = shiftState[0][3]
        shiftState[0][3] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"L2":
        tmp = shiftState[1][0]
        shiftState[1][0] = shiftState[1][1]
        shiftState[1][1] = shiftState[1][2]
        shiftState[1][2] = shiftState[1][3]
        shiftState[1][3] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"L3":
        tmp = shiftState[2][0]
        shiftState[2][0] = shiftState[2][1]
        shiftState[2][1] = shiftState[2][2]
        shiftState[2][2] = shiftState[2][3]
        shiftState[2][3] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"L4":
        tmp = shiftState[3][0]
        shiftState[3][0] = shiftState[3][1]
        shiftState[3][1] = shiftState[3][2]
        shiftState[3][2] = shiftState[3][3]
        shiftState[3][3] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"U1":
        tmp = shiftState[0][0]
        shiftState[0][0] = shiftState[1][0]
        shiftState[1][0] = shiftState[2][0]
        shiftState[2][0] = shiftState[3][0]
        shiftState[3][0] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"U2":
        tmp = shiftState[0][1]
        shiftState[0][1] = shiftState[1][1]
        shiftState[1][1] = shiftState[2][1]
        shiftState[2][1] = shiftState[3][1]
        shiftState[3][1] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"U3":
        tmp = shiftState[0][2]
        shiftState[0][2] = shiftState[1][2]
        shiftState[1][2] = shiftState[2][2]
        shiftState[2][2] = shiftState[3][2]
        shiftState[3][2] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"U4":
        tmp = shiftState[0][3]
        shiftState[0][3] = shiftState[1][3]
        shiftState[1][3] = shiftState[2][3]
        shiftState[2][3] = shiftState[3][3]
        shiftState[3][3] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"D1":
        tmp = shiftState[3][0]
        shiftState[3][0] = shiftState[2][0]
        shiftState[2][0] = shiftState[1][0]
        shiftState[1][0] = shiftState[0][0]
        shiftState[0][0] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"D2":
        tmp = shiftState[3][1]
        shiftState[3][1] = shiftState[2][1]
        shiftState[2][1] = shiftState[1][1]
        shiftState[1][1] = shiftState[0][1]
        shiftState[0][1] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"D3":
        tmp = shiftState[3][0]
        shiftState[3][2] = shiftState[2][2]
        shiftState[2][2] = shiftState[1][2]
        shiftState[1][2] = shiftState[0][2]
        shiftState[0][2] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState
    if shiftName == str(level)+"D4":
        tmp = shiftState[3][0]
        shiftState[3][3] = shiftState[2][3]
        shiftState[2][3] = shiftState[1][3]
        shiftState[1][3] = shiftState[0][3]
        shiftState[0][3] = tmp
        statesDictionary[shiftName] = shiftState
        return shiftState

def reconstructPath(parent,current):
    total_path = [current]
    while current in parent:
        current = parent[current]
        total_path.append(current)
    total_path.reverse()
    print("The moves from Start Node to End Node is:\n", total_path)

    cnt = 0
    for x in total_path:
        print("\n")
        print(statesDictionary[x][0])
        print(statesDictionary[x][1])
        print(statesDictionary[x][2])
        print(statesDictionary[x][3])
    return total_path

def getNextStates(current):

    print()
def astarSearch():

    print("\n****** A* SEARCH ALGORITHM *********:\n")

    #Array for visited nodes
    visitedNodes = []
    visitedFlag = 'N'

    #Fringe for currently used node
    fringe = []
    fringe.append("I")

    # The dictionary for navigated nodes.
    parent = {}

    # Function G Array i.e g(n)
    gValue = {}
    gValue["I"] = 0

    #Function F array i.e f(n)
    fValue = {}
    fValue["I"] = int(gValue["I"]) + 1
    level =1;
    while len(fringe) > 0:
        print("\nCurrent Fringe ",fringe)
        # Assigning current with the least function value Node i.e least f(n) which should be present in fringe
        sorted_x = sorted(fValue.items(), key=operator.itemgetter(1))
        currentAssigned =0
        lowestCost = 0
        fringeIndex = 0
        for nodeTuple in sorted_x:
            if(currentAssigned == 1):
                break
            if nodeTuple[0] in fringe:
                if nodeTuple[0] == 'I':
                    current = nodeTuple[0]
                if lowestCost == 0:
                    lowestCost = nodeTuple[1]
                    fringeIndex = fringe.index(nodeTuple[0])
                elif (lowestCost == nodeTuple[1]) and fringe.index(nodeTuple[0]) < fringeIndex:
                    fringeIndex = fringe.index(nodeTuple[0])
                if lowestCost != nodeTuple[1]:
                    currentAssigned =1
            if(currentAssigned == 1):
                current = fringe[fringeIndex]
                break

        if((statesDictionary[current][0][0] == statesDictionary["G"][0][0]) and (statesDictionary[current][0][1] == statesDictionary["G"][0][1]) and (statesDictionary[current][0][2] == statesDictionary["G"][0][2]) and (statesDictionary[current][0][3] == statesDictionary["G"][0][3])) and\
            ((statesDictionary[current][1][0] == statesDictionary["G"][1][0]) and (statesDictionary[current][1][1] == statesDictionary["G"][1][1]) and (statesDictionary[current][1][2] == statesDictionary["G"][1][2]) and (statesDictionary[current][1][3] == statesDictionary["G"][1][3])) and\
            ((statesDictionary[current][2][0] == statesDictionary["G"][2][0]) and (statesDictionary[current][2][1] == statesDictionary["G"][2][1]) and (statesDictionary[current][2][2] == statesDictionary["G"][2][2]) and (statesDictionary[current][2][3] == statesDictionary["G"][2][3])) and\
            ((statesDictionary[current][3][0] == statesDictionary["G"][3][0]) and (statesDictionary[current][3][1] == statesDictionary["G"][3][1]) and (statesDictionary[current][3][2] == statesDictionary["G"][3][2]) and (statesDictionary[current][3][3] == statesDictionary["G"][3][3])):
            print("Reconstructing Path")
            aStarPath = reconstructPath(parent, current)
            # TODO displayPath(aStarPath, listOfLists)
            break

        for j in range(len(fringe)):
            if fringe[j] == current:
                del fringe[j]
                break
        visitedNodes.append(current)

        #Get the branching Nodes,
        preBranchNodes = ['R1','R2','R3','R4','L1','L2','L3','L4','U1','U2','U3','U4','D1','D2','D3','D4']
        branchNodes = []
        for branch in preBranchNodes:
            branchNodes.append(str(level) + branch)

        for nextNode in branchNodes:
            state = deepcopy(statesDictionary.get(current))
            calculateShift(state,nextNode,level)
            visitedFlag = 'N'
            for vNode in visitedNodes:
                if((statesDictionary[nextNode][0][0] == statesDictionary[vNode][0][0]) and (statesDictionary[nextNode][0][1] == statesDictionary[vNode][0][1]) and (statesDictionary[nextNode][0][2] == statesDictionary[vNode][0][2]) and (statesDictionary[nextNode][0][3] == statesDictionary[vNode][0][3])) and\
                    ((statesDictionary[nextNode][1][0] == statesDictionary[vNode][1][0]) and (statesDictionary[nextNode][1][1] == statesDictionary[vNode][1][1]) and (statesDictionary[nextNode][1][2] == statesDictionary[vNode][1][2]) and (statesDictionary[nextNode][1][3] == statesDictionary[vNode][1][3])) and\
                    ((statesDictionary[nextNode][2][0] == statesDictionary[vNode][2][0]) and (statesDictionary[nextNode][2][1] == statesDictionary[vNode][2][1]) and (statesDictionary[nextNode][2][2] == statesDictionary[vNode][2][2]) and (statesDictionary[nextNode][2][3] == statesDictionary[vNode][2][3])) and\
                    ((statesDictionary[nextNode][3][0] == statesDictionary[vNode][3][0]) and (statesDictionary[nextNode][3][1] == statesDictionary[vNode][3][1]) and (statesDictionary[nextNode][3][2] == statesDictionary[vNode][3][2]) and (statesDictionary[nextNode][3][3] == statesDictionary["G"][3][3])):
                    visitedFlag = 'Y'
                    break

            if visitedFlag == 'Y':
                continue

            tentativeGValue = int(gValue[current]) + 1

            if nextNode not in fringe:
                parent[nextNode] = current
                gValue[nextNode] = tentativeGValue
                #fValue[nextNode] = gValue[nextNode] + calModManhattanDistance(nextNode)#calculateMisplacedTiles(nextNode,statesDictionary["G"],parent,level)
                fValue[nextNode] = gValue[nextNode] + calculateManhattanDistance(nextNode)

                if nextNode not in fringe:
                    fringe.append(nextNode)
        level += 1
        print ("\n********* LEVEL  ", level, " **************\n")
    return False

# Main Program from where the program starts
if __name__ == "__main__":
    input_board_filename = sys.argv[1]

    # Creates a list containing 4 lists initialized to 0
    initialState = []
    goalState = []

    goalState = [['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15','16']]
    # Forming a 2D array from the input board file
    with open(input_board_filename, "r") as ins:
        for line in ins:
            newline = line.rstrip()
            splitvalue = newline.split(' ')
            initialState.append(splitvalue)

    print("\n****** INPUT BOARD *********\n")
    for boardLine in initialState:
        print(boardLine,"\n")

    statesDictionary = {}
    statesDictionary["I"] = initialState
    statesDictionary["G"] = goalState
    # Function Call to perform A* Search
    astarSearch()


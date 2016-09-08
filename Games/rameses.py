#python3
import random
import sys
import os
import time


'''                                                       Part 2: Programming problems - Rameses
_______________________________________________________________________________________________________________________________________

DESCRIPTION:
The Ramses program takes a current state as input and provides the user with the next move.

PARAMETERS:             python3 Rameses.py [nValue] [currentState] [Time limit in seconds]
_______________________________________________________________________________________________________________________________________
APPROACH:

Take the current node as input node.
Check if the node is the terminal node.
Get the current time.
Check of the current node is the terminal node. If yes, print error.
Condition to check if the number of pebbles are < n*n/3 (If the board has very less [pebbles, then display a good move from its children )
Else perform alpha beta pruning: Alpha beta optimizes the algorithm by cutting the paths which do not contribute to the final result.
    If terminal node is reached:
        Evaluate the node
    If maximizing player:
        Assign v with minimum value( - infinity)
        loop through all children:
            Assign v with maximum(v, alphabeta(child, alpha, beta))
            Assign alpha with max(alpha, v)
            for pruning check if beta>=alpha : break(pruning)
        return v
    else
        Assign v with maximum value(+ infinity)
        loop through all children:
            Assign v with minimum(v, alphabeta(child, alpha, beta))
            Assign beta with min(beta,v)
            for pruning check if beta<=alpha : break(pruning)
        return v
The algorithm resturns the score to the root node.
Fetch the child node at level one which has the same score.
If there are multiple nodes, then display any one of them.
--------------------------------------------------------------------------------------------------------------------------------
The Static evaluation function checks if the state leads to a loss for max player - if all crosses appear in a row,
column or diagonal.
It will assign a -9 for such a loss node and a +10 for other nodes.

Time limit:
Start Timer at the start of the code.
Get time at every level and compare it with the threshold set(Threshold set for my code is half of the input time)
    The code checks if the elapsed time < timeLimit/2
If the threshold is reached then the algorithm takes this level as horizon(doesnt check the further children)
and in the remaining time backtracks and prunes rest of the nodes.
Thus it finds a move with maximum score for the max player.
_______________________________________________________________________________________________________________________________________
'''

scoresLists = []

def successors(node):
    childMoves = []
    curNode = ''
    for i in range(0,(len(node))):
        curNode = node
        if curNode[i] == '.':
            curNode = curNode[:i] + "x" + curNode[i+1:]
            childMoves.append(curNode)
        elif curNode[i] == 'x':
            continue
    return childMoves

def get_enemy(player):
    if player == 'MAX':
        return 'MIN'
    return 'MAX'

def alphabeta(node, depth, alpha, beta, maximizingPlayer,level):

    if isLeafNode(node):
        return evaluate(node,maximizingPlayer)

    if maximizingPlayer:
        v = -999

        #stop = datetime.now()-start
        stopMax = time.time()
        diffMax = round(stopMax - start)
        if diffMax < int(timeLimit/2):
            children = successors(node)
        else:
            return evaluate(node,True)
        for child in children:
            #print(child)
            v=-999
            v = max(v, alphabeta(child, depth - 1, alpha, beta, False, level + 1))
            scoreList = [child, v, level]
            scoresLists.append(scoreList)
            alpha = max(alpha, v)
            if beta <= alpha:
                break # β cut-off
        return v
    else:
        v = 999
        #stop = datetime.now()-start
        stopMin = time.time()
        diffMin = round(stopMin -start)
        if(diffMin < int(timeLimit/2)):
            children = successors(node)
        else:
            return evaluate(node, False)
        for child in children:
            v=999
            v = min(v, alphabeta(child, depth - 1, alpha, beta, True, level + 1))
            scoreList = [child, v, level]
            scoresLists.append(scoreList)
            alpha = min(beta, v)
            if beta <= alpha:
                break # α cut-off
        return v

def isLeafNode(node):
    #print("Is Leaf Node:")
    countRow = 0
    countCol = 0
    countDgl1 = 0
    countDgl2 = 0

    for i in range(0,nValue):

        countRow = 0
        countCol = 0

        # Check if all 3 pebbles in Dialgonal
        dglIndex = (i*nValue) + i
        if(node[dglIndex] == 'x'):
            countDgl1 = countDgl1 +1

        # Check if all 3 pebbles in Dialgona2
        dglIndex = (i*nValue) + ((nValue - i) - 1)
        if(node[dglIndex] == 'x'):
            countDgl2 = countDgl2 +1

        for j in range(0,nValue):
            # Checks if all 3 pebbles in any of the ROWS
            rowIndex = (i*nValue) + j
            if (node[rowIndex] == 'x'):
                countRow = countRow+1

            # Checks if all 3 pebbles in any of the COLUMNS
            colIndex = (j*nValue) + i
            if (node[colIndex] == 'x'):
                countCol = countCol+1

        #print (" ROW/COLUMN ", (i+1) ,"count row :",countRow,"count col :", countCol)
        if(countRow == nValue) | (countCol == nValue):
            return True
    #print ("\n count dgl 1 :",countDgl1,"countdgl 2:", countDgl2)
    if (countDgl1 == nValue) | (countDgl2 == nValue):
        return True
    else:
        return False

def evaluate(node,player):
    #print("EVALUATE ")
    score = 0
    countRow = 0
    countCol = 0
    countDgl1 = 0
    countDgl2 = 0

    if(isLeafNode(node)):
        return -9
    else:
        return 10
        '''for i in range(0,nValue):
            countRow = 0
            countCol = 0

            # Check if all 3 pebbles in Dialgonal
            dglIndex = (i*nValue) + i
            if(node[dglIndex] == 'x'):
                countDgl1 = countDgl1 +1

            # Check if all 3 pebbles in Dialgona2
            dglIndex = (i*nValue) + ((nValue - i) - 1)
            if(node[dglIndex] == 'x'):
                countDgl2 = countDgl2 +1

            for j in range(0,nValue):
                # Checks if all 3 pebbles in any of the ROWS
                rowIndex = (i*nValue) + j
                if (node[rowIndex] == 'x'):
                    countRow = countRow+1

                # Checks if all 3 pebbles in any of the COLUMNS
                colIndex = (j*nValue) + i
                if (node[colIndex] == 'x'):
                    countCol = countCol+1
            if(countRow < 2):
                score = score + 1
            if(countCol < 2):
                score = score + 1
    if(countDgl1 < 2):
        score = score + 1
    if(countDgl2 < 2):
        score = score +1'''

    #print("Score of node : ", node," is : [ ",score," ]")
    return score

if __name__ == "__main__":

    # Getting input arguments for start City , End City , Routing Option and Routing Algorithm
    if len(sys.argv) == 4:
        nValue       = int(sys.argv[1])
        stateStr  = sys.argv[2]
        timeLimit    = int(sys.argv[3])
    else:
        print("\n ERROR : Missing the input argument(s)\n\n************ USABILITY ************")
        print("python Rameses.py [n value] [Current Board State] [time limit in secs]")
        sys.exit();

    #start=datetime.now()
    start = time.time()
    curStateStr = stateStr.lower()
    print("\n****** INPUT ARGUMENTS *********\nN Value: ", nValue, "\nCurrent Board State: ", curStateStr,"\nTime Limit in seconds: ",timeLimit)

    '''for i in range(nValue):
        for j in range(nValue):
            print (curStateStr[i*(nValue)+j])'''
    # Check if input node is terminal node.
    if(isLeafNode(curStateStr)):
        print("Current Node: [", curStateStr,"] is the terminal Node.")
        sys.exit()

    counterX = 0
    for inx in range(0,len(curStateStr)):
        if(curStateStr[inx] == 'x'):
            counterX = counterX + 1
    minValue = (nValue*nValue)/3

    if counterX < round(minValue,0):
        children = successors(curStateStr)
        for child in children:
            if isLeafNode(child):
                continue
            else:
                for knx in range(0,len(curStateStr)):
                    if(child[knx] == curStateStr[knx]):
                        continue
                    else:
                        move = knx
                        break
                for i in range(0,nValue):
                    for j in range(0, nValue):
                         if(move ==  (nValue*i)+j):
                            row = i+1
                            col = j+1
                            break
                print("\nPlace the pebble at row:",row," col: ",col)
                print("Your move should be :", child)
                sys.exit()
    else:
        val = alphabeta(curStateStr, 2, -999, 999, True, 0)

    if not scoresLists:
        print("\nInsufficient time limit.")
        sys.exit()
    else:
        #Traverse through the scoreLists to get the child with optimal value
        choices = []
        foundMove = 0

        #nodecount = len(scoresLists)
        #print ("NODECOUNT :", nodecount)

        for list in scoresLists:
            #print(list)
            if(int(list[2]) == 0) & (int(list[1]) == val):
                choices.append(list[0])

        for item in choices:
            if (isLeafNode(item)):
                continue
            else:
                for knx in range(0,len(curStateStr)):
                    if(item[knx] == curStateStr[knx]):
                        continue
                    else:
                        move = knx
                        break
                for i in range(0,nValue):
                    for j in range(0, nValue):
                         if(move ==  (nValue*i)+j):
                            row = i+1
                            col = j+1
                            break
                print("\nPlace the pebble at row:",row," col: ",col)
                print("Your move is :\n")
                print(item)
                stop = time.time()
                diff = round(stop - start)
                #print("start : ",start,"stoptimer : ",stop," Time Taken :", diff)
                foundMove = 1
                break

        if(foundMove == 0):
            print("Current Node is the terminal node. Any state will lead to your loss !!")


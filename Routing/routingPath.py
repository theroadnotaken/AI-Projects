import random
import sys
import os
import re
import queue
from math import radians, cos, sin, asin, sqrt
import operator


'''                                                       Program 2 - BFS,DFS,A*
_______________________________________________________________________________________________________________________________________
                                                    FORMULTION OF THE SEARCH PROBLEM
DESCRIPTION:
This program takes an input board configuration for 16 puzzle solver and solves the problem by generating all
the possible states at every node. It uses the A* search algorithm to calculate the optimal path for solving the problem. The inital and
goal nodes are taken and the path is computed by using the distance travelled in combination with the heuristic function.

PARAMETERS:             python3 routingPath.py [start-city] [end-city] []

STATE SPACE:           State space is the list of all the cities fetched from the input file based on the start City

SUCCESSOR FUNCTION:    BFS : picks the children at every level and
                       DFS : PIcks the 1st child and continues int he direction till leaf node
                       A*  : Picks minimum value of the F(N) = G(N) + H(N) and proceeds

EDGE WEIGHTS:         EDGE weights are based on the "routing-option" - either distance, speed, segments


HEURISTIC FUNCTION:   Heuristic function used for the A* search is - latitude and longitude
                      We have referred the Haversine function for heuristic calculation from Ref: https://en.wikipedia.org/wiki/Haversine_formula
_______________________________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________________________
                                                      WORKING OF SEARCH ALGORITHM

BFS : BFS algorithm gets all the children at level 1 and loops though them one by one. It will check if the current node is goal node
        else continue with the expanding the current node. This will continue till the goal node is reached

DFS : DFS algorithm gets the 1st level children and loops through them. It fetches the 1st child and traverses tll the leaf node.
        If goal found it returns the path. Else it will backtrack to

A*  : A* algorithm fetches all the children and expands the one with the minimum F value( F(N) = G(N) +H(N) ). Here having an optimal
        heuristic helps in finding the goal node easily
_______________________________________________________________________________________________________________________________________

_______________________________________________________________________________________________________________________________________
TEST CASES
StartCity : Chicago_Heights,_Illinois
End City  : Pittswood,_Illinois
_____________________________________________________________________________________________________________________________________
OBSERVATIONS:

1. Best search algorithm is the A* algorithm which gives a minimal solution.

2. Between DFS and BFS we found that BFS is more optimal.
start city : Austin,_Texas
end city   : Windcrest,_Texas

BFS : 'Austin,_Texas', 'San_Marcos,_Texas', 'Windcrest,_Texas'
DFS : 'Austin,_Texas', 'Bastrop,_Texas', 'Jct_US_183_&_TX_21,_Texas', 'Luling,_Texas', 'San_Marcos,_Texas', 'Windcrest,_Texas'

Hence BFS gives optimal compared to DFS

3.Computation time will be less for A* followed by BFS, DFS at last
______________________________________________________________________________________________________________________________________
'''
import math
#Program to read the road-segments.txt file
cflag='Y'
def getChildren(startCity):
	var = 'N'
	global cflag
	if cflag == 'Y':
		childList = list()
		with open("road-segments.txt","r") as fileRead:
			for checkLine in fileRead:
				if var == 'N' or var == 'Y':
					child = checkLine.split()
					if child[0] == startCity:
						var = 'Y'
						#print(child[1])
						childList.append(child)
					elif var == 'Y' and child[0] != startCity:
						var = 'E'
			#print(len(childList))
			return childList

def getCount(strCity, trList):
	cnt = 0
	for i in trList:
		if i[0] == strCity:
			cnt+= 1
	#print("Count parent :"+str(cnt))
	return cnt

def dfs(startCity, endCity, acc):
	#print(startCity+"------"+str(acc)+"------"+endCity)
	global cflag
	if startCity == endCity:
		if acc == []:
			acc.append([startCity,startCity,0,0,'-'])
		#acc[1].append(0)
		#acc[2].append(0)
		cflag='N'
		#print("0 :"+cflag)
	else:
		if cflag == 'Y':
			for children in getChildren(startCity):
				#print(startCity+"*****"+str(acc)+"******"+endCity)
				if cflag == 'Y':
					#print("Trace :"+children[1])
					while getCount(children[0],acc) > 0:
						popPath = acc.pop()
						#popDist	= acc[1].pop()
						#popTime = acc[2].pop()
						#print(popPath+" removed from acc. Distance :"+str(popDist)+" Time taken :"+str(popTime))
					#acc[1].append(int(children[2]))
					if int(children[2]) != 0:
						acc.append([children[0],children[1],children[2],int(children[2])/int(children[3]),children[4]])
					#print("1 :"+cflag)
					#print(acc)
					dfs(children[1], endCity, acc)
				else:
					break
		else:
			pass
			#print("2 :"+cflag)
			#print("Last ACC "+str(acc))
		if cflag == 'N':
			return acc
		else:
			return []

def getRoute(startCity,endCity,param):
	global cflag
	cflag = 'Y'
	finalPath = []
	totDist = 0
	totTime = 0
	print("********* DEPTH FIRST SEARCH *********")
	finalList = dfs(startCity,endCity,[])
	if(finalList == []):
		print("No route found beteen "+startCity+" and "+endCity)
	else:
		for desc in finalList:
			finalPath.append(desc[0])
			totDist+= int(desc[2])
			totTime+= round(desc[3],4)
			if param == 'segments':
				print("Take Highway "+desc[4]+" from "+desc[0]+" to "+desc[1])
			if param == 'distance':
				print("Take Highway "+desc[4]+" from "+desc[0]+" to "+desc[1]+" for "+str(desc[2])+" miles")
			if param == 'time':
				print("Take Highway "+desc[4]+" from "+desc[0]+" to "+desc[1]+" for "+str(round(int(desc[3]),4))+" hours")
		finalPath.append(endCity)
		print(str(totDist)+" "+str(round(totTime,4))+" "+str(finalPath))

#BFS Search
def bfsSearch():
    print("\n****** BREADTH FIRST ALGORITHM *********:\n")

    fringe = []
    #BFS 2
    #distant_from_start = {}
    fringe.append(startCity)
    #distance_from_start[startCity] = 0;
    path = {}
    path[startCity] = [startCity]
    listOfLists = []
    foundGoal = 0

    while len(fringe) > 0:
        currentNode = fringe[0]
        del fringe[0]

        #Get the branching Nodes
        with open("road-segments.txt", "r") as ins:
            branchNodes = []
            length = []
            speedlimit = []
            namehighway = []
            for line in ins:
                splitvalue = line.split(' ')
                if currentNode in splitvalue[0]:
                    branchNodes.append(splitvalue[1])
                    length.append(splitvalue[2])
                    speedlimit.append(splitvalue[3])
                    namehighway.append(splitvalue[4])
                    listOfLists.append(splitvalue)
            #print(currentNode,"    :",branchNodes)

        #Get the path
        for nextNode in branchNodes:
            if nextNode not in path:
                path[nextNode] = path[currentNode] + [nextNode]
            if nextNode == endCity:
                fringe = []
                foundGoal = 1
                break
            fringe.append(nextNode)

    if(foundGoal == 1):
        displayPath(path[endCity], listOfLists)
    elif(foundGoal ==0):
        print("No Route for the specified start city and end city")

def heuristic_cost_estimate(startCity,endCity):
    R = 6373.0
    lat1 = 0.0
    lon1 = 0.0
    lat2 = 0.0
    lon2 = 0.0
    with open("city-gps.txt","r") as getCoords:
        for checkLine in getCoords:
            child = checkLine.split()
            if child[0] == startCity:
                lat1 = float(child[1])
                lon1 = float(child[2])
            if child[0] == endCity:
                lat2 = float(child[1])
                lon2 = float(child[2])
                if lat1 != 0.0 and lon1 != 0.0 and lat2 != 0.0 and lon2 != 0.0:
                    break
    #print(str(lat1)+','+str(lon1))
    #print(str(lat2)+','+str(lon2))
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    #print(str(lat1)+','+str(lon1))
    #print(str(lat2)+','+str(lon2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    distance = R * c * 0.621371

    #print("Distance in Miles:", distance)
    return distance

def reconstruct_path(parent,current):
    total_path = [current]
    while current in parent:
        current = parent[current]
        total_path.append(current)
    return total_path

def distanceCalculator(current,nextNode,startNode,branchNodes,length):
    for i in range(len(branchNodes)):
        if startNode[i] == current:
            if branchNodes[i] == nextNode:
                return length[i]

#   A* SEARCH ALGORITHM
def astarSearch(startCity, endCity):
    goalFound = 0;
    print("\n****** A* SEARCH ALGORITHM *********:\n")

    #Array for visited nodes
    visitedNodes = []

    #Fringe for currently used node
    fringe = []
    fringe.append(startCity)

    # The dictionary for navigated nodes.
    parent = {}

    # Function G Array i.e g(n)
    gValue = {}
    gValue[startCity] = 0

    #Function F array i.e f(n)
    fValue = {}
    fValue[startCity] = int(gValue[startCity]) + int(heuristic_cost_estimate(startCity, endCity))
    listOfLists = []
    while len(fringe) > 0:
        # Assigning current with the least function value Node i.e least f(n) which should be present in fringe
        sorted_x = sorted(fValue.items(), key=operator.itemgetter(1))
        currentAssigned =0
        for nodeTuple in sorted_x:
            if(currentAssigned == 1):
                break
            for key in nodeTuple:
                if key in fringe:
                        current = key
                        currentAssigned =1
                if(currentAssigned == 1):
                    break

        if current == endCity:
            aStarPath = reconstruct_path(parent, endCity)
            aStarPath.reverse()
            displayPath(aStarPath, listOfLists)
            goalFound =1
            return

        for j in range(len(fringe)):
            if fringe[j] == current:
                del fringe[j]
                break
        visitedNodes.append(current)

        #Get the branching Nodes,
        with open("road-segments.txt", "r") as ins:
            startNode = []
            branchNodes = []
            length = []
            speedlimit = []
            namehighway = []
            for line in ins:
               # print("TEST:", line)
                splitvalue = line.split(' ')
                if current in splitvalue[0]:
                    startNode.append(splitvalue[0])
                    branchNodes.append(splitvalue[1])
                    length.append(splitvalue[2])
                    speedlimit.append(splitvalue[3])
                    namehighway.append(splitvalue[4])
                    listOfLists.append(splitvalue)
            #print(current,"    :",branchNodes)

        value =[]
        for nextNode in branchNodes:
            if nextNode in visitedNodes:
                continue
            if(routingOption == 'distance'):
                value = length
            elif(routingOption == 'time'):
                for i in range(len(speedlimit)):
                    value.append(round((int(length[i])/int(speedlimit[i])),4))

            if(routingOption == 'distance' or routingOption == 'time'):
                tentativeGValue = gValue[current] + float(distanceCalculator(current,nextNode,startNode,branchNodes,value))

            if(routingOption == 'segments'):
                tentativeGValue = gValue[current] + 1

            if nextNode not in fringe:
                parent[nextNode] = current
                gValue[nextNode] = tentativeGValue
                fValue[nextNode] = gValue[nextNode] + heuristic_cost_estimate(nextNode, endCity)
                if nextNode not in fringe:
                    fringe.append(nextNode)
    if(goalFound ==0):
        print("No Path from start state and end state")
    return False
    #end

# Output Display Function
def displayPath(aStartPath, listOfLists):
    totalDistance =0
    totalTime =0
    #aStartPath.reverse()    print("\nDRIVING DIRECTIONS from ",startCity, " to ", endCity,":")
    for k in range(len(aStartPath)):
        for list in listOfLists:
            if list[0] == aStartPath[k] and list[1] == aStartPath[k+1]:
                print("\nTake Highway - ",list[4].rstrip("\n"),"- from ", aStartPath[k]," to ", aStartPath[k+1]," time: ", round((int(list[2])/int(list[3])),4),"hrs Distance: ",list[2], "miles")
                totalDistance = totalDistance + int(list[2])
                totalTime = totalTime + float(int(list[2])/int(list[3]))
                break

    print("\n",totalDistance," ",totalTime," ", aStartPath)

if __name__ == "__main__":

    # Getting input arguments for start City , End City , Routing Option and Routing Algorithm
    if len(sys.argv) == 5:
        startCity     = sys.argv[1]
        endCity       = sys.argv[2]
        routingOption = sys.argv[3]
        routingAlgo   = sys.argv[4]
    else:
        print("\n ERROR : Missing the input argument(s)\n\n************ USABILITY ************")
        print("python routingPath.py [start-city] [end-city] [routing-option] [routing-algorithm] ")
        sys.exit();

    print("\n****** INPUT ARGUMENTS *********\n\nStartCity: ", startCity, "\nEndCity: ", endCity,"\nRoutingOption: ",routingOption, "\nRoutingAlgo: ",routingAlgo)

    #Make the function call based on the routing algorithm
    if routingAlgo == 'bfs':
        bfsSearch()
    elif routingAlgo == 'dfs':
       getRoute(startCity,endCity,routingOption)
    elif routingAlgo == 'astar':
        astarSearch(startCity,endCity)






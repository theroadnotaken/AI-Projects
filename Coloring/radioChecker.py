import sys
import os

                                        ### Please NOTE that this program will have to be run in python3 only ###
                                                         ###### run in PYTHON3 only ########

# Radio Frequency Assignment Validation Program
# AUTHOR        :   srkanuri (Srikanth Kanuri)

class cspNode:
    node = ''
    assFreq = []
    adjStates = []


class cspGraph:
    graph = dict()
    checkStates = []
    freq = ['A', 'B', 'C', 'D']
    backtrackCnt = 0
    prevNode = ''

    # Constructor loads the Adj States file to class and also assigns the legacy constraints to the graph
    def __init__(self):
        for checkLine in open('adjacent-states','r'):
            children = checkLine.split()
            child = cspNode()
            child.node = children[0]
            child.assFreq = self.freq
            child.adjStates = [i for i in children if i != child.node]
            self.graph[child.node] = child

    #Backtracking search Algorithm
    def backtrackingSearch(self):
        display('List Length '+str(len([nodeList for nodeList in self.graph if len(self.graph[nodeList].assFreq) != 1])))
        if len([nodeList for nodeList in self.graph if len(self.graph[nodeList].assFreq) != 1]) == 0:
            return True
        else:
            acc = []
            maxcvar = 0
            maxcvarVals = []
            maxconsvar = 0
            maxconsvarVals = []
            finalNode = ''
            selectedFreq = ''
            if self.prevNode != '' and len([adjs for adjs in self.graph[self.prevNode].adjStates if len(self.graph[adjs].assFreq) > 1]) > 0:
                acc = [self.graph[nodeList] for nodeList in self.graph[self.prevNode].adjStates if len(self.graph[nodeList].assFreq) != 1]
            else:
                acc = [self.graph[nodeList] for nodeList in self.graph if len(self.graph[nodeList].assFreq) != 1]
            maxcvar = min([len(ac.assFreq) for ac in acc])
            display('Max constrained Variable length is :'+str(maxcvar))
            maxcvarVals = [ac for ac in acc if len(ac.assFreq) == maxcvar]
            display('Nodes for Max constrained Variable :'+str(maxcvarVals))
            if len(maxcvarVals) >= 1:
                maxconsvar = max([len(m2.adjStates) for m2 in maxcvarVals])
                display('Max constraining Variable length is :'+str(maxconsvar))
                maxconsvarVals = [m2 for m2 in maxcvarVals if len(m2.adjStates) == maxconsvar]
                display('Nodes for Max constraining Variable :'+str(maxconsvarVals))
                if len(maxconsvarVals) >= 1:
                    cnt = 0
                    for i in maxconsvarVals[0].assFreq:
                        val = self.checkConsistency(maxconsvarVals[0].node, i)
                        if val == 'T':
                            selectedFreq = i
                            finalNode = maxconsvarVals[0].node
                            tempFreq = self.graph[finalNode].assFreq
                            self.graph[finalNode].assFreq = list(selectedFreq)
                            self.prevNode = finalNode
                            result = self.backtrackingSearch()
                            if result != False:
                                return self.arcConsistent(finalNode, selectedFreq)
                                #[self.graph[n].assFreq.remove(selectedFreq) for n in self.graph[finalNode].adjStates if self.graph[n].assFreq.count(selectedFreq) != 0]
                            else:
                                self.graph[finalNode].assFreq = tempFreq
                                self.backtrackCnt+=1
                        elif val == 'E':
                            display('Error encountered')
                        else:
                            display(i+' already present in neighbours')
                            cnt+=1
                    return False
            else:
                display('Error in finding the node with max constrained variable '+maxcvarVals)

    #Check the consistency of node asignment w.r.t its adjacent nodes
    def checkConsistency(self, node, assignment):
        for neighbour in self.graph[node].adjStates:
            display('Current Node :'+node)
            display('Neighbour :'+neighbour)
            display('Assignment :'+assignment)
            if len(self.graph[neighbour].assFreq) == 0:
                return 'E'
            elif len(self.graph[neighbour].assFreq) == 1:
                if assignment == self.graph[neighbour].assFreq[0]:
                    return 'F'
        return 'T'

    #Arc Consistency Algorithm
    def arcConsistent(self, node, selectedFreq):
        changeList = []
        for n in self.graph[node].adjStates:
            if self.graph[n].assFreq.count(selectedFreq) == 1:
                self.graph[n].assFreq.remove(selectedFreq)
                changeList.append(n)
                if len(self.graph[n].assFreq) == 1:
                    res = self.arcConsistent(self.graph[n].node, self.graph[n].assFreq[0])
                    if res == False:
                        for cl in changeList:
                            self.graph[n].assFreq.append(selectedFreq)
                        return False
                    else:
                        return True
                if len(self.graph[n].assFreq) == 0:
                    return False
        return True

    #Load Results data to Graph for validation
    def loadResults(self):
        prev = 0
        cnt = 1
        for valLine in open(resFileName,"r"):
            if cnt == prev+1:
                if len(valLine) == 1:
                    prev = cnt
                else:
                    val = valLine.split()
                    if len(val) > 2:
                        print('Unwanted Values present for '+val[0])
                        sys.exit(0)
                    self.graph[val[0]].assFreq = list(val[1])
                    prev = cnt
                    cnt+=1
            else:
                break

#Log Writer
def display(lstring):
    #print(lstring)
	pass


#Main driver for the program
if __name__ == "__main__":
    if len(sys.argv) == 3:
        resFileName = sys.argv[1]
        lcFileName = sys.argv[2]
    else:
        print('\nError in input of radioChecker.py >> Wrong format for Input Arguments:')
        print('Correct format: python3 radioChecker.py <results_file> <legacy_constraint_file>\n')
        sys.exit();


#resFileName = 'results.txt'
#lcFileName = 'legacy-constraints-3'
valFlag = 'Y'
validater = cspGraph()
validater.loadResults()
for legacyLine in open(lcFileName,"r"):
    if legacyLine.strip() != '':
        legacyData = legacyLine.split()
        if( validater.graph[legacyData[0]].assFreq != list(legacyData[1])):
            print('Validation failed in Legacy data constraints for '+str(validater.graph[legacyData[0]].node))
            sys.exit(0)
            #self.arcConsistent(legacyData[0], legacyData[1])
for i in validater.graph:
    if len(validater.graph[i].assFreq) > 1:
        valFlag = 'N'
        break
    result = validater.checkConsistency(validater.graph[i].node, validater.graph[i].assFreq[0])
    if result != 'T':
        print('Validation failed in adjacency check for '+str(validater.graph[i].node))
        valFlag = 'N'
        break
if valFlag == 'N':
    print('Output file Wrong')
else:
    print('Output file Validated')

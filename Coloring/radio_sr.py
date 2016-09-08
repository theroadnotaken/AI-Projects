import sys
import os

# Radio Frequency Assignment Program
# AUTHOR        :   srkanuri (Srikanth Kanuri)
# DESCRIPTION   :   The program assigns the radio frequencies [A, B, C, D] to all the states in USA so that no 2 adjacent states have the same frequency.
#                   We also have a few states which have legacy devices and can only support a particular frequency.
#
# APPROACH      :   I have used the following algorithms for the following categories
#                   CSP         -> Backtracking Search
#                   Filtering   -> Arc Consistency
#                   Ordering    -> Most Constrained Variable, Most Constraining Variable and Least Constraining Value
#
#                   I have used a class cspNode to model each state and cspGraph class to model the complete graph. I loaded the complete file into the graph
#                   dictionary of cspNode in cspGraph class. Each node can be referenced with the state name. Initially each state will have all the frequencies
#                   assigned. The final frequency will be achieved after a set computations performed using the above metioned algorithms.
#
# SOLUTION      :   Before the backtracking search could start, the legacy constraint values are assigned. When the backtracking starts, the value which has the
#                   least number of frequencies > 1 is considered (Most Constrained Variable). If there are multiple states, the states having the maximum number of
#                   neighbours are considered. Once a specific state is selected, the least constrained value is selected and assigned. Once assigned, we check the
#                   consistency of the graph for that node and then invoke the Arc Consistency filtering algorithm for it. Arc Consistency removes the obvious
#                   unwanted values from the neighbours and propogates the same forward. The same is continued until all the frequencies are reduced.
#
# MISC          :   The Backtracking count is calculated and output to the results.txt file along with the final list of states with frequencies.
#                   Once the final output is generated, it is validated by another method and the output is prompted to the user.
#
# PROBLEMS      :   (i)  Initially the bactracking was going into an infitine loop of backtracks and was not giving an output. But once all the heuristics were
#                        coded in this issues were sorted out.
#                   (ii) Even though the I have implemented backtracking search with Filtering (Forward Checking) and Ordering Techniques, there was heavy amount
#                        of backtracking happening and the program took a good amount of time to complete. I have then implemented Arc Consistency and also added
#                        an additional constraint to give priority to neighbours before looking outside. These tweaks reduced the backtracking factor to a great
#                        extent.
#
# ANALYSIS      :   The program worked really well after implementing all the heuristics and algorithms particularly the Arc Consistency. The program runs reduced
#                   from 20-30 seconds to 1 second which is a great reduction. The program keeps all the data in the graph and doesnt fetch the values from data file
#                   repeatedly. It uses a class for the implementation and hence there is no need to carry around variable for each call is a great model for
#                   implementing this problem. There is an additional file used to store the log of the program run which can be used to debug the program run.
#                   Once the output is generated, I have also included a validator which validates the output with reference to the state adjacecny and give the output
#                   to the user. This reduces the work to validate all the state assignment manually.

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
    outputFileName = 'results.txt'

    # Constructor loads the Adj States file to class and also assigns the legacy constraints to the graph
    def __init__(self):
        for checkLine in open('adjacent-states','r'):
            children = checkLine.split()
            child = cspNode()
            child.node = children[0]
            child.assFreq = self.freq
            child.adjStates = [i for i in children if i != child.node]
            self.graph[child.node] = child
        for legacyLine in open(lcFileName,"r"):
            if legacyLine.strip() != '':
                legacyData = legacyLine.split()
                self.graph[legacyData[0]].assFreq = list(legacyData[1])
                #self.arcConsistent(legacyData[0], legacyData[1])

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
        for valLine in open(self.outputFileName,"r"):
            if cnt == prev+1:
                if len(valLine) == 1:
                    prev = cnt
                else:
                    val = valLine.split()
                    self.graph[val[0]].assFreq = list(val[1])
                    prev = cnt
                    cnt+=1
            else:
                break

#Log Writer
def display(lstring):
    log.write(lstring)


#Main driver for the program
if __name__ == "__main__":
    if len(sys.argv) == 2:
        lcFileName = sys.argv[1]
    else:
        print('\nError in input of radio.py >> Wrong format for Input Arguments:')
        print('Correct format: python3 radio.py <legacy_constraint_file>\n')
        sys.exit();
#lcFileName = 'legacy-constraints-3'
log = open('radioLog.log','w')
bts = cspGraph()
bts.backtrackingSearch()
f = open(bts.outputFileName, 'w')
for x in [str(bts.graph[nodes].node)+' '+str(bts.graph[nodes].assFreq[0]) for nodes in bts.graph if len(bts.graph[nodes].assFreq) == 1]:
    f.write(x+'\n')
f.write('\nNumber of backtracks: '+str(bts.backtrackCnt))
f.close()


valFlag = 'Y'
validater = cspGraph()
validater.loadResults()
for i in validater.graph:
    if len(validater.graph[i].assFreq) > 1:
        valFlag = 'N'
        break
    result = validater.checkConsistency(validater.graph[i].node, validater.graph[i].assFreq[0])
    if result != 'T':
        display('Validation failed for '+str(validater.graph[i].node))
        valFlag = 'N'
        break
if valFlag == 'N':
    print('Output file Wrong')
else:
    print('Output file Validated')
log.close()

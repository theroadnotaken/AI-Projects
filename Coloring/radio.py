__author__ = 'USER'
from collections import defaultdict
import sys
from copy import deepcopy
import time
# 1) FORMULATION OF PROBLEM: (Backtracking and forward checking)

# a) Initialize the dictionaries:

#    -state_freq -> State name as keyword and number of frequencies legally possible as values
#    -state_neighbour -> State name as keyword and number of neighbouring states as values
#    -state_freq_temp -> empty type list dictionary
#    -allocated -> dictionary with states as key and assigned frequency as value

# b) Backtracking function:

#    - Check if the length of allocated is equal to the total number of variables i.e 50
#    - if yes return allocated
#    - pickup a variable using heuristics minimum remaining values MRV and variable with max neighbours
#    - for each frequency in the state selected check the consistency using least constraining value heuristics
#    - add the state, frequency to allocated dictionary
#    - (Forward Checking used)Remove the selected freq from the neighbouring states from state_freq dictionary
#    - Assign the selected freq to the selected state in state_freq dictionary
#    - backtrack with the current allocated dictionary
#    - if backtrack is not false return result
#    - if value is inconsistent remove the state from allocated and reassign the original value to state in dictionary
#    - reassign the previous values to the neighbouring states
#    - return false

# c) fetch state function:

#    - returns variable with least domain
#    - if domain len is same returns variable with maximum neighbours

# d) lcv function:

#    -if corresponding neighbour has a one domain value and the value is same as selected frequency then declare
#     variable as inconsistent

# References: Backtracking algorithm referred from lect slides
start = time.time()
allocated = {}
count_backtracks = 0


def fetch_state():
    #minimum remaining values state
    new_dict = defaultdict(list)
    new_dict = state_freq.copy()
    for i in new_dict.keys():
        if i in allocated.keys() or i == '':
            del new_dict[i]
    mrv = min(new_dict.keys(), key=lambda k: len(new_dict[k]))
    same_len_domains = []
    for j in new_dict.keys():
        if len(new_dict[mrv]) == len(new_dict[j]):
            same_len_domains.append(j)
    max_count = 0
    for k in state_neighbour.keys():
        for m in same_len_domains:
            if k == m and max_count <= len(state_neighbour[k]):
                max_neigh = m
                max_count = len(state_neighbour[k])

    return max_neigh


def lcv(variable, value):
    for n in state_neighbour[variable]:
        if len(state_freq[n]) == 1:
            neigh = state_freq[n][0]
            if neigh == value:
                return False
    return True


def backtracking(allocated):
    if len(allocated.keys()) == len(states):
        return allocated
    mrv = fetch_state()
    if mrv in state_freq.keys():
        domain = state_freq.get(mrv)
    for frequency in domain:
        if lcv(mrv, frequency):
            allocated[mrv] = frequency
            #print len(allocated)
            #print(mrv, ":", frequency)
            neigh3 = deepcopy(state_neighbour[mrv])
            for z in neigh3:
                dom3 = deepcopy(state_freq[z])
                if frequency in dom3:
                    dom3.remove(frequency)
                state_freq[z] = deepcopy(dom3)
            backup =[]
            backup = deepcopy(state_freq[mrv])
            state_freq_temp[mrv] = deepcopy(backup)
            state_freq[mrv] = [frequency]
            result = backtracking(allocated)
            if result is not None:
                    return result
            for y in neigh3:
                dom3 = deepcopy(state_freq[z])
                if frequency not in dom3:
                    dom3.append(frequency)
                state_freq[z] = deepcopy(dom3)
            dom = deepcopy(state_freq_temp[mrv])
            dom.remove(frequency)
            state_freq[mrv] = dom
            del allocated[mrv]
            count_backtracks = count_backtracks + 1
    return None

if __name__ == "__main__":

    # Getting input arguments for legacy constraints file
    if len(sys.argv) == 2:
        legacyConstraint = sys.argv[1]
    else:
        print "\n\n Input Argument missing : Legacy Constraint File is missing "
        sys.exit()

    freq = ['A', 'B', 'C', 'D']
    document = open('adjacent-states', 'r')
    line = document.readline()
    state_neighbour = defaultdict(list)
    state_freq = defaultdict(list)
    states = []
    while line:
        splitarray = line.split(' ')
        states.append(splitarray[0].strip('\n'))
        state_freq[splitarray[0].strip('\n')] = freq
        temp = []
        for i in splitarray[1:]:
            temp.append(i.strip('\n'))
        state_neighbour[splitarray[0].strip('\n')] = temp
        line = document.readline()
    document.close()

    doc = open(legacyConstraint,'r')
    line1 = doc.readline()
    while line1.strip():
	print 'In Loop '+line1
        splitarray1 = line1.split(' ')
        if splitarray1[0].strip('\n') in state_freq.keys():
	    print 'In If '+splitarray1[0].strip('\n')
            state_freq[splitarray1[0].strip('\n')] = [splitarray1[1].strip('\n')]
            line1 = doc.readline()
    doc.close()
    state_freq_temp = defaultdict(list)
    allocated = defaultdict(str)
    answer = backtracking(allocated)

    print "\nNumber of Backtracks: ",count_backtracks


    #print len(allocated)

    f = open('results.txt', 'w')

    for i in allocated.keys():
        f.write(i), f.write(" "), f.write(allocated[i]), f.write("\n")

    f.close()
end = time.time()
print end - start
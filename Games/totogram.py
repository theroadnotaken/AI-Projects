import math
import sys
from queue import Queue


class totoNode:

    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val
        self.parent = None
        self.dist = 0


class totoRootNode:

    def __init__(self, val):
        self.left = None
        self.center = None
        self.right = None
        self.value = val
        self.dist = 0


def calcNodesFromLvl(level):
    return (3 * ((2**(int(level) - 1)) - 1)) + 1


def setTotogram(level):
    totNodes = calcNodesFromLvl(level)
    #print("Total Nodes in the list are " + str(totNodes))
    rootNode = int(totNodes / 2)
    root = totoRootNode(rootNode)
    #print("Root Node " + str(rootNode))
    segmentSize = int((totNodes - 1) / 3)
    loadDictionary(root, totNodes)
    root.left = getPreOrderTree(1, segmentSize)
    root.left.parent = root
    root.left.dist = abs(root.value - root.left.value)
    root.center = getInOrderTree(segmentSize + 1, rootNode, (2 * segmentSize) + 1)
    root.center.parent = root
    root.center.dist = abs(root.value - root.center.value)
    root.right = getPostOrderTree((2 * segmentSize) + 2, totNodes)
    root.right.parent = root
    root.right.dist = abs(root.value - root.right.value)
    #print("Dict "+str(treeDict))
    # print(str(treeDict[rootNode].left)+""+str(treeDict[rootNode].center)+""+str(treeDict[rootNode].value)+""+str(treeDict[rootNode].right))
    return root


def loadDictionary(root, totalNodes):
    for i in range(1, totalNodes + 1):
        if i == root.value:
            treeDict[i] = root
        else:
            treeDict[i] = totoNode(i)


def getPreOrderTree(preStart, preEnd):
    #print("Pre Order Start is " + str(preStart) + " and End is " + str(preEnd))
    nodeMid = int((preEnd - preStart) / 2)
    treeDict[preEnd] = totoNode(preEnd)
    if (preEnd - nodeMid - 1) == preStart:
        treeDict[preStart] = totoNode(preStart)
        treeDict[preEnd - 1] = totoNode(preEnd - 1)
        treeDict[preEnd].left = treeDict[preStart]
        treeDict[preEnd].right = treeDict[preEnd - 1]
    else:
        treeDict[preEnd].left = getPreOrderTree(preStart, (preEnd - nodeMid - 1))
        treeDict[preEnd].right = getPreOrderTree((preEnd - nodeMid), preEnd - 1)
    treeDict[preEnd].left.parent = treeDict[preEnd]
    treeDict[preEnd].left.dist = abs(treeDict[preEnd].value - treeDict[preEnd].left.value)
    treeDict[preEnd].right.parent = treeDict[preEnd]
    treeDict[preEnd].right.dist = abs(treeDict[preEnd].value - treeDict[preEnd].right.value)
    return treeDict[preEnd]


def getInOrderTree(inStart, rootNode, inEnd):
    #print("In Order Start is " + str(inStart) + " and End is " + str(inEnd))
    treeDict[rootNode + 1] = totoNode(rootNode + 1)
    if (math.floor((inEnd + inStart) / 2) == rootNode) and (inEnd - inStart - 1) > 3:
        treeDict[rootNode + 1].left = getPreOrderTree(inStart, rootNode - 1)
        treeDict[rootNode + 1].right = getPostOrderTree(rootNode + 2, inEnd)
    elif (inEnd - inStart - 1) <= 3:
    	treeDict[inStart] = totoNode(inStart)
    	treeDict[inEnd] = totoNode(inEnd)
    	treeDict[rootNode + 1].left = treeDict[inStart]
    	treeDict[rootNode + 1].right = treeDict[inEnd]
    else:
        print("Something went Wrong! ....")
        print("Oops I forgot ... get your coding right")
        return None
    treeDict[rootNode + 1].left.parent = treeDict[rootNode + 1]
    treeDict[rootNode + 1].left.dist = abs(treeDict[rootNode + 1].value - treeDict[rootNode + 1].left.value)
    treeDict[rootNode + 1].right.parent = treeDict[rootNode + 1]
    treeDict[rootNode + 1].right.dist = abs(treeDict[rootNode + 1].value - treeDict[rootNode + 1].right.value)
    return treeDict[rootNode + 1]


def getPostOrderTree(postStart, postEnd):
    #print("Post Order Start is " + str(postStart) +" and End is " + str(postEnd))
    nodeMid = int((postEnd - postStart) / 2)
    treeDict[postStart] = totoNode(postStart)
    if (postStart + nodeMid + 1) == postEnd:
        treeDict[postStart + 1] = totoNode(postStart + 1)
        treeDict[postEnd] = totoNode(postEnd)
        treeDict[postStart].left = treeDict[postStart + 1]
        treeDict[postStart].right = treeDict[postEnd]
    else:
        treeDict[postStart].left = getPostOrderTree(postStart + 1, (postStart + nodeMid))
        treeDict[postStart].right = getPostOrderTree((postStart + nodeMid + 1), postEnd)
    treeDict[postStart].left.parent = treeDict[postStart]
    treeDict[postStart].left.dist = abs(treeDict[postStart].value - treeDict[postStart].left.value)
    treeDict[postStart].right.parent = treeDict[postStart]
    treeDict[postStart].right.dist = abs(treeDict[postStart].value - treeDict[postStart].right.value)
    return treeDict[postStart]


def displayResult():
        #print(str(root.value)+" Displaying result function "+str(lvl))
    lvl = trDist
    ls = list()
    totNodes = calcNodesFromLvl(lvl)
    try:
        q = Queue(totNodes)
        q.put(root.left)
        q.put(root.center)
        q.put(root.right)
        # print(q.qsize())
        ls.append(root.value)
        while not q.empty():
            node = q.get()
            # print(q.qsize())
            ls.append(node.value)
            if node.left is not None:
                q.put(node.left)
            #print("left "+str(q.qsize()))
            if node.right is not None:
                q.put(node.right)
            #print("right "+str(q.qsize()))
        print(ls)
    except Exception as ex:
        print("Exception encountered :" + str(ex))


def getDistance():
	dist = 0
	for i in treeDict:
		if treeDict[i].dist > dist:
			dist = treeDict[i].dist
		#print(str(i) + " Node distance " + str(treeDict[i].dist))
	return dist


def checkAlternative(node):
	nodeDist = abs(node.value - node.parent.value)
	selNode = node.value
	#print(str(selNode)+" Node - Dist "+str(nodeDist))
	if node.value > node.parent.value:
		val1 = node.parent.value
		val2 = node.value
	else:
		val1 = node.value
		val2 = node.parent.value
	#print("Val1 is "+str(val1)+" Val2 is "+str(val2))
	for i in range(val1+1, val2):
		if i != root.value:
			otherNodeDist = abs(treeDict[i].value - treeDict[i].parent.value)
			#print("i value is "+str(i))
			#(abs(node.value - treeDict[i].parent.value) <= otherNodeDist) and .value) < trDist):
			#print(abs(treeDict[i].value - node.value))
			#print(nodeDist)
			if (abs(treeDict[i].value - node.value) < nodeDist) and treeDict[i].parent != node.parent:
				#print("Inside Loop i value is "+str(i))
				if node is not None or (abs(treeDict[i].value - node.left.value) <= initialDist and abs(treeDict[i].value - node.right.value) <= initialDist):
					nodeDist = abs(treeDict[i].value - node.value)
					selNode = i
				elif treeDict[i].left is None:
					nodeDist = abs(treeDict[i].value - node.value)
					selNode = i
				#elif childSafe == 'N':
					#nodeDist = abs(treeDict[i].value - node.parent.value)
					#selNode = i
	if (selNode != node.value) and (treeDict[selNode].parent != node.parent):
		#print(str(treeDict[selNode].value)+" Value for "+str(node.value))
		tempLeft = treeDict[selNode].left
		tempRight = treeDict[selNode].right
		tempParent = treeDict[selNode].parent
		treeDict[selNode].left = node.left
		treeDict[selNode].right = node.right
		treeDict[selNode].parent = node.parent
		node.left = tempLeft
		node.right = tempRight
		node.parent = tempParent

		if treeDict[selNode].parent.left == node:
			treeDict[selNode].parent.left = treeDict[selNode]
		elif treeDict[selNode].parent.right == node:
			treeDict[selNode].parent.right = treeDict[selNode]
		else:
			treeDict[selNode].parent.center = treeDict[selNode]

		treeDict[selNode].dist = abs(treeDict[selNode].value - treeDict[selNode].parent.value)

		if treeDict[selNode].left is not None:
			treeDict[selNode].left.parent = treeDict[selNode]
			treeDict[selNode].left.dist = abs(treeDict[selNode].left.value - treeDict[selNode].value)
		if treeDict[selNode].right is not None:
			treeDict[selNode].right.parent = treeDict[selNode]
			treeDict[selNode].right.dist = abs(treeDict[selNode].right.value - treeDict[selNode].value)

		if node.parent.left == treeDict[selNode]:
			node.parent.left = node
		elif node.parent.right == treeDict[selNode]:
			node.parent.right = node
		else:
			node.parent.center = node

		node.dist = abs(node.value - node.parent.value)

		if node.left is not None:
			node.left.parent = node
			node.left.dist = abs(node.left.value - node.value)
		if node.right is not None:
			node.right.parent = node
			node.right.dist = abs(node.right.value - node.value)

		#print("The old node Config is "+str(node.value))
		#print("The new node Config is "+str(selNode))


def reduceDistance(chkValue):
	cnt = 0
	for i in treeDict:
		if (treeDict[i].dist >= chkValue) and (treeDict[i] != root) and cnt < calcNodesFromLvl(trDist):
			#print(str(treeDict[i].value)+" Parent "+str(treeDict[i].parent.value)+" Distance "+str(treeDict[i].dist))
			checkAlternative(treeDict[i])
			cnt+=1
			#print(getDistance())
			#displayResult()

def mainreducer():
	cntr = 0
	chkValue = initialDist
	while getDistance() >= chkValue  and cntr < calcNodesFromLvl(trDist):
		reduceDistance(chkValue)
		cntr+=1


if __name__ == "__main__":
	if len(sys.argv) == 2:
		trDist     = sys.argv[1]
	else:
		print("\n ERROR : Missing the input argument(s)\n\n************ USABILITY ************")
		print("python3 totogram.py [level]")
		sys.exit();
	treeDict = {}
	root = setTotogram(trDist)
	initialDist = getDistance()
	while getDistance() == initialDist:
		treeDict = {}
		root = setTotogram(trDist)
		mainreducer()
		initialDist-=1
	treeDict = {}
	root = setTotogram(trDist)
	initialDist = initialDist+2
	mainreducer()
	print(getDistance())
	displayResult()

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
						acc.append([children[0],children[1],children[2],int(children[3])/int(children[2]),children[4]])
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
			totTime+= int(round(desc[3],4))
			if param == 'segments':
				print("Take Highway "+desc[4]+" from "+desc[0]+" to "+desc[1])
			if param == 'distance':
				print("Take Highway "+desc[4]+" from "+desc[0]+" to "+desc[1]+" for "+str(desc[2])+" miles")
			if param == 'time':
				print("Take Highway "+desc[4]+" from "+desc[0]+" to "+desc[1]+" for "+str(round(int(desc[3]),4))+" hours")
		finalPath.append(endCity)
		print(str(totDist)+" "+str(round(totTime,4))+" "+str(finalPath))


getRoute('Austin,_Texas','Windcrest,_Texas','distance')

import itertools

'''
# This program finds the items ordered by people based on the conditions provided in the problem statement. None of the 

APPROACH:
We have considered the all the permutations of (person,ordered item,place) in the given problem statement. For each configuration generated, 
we applied the conditions provided in the problem statement to generate the received list. If there are multiple items received for the same person, 
the whole configurtion is rejected and we get move on to a new configuration.
'''
def findAmazonParrotOrders():
	totCnt = 0
	succCnt = 0
	person = ['F','G','H','I','J']
	order = ['A','B','C','D','E']
	place = ['K','L','M','N','O']
	valueDict = {'A':'Amplifer',
				 'B':'Banister',
				 'C':'Candelabrum',
				 'D':'Doorknob',
				 'E':'Elephant',
				 'F':'Frank',
				 'G':'George',
				 'H':'Heather',
				 'I':'Irene',
				 'J':'Jerry',
				 'K':'Kirkwood Street',
				 'L':'Lake Avenue',
				 'M':'Maxwell Street',
				 'N':'North Avenue',
				 'O':'Orange Drive'}
	for orderCombo in itertools.permutations(order):
		for placeCombo in itertools.permutations(place):
			totCnt+= 1
			receive = ['0','0','0','0','0']
			valFlag = True
			#Validation and Received Prediction
			#1) The customer who ordered the Candelabrum received the Banister
			if ((receive[orderCombo.index('C')] == '0') or (receive[orderCombo.index('C')] == 'B')) and (valFlag == True):
				receive[orderCombo.index('C')] = 'B'
			else:
				valFlag = False

			#2) The customer who ordered the Banister received the package that Irene had ordered
			if ((receive[orderCombo.index('B')] == '0') or (receive[orderCombo.index('B')] == orderCombo[person.index('I')])) and (valFlag == True):
				receive[orderCombo.index('B')] = orderCombo[person.index('I')]
			else:
				valFlag = False

			#3) Frank received a Doorknob
			if ((receive[person.index('F')] == '0') or (receive[person.index('F')] == 'D')) and (valFlag == True):
				receive[person.index('F')] = 'D'
			else:
				valFlag = False

			#4) George’s package went to Kirkwood Street
			if ((receive[placeCombo.index('K')] == '0') or (receive[placeCombo.index('K')] == orderCombo[person.index('G')])) and (valFlag == True):
				receive[placeCombo.index('K')] = orderCombo[person.index('G')]
			else:
				valFlag = False

			#5) The delivery that should have gone to Kirkwood Street was sent to Lake Avenue
			if ((receive[placeCombo.index('L')] == '0') or (receive[placeCombo.index('L')] == orderCombo[placeCombo.index('K')])) and (valFlag == True):
				receive[placeCombo.index('L')] = orderCombo[placeCombo.index('K')]
			else:
				valFlag = False

			#6) Heather received the package that was to go to Orange Drive
			if ((receive[person.index('H')] == '0') or (receive[person.index('H')] == orderCombo[placeCombo.index('O')])) and (valFlag == True):
				receive[person.index('H')] = orderCombo[placeCombo.index('O')]
			else:
				valFlag = False

			#7) Jerry received Heather’s order
			if ((receive[person.index('J')] == '0') or (receive[person.index('J')] == orderCombo[person.index('H')])) and (valFlag == True):
				receive[person.index('J')] = orderCombo[person.index('H')]
			else:
				valFlag = False

			#8) The Elephant arrived in North Avenue
			if ((receive[placeCombo.index('N')] == '0') or (receive[placeCombo.index('N')] == 'E')) and (valFlag == True):
				receive[placeCombo.index('N')] = 'E'
			else:
				valFlag = False

			#9) The person who had ordered Elephant received the package that should have gone to Maxwell Street
			if ((receive[orderCombo.index('E')] == '0') or (receive[orderCombo.index('E')] == orderCombo[placeCombo.index('M')])) and (valFlag == True):
				receive[orderCombo.index('E')] = orderCombo[placeCombo.index('M')]
			else:
				valFlag = False

			#10) The customer on Maxwell Street received the Amplifier
			if ((receive[placeCombo.index('M')] == '0') or (receive[placeCombo.index('M')] == 'A')) and (valFlag == True):
				receive[placeCombo.index('M')] = 'A'
			else:
				valFlag = False

			if receive[0] == orderCombo[0] or receive[1] == orderCombo[1] or receive[2] == orderCombo[2] or receive[3] == orderCombo[3] or receive[4] == orderCombo[4]:
				valFlag = False

			if valFlag == True:
				succCnt+= 1
				print ('------------------------------------------------------------------')
				print ('Person :'+'{s:{c}<{n}}'.format(s=valueDict[person[0]],n=10,c=' ')+' Ordered :'+'{s:{c}<{n}}'.format(s=valueDict[orderCombo[0]],n=15,c=' ')+' Place :'+'{s:{c}<{n}}'.format(s=valueDict[placeCombo[0]],n=18,c=' ')+' Received :'+'{s:{c}<{n}}'.format(s=valueDict[receive[0]],n=15,c=' '))
				print ('Person :'+'{s:{c}<{n}}'.format(s=valueDict[person[1]],n=10,c=' ')+' Ordered :'+'{s:{c}<{n}}'.format(s=valueDict[orderCombo[1]],n=15,c=' ')+' Place :'+'{s:{c}<{n}}'.format(s=valueDict[placeCombo[1]],n=18,c=' ')+' Received :'+'{s:{c}<{n}}'.format(s=valueDict[receive[1]],n=15,c=' '))
				print ('Person :'+'{s:{c}<{n}}'.format(s=valueDict[person[2]],n=10,c=' ')+' Ordered :'+'{s:{c}<{n}}'.format(s=valueDict[orderCombo[2]],n=15,c=' ')+' Place :'+'{s:{c}<{n}}'.format(s=valueDict[placeCombo[2]],n=18,c=' ')+' Received :'+'{s:{c}<{n}}'.format(s=valueDict[receive[2]],n=15,c=' '))
				print ('Person :'+'{s:{c}<{n}}'.format(s=valueDict[person[3]],n=10,c=' ')+' Ordered :'+'{s:{c}<{n}}'.format(s=valueDict[orderCombo[3]],n=15,c=' ')+' Place :'+'{s:{c}<{n}}'.format(s=valueDict[placeCombo[3]],n=18,c=' ')+' Received :'+'{s:{c}<{n}}'.format(s=valueDict[receive[3]],n=15,c=' '))
				print ('Person :'+'{s:{c}<{n}}'.format(s=valueDict[person[4]],n=10,c=' ')+' Ordered :'+'{s:{c}<{n}}'.format(s=valueDict[orderCombo[4]],n=15,c=' ')+' Place :'+'{s:{c}<{n}}'.format(s=valueDict[placeCombo[4]],n=18,c=' ')+' Received :'+'{s:{c}<{n}}'.format(s=valueDict[receive[4]],n=15,c=' '))
				print ('------------------------------------------------------------------')
	print ('Total Combinations :'+str(totCnt))
	print ('Total Valid Combinations :'+str(succCnt))

findAmazonParrotOrders()

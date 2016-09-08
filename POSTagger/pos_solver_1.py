###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# 1. Learning :
#        The training data is prepared by estimating the conditional probability tables - Prior, Transition and Likelihood:
#
#        P(S1)      - The Prior is calculated by the count of POS at first position by the total POS
#        P(Si+1|Si) - The transition probability is calculated by taking count of the Transition occurence by count
#                         of Si
#        P(Wi|Si)   - The Likelihood probabilty is calculated by count of words as POS by the count of POS
#    2. Naive Inference :
#        Naive Inference is calcualted by the product of the prior and likelihood which are already calculated in training.
#
#    3. Sampling :
#
#        First pick initial sample(POS) : Picked up the initial sample using Naive Bayes , looping through each word in the sentence. Storing probability of all POS.
#        Normalizing teh values in the list and generating another list on the multiples of the POS normalized probabilities.
#        Once the list is built, picking a random value in the list and assigning this value to the picked POS.
#        Repeat the same for all the words  in teh sentence to generate the 1st sample. % samples are displayed as mentioned
####

import random
import math
import copy
from collections import defaultdict

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    priorDict   = {}
    priorDict1 = {}
    totalPOSCount = 0
    POSTagCount = {'adj':0, 'adv':0, 'adp':0, 'conj':0, 'det':0, 'noun':0, 'num':0, 'pron':0, 'prt':0, 'verb':0, 'x':0, '.':0 }
    POSTags     = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
    priorDict = defaultdict(float)
    transCountDict = dict()
    transitionDict = dict()
    likelihoodDict = dict()
    naiveSelection = []
    mcmcSelection = []
    maxSelection = []
    viterbiSelection = []

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        postProd = 1
        for val in [self.likelihoodDict[sentence[i]][label[i]]*self.priorDict[label[i]] if sentence[i] in self.likelihoodDict and label[i] in self.likelihoodDict[sentence[i]] else (1/self.totalPOSCount)*self.priorDict[label[i]] for i in range(0,len(sentence))]:
            postProd*=val
        return math.log10(postProd) if postProd != 0 else 0

    # Do the training!
    #
    def train(self, data):
        for tuple in data:
            # P(S1)
            first = tuple[1][0]
            if first in self.priorDict1:
                self.priorDict1[first] += 1
            else:
                self.priorDict1[first] = 1
            # 1. Prior Processing
            for pos in self.POSTags:
                self.POSTagCount[pos]+=int(str(tuple[1]).count(pos))
            # 2. Likelihood Processing
            for i in range(0, len(tuple[0])):
                dictKey1 = tuple[0][i]
                dictKey2 = tuple[1][i]
                if dictKey1 in self.likelihoodDict:
                    if dictKey2 in self.likelihoodDict[dictKey1]:
                        self.likelihoodDict[dictKey1][dictKey2]+= 1
                    else:
                        self.likelihoodDict[dictKey1][dictKey2] = 1
                else:
                    self.likelihoodDict[dictKey1] = dict()
                    self.likelihoodDict[dictKey1][dictKey2] = 1

        self.totalPOSCount = 0
        for tagCnt in self.POSTagCount.values():
            self.totalPOSCount+= tagCnt

        for firstKeys in self.priorDict1:
            self.priorDict1[firstKeys] = self.priorDict1[firstKeys]/len(data)

        for pos in self.POSTags:
            self.priorDict[pos]  = float(self.POSTagCount[pos]/self.totalPOSCount)

        # Likelihood - P(W|S)
        for wordsLike in self.likelihoodDict:
            for keysLike in self.likelihoodDict[wordsLike]:
                self.likelihoodDict[wordsLike][keysLike] = float(self.likelihoodDict[wordsLike][keysLike]/self.POSTagCount[keysLike])

        # P(Si+1 | Si)
        for pos1 in self.POSTags:
            self.transCountDict[pos1] = dict()
            for pos2 in self.POSTags:
                self.transCountDict[pos1][pos2] = 0

        countSentence = 0
        for row in data:
            countSentence+=1
            for tagIndex in range (1,len(row[1])):
                for pos1 in self.POSTags:
                    for pos2 in self.POSTags:
                        if row[1][tagIndex] == pos1:
                            if row[1][tagIndex-1] == pos2:
                                self.transCountDict[pos1][pos2]+= 1

        for pos1 in self.POSTags:
            self.transitionDict[pos1] = dict()
            for pos2 in self.POSTags:
                self.transitionDict[pos1][pos2] = float(self.transCountDict[pos1][pos2]/self.POSTagCount[pos2])

    # Functions for each algorithm.
    #
    def naive(self, sentence):
        self.naiveSelection = [max(self.likelihoodDict[text], key=lambda i: self.likelihoodDict[text][i]*self.priorDict1[i]) if text in self.likelihoodDict else random.choice(self.POSTags) for text in sentence]
        return [ [ self.naiveSelection ], [] ]

    def mcmc(self, sentence, sample_count):
        samplePOS = copy.deepcopy(self.naiveSelection)
        result = []
        for i in range(0,sample_count): #Sampling passes
            self.sampling(sentence, samplePOS)
            if(i > sample_count-6):
                result.append(samplePOS)
        self.mcmcSelection = samplePOS
        return [ result, [] ]

    def sampling(self, sentence, samplePOS):
        for j in range(0,len(samplePOS)): #Variable picking
            #print(samplePOS)
            sampSelDict = dict()
            currW = sentence[j]
            for pos in self.POSTags:
                if j == 0 and len(samplePOS)>1:
                    nextPOS = samplePOS[j+1]
                    if (currW in self.likelihoodDict) and (nextPOS in self.transitionDict):
                        if (pos in self.likelihoodDict[currW]) and (pos in self.transitionDict[nextPOS]):
                            sampSelDict[pos] = self.likelihoodDict[currW][pos]*self.transitionDict[nextPOS][pos]*self.priorDict1[pos]
                        else:
                            sampSelDict[pos] = 0
                    else:
                        sampSelDict[pos] = self.transitionDict[nextPOS][pos]*self.priorDict1[pos]*(1/self.totalPOSCount)
                elif j == 0 and len(samplePOS) == 1:
                    if currW in self.likelihoodDict:
                        if pos in self.likelihoodDict[currW]:
                            sampSelDict[pos] = self.likelihoodDict[currW][pos]*self.priorDict1[pos]
                        else:
                            sampSelDict[pos] = 0
                    else:
                        sampSelDict[pos] = self.priorDict1[pos]*(1/self.totalPOSCount)
                elif j == len(samplePOS)-1:
                    prevPOS = samplePOS[j-1]
                    if (currW in self.likelihoodDict) and (pos in self.transitionDict):
                        if (pos in self.likelihoodDict[currW]) and (prevPOS in self.transitionDict[pos]):
                            sampSelDict[pos] = self.likelihoodDict[currW][pos]*self.transitionDict[pos][prevPOS]
                        else:
                            sampSelDict[pos] = 0
                    else:
                        sampSelDict[pos] = self.transitionDict[pos][prevPOS]*(1/self.totalPOSCount)
                else:
                    prevPOS = samplePOS[j-1]
                    nextPOS = samplePOS[j+1]
                    if (currW in self.likelihoodDict) and (pos in self.transitionDict) and (nextPOS in self.transitionDict):
                        if (pos in self.likelihoodDict[currW]) and (prevPOS in self.transitionDict[pos]) and (pos in self.transitionDict[nextPOS]):
                            sampSelDict[pos] = self.likelihoodDict[currW][pos]*self.transitionDict[nextPOS][pos]*self.transitionDict[pos][prevPOS]
                        else:
                            sampSelDict[pos] = 0
                    else:
                        sampSelDict[pos] = self.transitionDict[nextPOS][pos]*self.transitionDict[pos][prevPOS]*(1/self.totalPOSCount)
            #dictSum = sum(sampSelDict.values())
            #sampSelDict = {k:v/dictSum if dictSum != 0 else 0 for k, v in sampSelDict.items()}
            maxDictVal = float(0)
            for sampVal in sampSelDict.values():
                if sampVal != 0 and sampVal > maxDictVal:
                    maxDictVal = sampVal
            sampSelDict = {k:round((v/maxDictVal)) if maxDictVal!= 0 else 0 for k, v in sampSelDict.items()}
            [sampSelDict.pop(key,None) for key in [k for k, v in sampSelDict.items() if v == 0]]
            wheelList = []
            if len(sampSelDict) == 1:
                (jkey, jvalue) = sampSelDict.popitem()
                samplePOS[j] = jkey
            else:
                for prob in sampSelDict:
                    if sampSelDict[prob] != 0:
                        [wheelList.append(prob) for itr in range(0, round(sampSelDict[prob]))]
                if len(wheelList) != 0:
                    samplePOS[j] = random.choice(wheelList)
                else:
                    samplePOS[j] = random.choice(self.POSTags)

    def best(self, sentence):
        return [ [ [max([self.naiveSelection[i],self.mcmcSelection[i],self.maxSelection[i]]) for i in range(0, len(sentence))] ], [] ]

    def max_marginal(self, sentence):
        samplePOS = copy.deepcopy(self.mcmcSelection)
        result = {k:{samplePOS[k]:1} for k in range(0,len(samplePOS))}
        for i in range(0,1000): #Sampling passes
            self.sampling(sentence, samplePOS)
            for k in range(0, len(samplePOS)):
                if samplePOS[k] in result[k]:
                    result[k][samplePOS[k]]+=1
                else:
                    result[k][samplePOS[k]]=1
        maxKeys = [max(val, key=lambda i: val[i]) for val in result.values()]
        maxVals = [result[k][maxKeys[k]] for k in range(0, len(result))]
        self.maxSelection = maxKeys
        return [ [ maxKeys ] , [ maxVals ] ]

    def viterbi(self, sentence):
        V = [{}]
        path = {}
        unknownList = []

        # Initialize base cases (t == 0)
        for y in self.POSTags:
           if sentence[0] in self.likelihoodDict:
               if y in self.likelihoodDict[sentence[0]]:
                   #print("\ny = ",y)
                   V[0][y] = self.priorDict1[y] * self.likelihoodDict[sentence[0]][y]
                   path[y] = [y]
               else:
                   #posKey = self.keywithmaxval(self.priorDict)
                   unknownList.append(sentence[0]+y)
                   V[0][y]= float(1/self.totalPOSCount)
                   path[y]=[y]
           else:
               unknownList.append(sentence[0])
               V[0][y]= float(1/self.totalPOSCount)
               path[y]=[y]

        # Run Viterbi for t > 0
        for t in range(1, len(sentence)):
            V.append({})
            newpath = {}

            for y in self.POSTags:
                (prob, state) = (0, 0)
                for y0 in self.POSTags:
                    if y0 in V[t-1] and sentence[t] in self.likelihoodDict and y in self.likelihoodDict[sentence[t]]:
                        tmpProb = V[t-1][y0] * self.transitionDict[y0][y] * self.likelihoodDict[sentence[t]][y]
                        if prob < tmpProb:
                            (prob, state) = (tmpProb, y0)
                    elif y0 in V[t-1]:
                        tmpProb = V[t-1][y0] * self.transitionDict[y0][y] * (1/self.totalPOSCount)
                        if prob < tmpProb:
                            (prob, state) = (tmpProb, y0)
                    else:
                        tmpProb = (1/self.totalPOSCount) * self.transitionDict[y0][y] * self.likelihoodDict[sentence[t]][y]
                        if prob < tmpProb:
                            (prob, state) = (tmpProb, y0)
                    V[t][y] = prob
                    if state in path:
                        newpath[y] = path[state] + [y]
            path = newpath
        n = len(sentence) - 1
        (prob, state) = max((V[n][y] if y in V[n] else 0, y) for y in self.POSTags)
        self.viterbiSelection = path[state]
        return [ [ path[state] ], [] ]

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 20)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print("Unknown algo!")

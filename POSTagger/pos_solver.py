###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids: kolliv(Vandana Kolli) and srkanuri(Srikanth Kanuri)
#
# (Based on skeleton code by D. Crandall)
# (Viterbi pseudocode referred from Wikipedia: https://en.wikipedia.org/wiki/Viterbi_algorithm)
#
# ***************************************************************************************************************************************
# **********  NOTE: PLEASE RUN THE CODE IN PYTHON 3 - INCLUDE PARENTHESIS FOR PRINT STATEMENTS IN POS_SCORER.PY and LABEL.PY  ***********
# ***************************************************************************************************************************************
#
#   1. Learning :
#        The training data is prepared by estimating the conditional probability tables - Prior, Transition and Likelihood:
#
#        P(S1)      - The Prior is calculated by the count of POS at first position by the total POS
#        P(Si+1|Si) - The transition probability is calculated by taking count of the Transition occurence by count
#                         of Si
#        P(Wi|Si)   - The Likelihood probabilty is calculated by count of words as POS by the count of POS
#
#    2. Naive Inference :
#        Naive Inference is calcualted by the product of the prior and likelihood which are already calculated in training.
#        The maximum of this product for all pos is considered and the corresponding pos is output
#
#    3. Sampling :
#        Using Gibbs (MCMC) sampling to sample from the posterior distribution, P(S|W) . Steps are:
#        a. First pick initial sample(POS) : Picked up the initial sample using Naive Bayes ,
#        b. Looping through each word in the sentence.
#        c. Storing probability of all POS.
#        d. Normalizing the values in the list and generating another list on the multiples of the POS normalized probabilities.
#        e. Once the list is built, picking a random value in the list and assigning this value to the picked POS.
#        f. Repeat the same for all the words  in the sentence to generate the 1st sample.
#
#    4. Approximate max-marginal inference:
#        Gibbs MCMC sampling code is used as mentioned in the assignment. 1000 samples are generated.
#        Information from each sample is extracted into a dictionary (incremented at each sampling step) and the once all the samples
#        are generated, the max part of speech occurences are found and is presented as the final sample.
#
#    5. Exact maximum a posteriori inference:
#        Viterbi Algorithm is used to fidn the most likely sequence of state variables.
#
#        a. Initialize base cases :  For the first word, calculate the V[0] values for all states(All POS) which is product
#            of prior and likelihood for all the parts of speech.
#            For y in POSTags:
#                V[0][y] = Prior[y] * likelihood[y][word]
#        b. Run Viterbi for t > 0:
#            For the remaining words loop through them and for all parts of speech calculate the
#            previous value * transition probability * likelihood(emission) probability
#            max((V[t-1][y0] * transition[y0][y] * likelihood[y][obs[t]], y0) for y0 in states)
#
#        c. Pick the maximum probability of the last word for each POS and then traceback the path picking the maximum
#           probability values along the way.
#
#    6. Best:
#        The maximum occurence of a part of speech in all of the algorithms is evaluated as the final part of speech of the best algorithm.
#        The output samples of all the algorithms are saved and used in the best algorithm
#
#    Comments 2:
#    The results of the evaluation on the bc.test file:
#
#    ==> So far scored 2000 sentences with 29442 words.
#                        Words correct:     Sentences correct:
#        0. Ground truth:      100.00%              100.00%
#               1. Naive:       91.76%               37.30%
#             2. Sampler:       94.71%               52.55%
#        3. Max marginal:       94.76%               52.55%
#                 4. MAP:       87.76%               25.30%
#                5. Best:       93.15%               43.95%
#
#    a5_exec_log.txt has been included in Github which is a full log of the execution
#    ----
#
#    Comments 3:
#    1. Unknown words    : For unknown words i.e words which do not appear in training
#    2. Enhancement      : Providing the initital sample to the Gibbs from Step 2: Naive Inference unlike giving it random
#    3. Simplification   : Normalization for Gibbs - Anything smaller than 10 power -2 of maximum probability is being ignored
#                          for faster execution of the program.
#    4. Design decisions : Reusability : Re used teh same code for Gibbs and Max marginal by creating a new function 'sampling'
#
# ***************   NOTE: PLEASE RUN THE CODE IN PYTHON 3 - INCLUDE PARENTHESIS FOR PRINT STATEMENTS IN POS_SCORER.PY and LABEL.PY   *********************


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
    maxSample = 1000
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
            postProd = postProd * val
        return math.log10(postProd) if postProd != 0 else 0

    # Do the training!
    #
    def train(self, data):
        for tuple in data:
            # P(S1)
            first = tuple[1][0]
            if first in self.priorDict1:
                self.priorDict1[first] = self.priorDict1[first] + 1
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
                        self.likelihoodDict[dictKey1][dictKey2] =  self.likelihoodDict[dictKey1][dictKey2] + 1
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
            countSentence = countSentence+1
            for tagIndex in range (1,len(row[1])):
                for pos1 in self.POSTags:
                    for pos2 in self.POSTags:
                        if row[1][tagIndex] == pos1:
                            if row[1][tagIndex-1] == pos2:
                                self.transCountDict[pos1][pos2] = self.transCountDict[pos1][pos2] + 1

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
            sampSelDict = {k:round((v/maxDictVal)*1) if maxDictVal!= 0 else 0 for k, v in sampSelDict.items()}
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
        for i in range(0,self.maxSample-1): #Sampling passes
            self.sampling(sentence, samplePOS)
            for k in range(0, len(samplePOS)):
                if samplePOS[k] in result[k]:
                    result[k][samplePOS[k]] = result[k][samplePOS[k]]+1
                else:
                    result[k][samplePOS[k]]=1
        maxKeys = [max(val, key=lambda i: val[i]) for val in result.values()]
        maxVals = [round(result[k][maxKeys[k]]/self.maxSample, 2) for k in range(0, len(result))]
        self.maxSelection = maxKeys
        return [ [ maxKeys ] , [ maxVals ] ]


    def viterbi(self, sentence):
        V = [{}]
        path = {}
        stateMax=max(self.priorDict1.keys(),key=lambda y:self.priorDict1[y])
        for y in self.POSTags:
          if (sentence[0] in self.likelihoodDict and y in self.likelihoodDict[sentence[0]] ):
              V[0][y] = ((self.priorDict1[y] * self.likelihoodDict[sentence[0]][y]))
              path[y] = [y]
          else :
            V[0][y] =(self.priorDict1[stateMax] * 1/len(self.likelihoodDict))
            path[y] = [stateMax]

        for t in range(1, len(sentence)):
          V.append({})
          newpath = {}

          for y in self.POSTags:
             if sentence[t] in self.likelihoodDict and y in self.likelihoodDict[sentence[t]]:
                (prob, state)=  max((((V[t-1][y0] * self.transitionDict[y0][y] * self.likelihoodDict[sentence[t]][y])),y0) for y0 in self.POSTags)
                V[t][y] = prob
                newpath[y] = path[state] + [y]
             else:
                (prob, state)=max(((V[t-1][y0] *1/len(self.likelihoodDict)*1/len(self.likelihoodDict)) ,y0) for y0 in self.POSTags )
                V[t][y] = prob
                newpath[y] = path[state] + [y]

          path = newpath

        n = len(sentence) - 1
        (prob, state) = max((V[n][y], y) for y in self.POSTags)
        return [ [path[state]], [] ]

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

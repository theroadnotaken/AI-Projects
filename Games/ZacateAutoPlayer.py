# Automatic Zacate game player
# B551 Fall 2015
# Srikanth Kanuri - SRKANURI
#
# Based on skeleton code by D. Crandall
#
# APPROACH
# The program is supposed the play the game Zacate using an optimal algorithm to maximize its mean score
# I have defined 2 functions in this code find_category() and getKeptDice() which gets the best category to
# fit the given conditions
# The program first checks if the dice combination has a potential for special categories.
# If yes, it maps it with the values and sends it back to the calling program.
# If there are no special categories fitting the combination, we can either re-roll the numbers or choose
# a small pattern where it has to potential to make it to the special category.
#
# For the first 2 rolls the program gives back the dice which are to be re-rolled
# For the final roll, the program gives back the suitable category to be selected
# The categories other than "Numbers" are given higher priority as they provide higher chance to win more score
# This program is written in Python 3. Hence I have removes all the print commands to work in python2.7 as well
# The program can be executed by issuing the following command :
#                > python zacate.py
#
# Below is on of the output means achieved:
# Min/max/mean scores: 89 271 179.43
# [Finished in 1.6s]
#
# The main program calls this program three times for each turn.
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list
#      of dice indices that should be re-rolled.
#
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from ZacateState import Dice
from ZacateState import Scorecard
import random
import collections


class ZacateAutoPlayer:
    diceCounts = 0
    reRollHist = []
    def __init__(self):
        reRollHist = []
        diceCounts = 0

    def first_roll(self, dice, scorecard):
        self.reRollHist = self.find_category(dice, scorecard,0)[1]
        return list(set([0,1,2,3,4])-set(self.reRollHist))

    def second_roll(self, dice, scorecard):
        self.reRollHist = self.find_category(dice, scorecard,0)[1]
        return list(set([0,1,2,3,4])-set(self.reRollHist))

    def third_roll(self, dice, scorecard):
        return self.find_category(dice, scorecard,1)[0]

    def find_category(self, dice, scorecard, finalFlag):
        returnCategory = []
        maxScoreCapacity = {"unos": 5, "doses": 10, "treses": 15, "cuatros": 20, "cincos": 25, "seises": 30, "pupusa de queso": 40,"pupusa de frijol": 30, "elote": 25, "triple": 36, "cuadruple": 36, "quintupulo": 36, "tamal": 36}
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        self.diceCounts = [dice.dice.count(i) for i in range(1, 7)]
        valSc = Scorecard()
        [valSc.record(cats, dice) for cats in Scorecard.Categories if cats not in scorecard.scorecard]
        if 5 in self.diceCounts and 'quintupulo' not in scorecard.scorecard:
            returnCategory = ['quintupulo', self.getKeptDice('quintupulo', dice)]
        elif 4 in self.diceCounts and 'cuadruple' not in scorecard.scorecard:
            returnCategory = ['cuadruple', self.getKeptDice('cuadruple', dice)]
        elif 3 in self.diceCounts and 2 in self.diceCounts and 'elote' not in scorecard.scorecard:
            returnCategory = ['elote', self.getKeptDice('elote', dice)]
        elif 3 in self.diceCounts and 'triple' not in scorecard.scorecard:
            returnCategory = ['triple', self.getKeptDice('triple', dice)]
        elif compare((dice.dice), [1, 2, 3, 4, 5]) or compare((dice.dice), [2, 3, 4, 5, 6]) and 'pupusa de queso' not in scorecard.scorecard:
            returnCategory = ['pupusa de queso', self.getKeptDice('pupusa de queso', dice)]
        elif len(set([1, 2, 3, 4]) - set(dice.dice)) == 0 or len(set([2, 3, 4, 5]) - set(dice.dice)) == 0 or len(set([3, 4, 5, 6]) - set(dice.dice)) == 0 and 'pupusa de frijol' not in scorecard.scorecard:
            returnCategory = ['pupusa de frijol', self.getKeptDice('pupusa de frijol', dice)]
        if (returnCategory != [] and returnCategory[0] not in scorecard.scorecard) or (finalFlag == 0):
            if returnCategory == [] or returnCategory[0] in scorecard.scorecard:
                for rep in range(0,5):
                    if self.diceCounts.__contains__(6-rep):
                        return ['', [i for i, x in enumerate(dice.dice) if x in [j+1 for j, y in enumerate(self.diceCounts) if y == (6-rep)]]]
                    else:
                        if rep == 3:
                            if len(set([1, 2, 3]) - set(dice.dice)) == 0 or len(set([2, 3, 4]) - set(dice.dice)) == 0 or len(set([3, 4, 5]) - set(dice.dice)) == 0 or len(set([4, 5, 6]) - set(dice.dice)) == 0:
                                if len(set([1, 2, 3]) - set(dice.dice)) == 0:
                                    return ['', [i for i, x in enumerate(dice.dice) if x in [1, 2, 3]]]
                                elif len(set([2, 3, 4]) - set(dice.dice)) == 0:
                                    return ['', [i for i, x in enumerate(dice.dice) if x in [2, 3, 4]]]
                                elif len(set([3, 4, 5]) - set(dice.dice)) == 0:
                                    return ['', [i for i, x in enumerate(dice.dice) if x in [3, 4, 5]]]
                                elif len(set([4, 5, 6]) - set(dice.dice)) == 0:
                                    return ['', [i for i, x in enumerate(dice.dice) if x in [4, 5, 6]]]
                return ['',[]]
            else:
                return returnCategory
        else:
            retKey = [k for k, v in valSc.scorecard.items() if v == max(valSc.scorecard.values()) ][0]
            return [retKey, self.getKeptDice(retKey, dice)]

    def getKeptDice(self, category, dice):
        keptList = []
        if category == "quintupulo":
            keptList = [i for i, x in enumerate(dice.dice) if x == self.diceCounts.index(5)+1] if self.diceCounts.__contains__(5) else []
        elif category == "cuadruple":
            keptList = [i for i, x in enumerate(dice.dice) if x == self.diceCounts.index(4)+1] if self.diceCounts.__contains__(4) else []
        elif category == "elote":
            keptList = [i for i, x in enumerate(dice.dice) if x == self.diceCounts.index(3)+1 or x == self.diceCounts.index(2)+1] if self.diceCounts.__contains__(3) and self.diceCounts.__contains__(2) else []
        elif category == "triple":
            keptList = [i for i, x in enumerate(dice.dice) if x == self.diceCounts.index(3)+1] if self.diceCounts.__contains__(3) else []
        elif category == "pupusa de queso" or category == "tamal":
            keptList = [k for k in range(0, 5)]
        elif category == "pupusa de frijol":
            if len(set([1, 2, 3, 4]) - set(dice.dice)) == 0:
                keptList = [i for i, x in enumerate(dice.dice) if x in [1, 2, 3, 4]]
            elif len(set([2, 3, 4, 5]) - set(dice.dice)) == 0:
                keptList = [i for i, x in enumerate(dice.dice) if x in [2, 3, 4, 5]]
            elif len(set([3, 4, 5, 6]) - set(dice.dice)) == 0:
                keptList = [i for i, x in enumerate(dice.dice) if x in [3, 4, 5, 6]]
        elif category in ["unos","doses","treses","cuatros","cincos","seises"]:
            keptList = [i for i, x in enumerate(dice.dice) if x == Scorecard.Numbers[category]]
        return keptList

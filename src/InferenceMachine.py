# Joey Velez-Ginorio
# Rosie Aboody
# Laurie R. Santos
# Julian Jara-Ettinger
# -----------------------------
# When teaching breaks down...
# -----------------------------

"""
This script has all the machinery for computing a posterior belief in examples
for a learner. 
"""

import itertools
import numpy as np
from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from copy import deepcopy
import operator


class InferenceMachine():
    """
        Main project class. Combines the tools for hypothesis generation and updates
        to generate the final inferences of interest, namely the probability that a
        specific example would be taught out of the space of all examples.

    """
    def __init__(self, hypothesisSpace, trueHypothesis, examples, lambda_noise):

        self.taggedActions = list()

        for a in hypothesisSpace[2]:
            temp = list()
            for h in hypothesisSpace[0]:
                temp.append((self.getOutcome([a], h, lambda_noise)))
            self.taggedActions.append(temp)


    def evaluateExample(self, hypothesisSpace, trueHypothesis, examples, lambda_noise=.05,
                            independent=True, option=0):
        """
            Returns value for an example V(e). Equivalent to the posterior belief of
            the trueHypothesis for the learner.

            Params:
                hypothesisSpace - Fed from HypothesisSpaceGenerator()
                examples - a list of teacher exampleshttps://stackoverflow.com/questions/15128418/is-there-a-way-to-do-a-history-search-in-nrepl e.g. ['A','B',['B','C']]
                trueHypothesis - the combination that turns blicket detector on e.g. 'A'
                hUpdater - instance of HypothesisSpaceUpdater clspacemacs disable indent rulesass, calculates posterior 
                            belief of the learner.
                lambda_noise - how much does learner mistrust teacher data 
                option - chooses recursive/nonrecursive update

        """

        # Find index of trueHypothesis in learner's hypothesis space
        trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)
        
        # Run a hypothesis update on learner using the examples provided
        hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples,
                    self.taggedActions, lambda_noise,independent, option)

        # Calculate V(e) of example
        return hUpdater.hSpacePosterior[trueHypothesisIndex], hUpdater.hSpacePosterior

    


    def probabilityOfExamples(self, hypothesisSpace, trueHypothesis, examples, lambda_noise=.05,
                                 independent=True, option=1, tau=.1, types=True):
        """
            Returns the probability of teaching an example.

            Params:
                hypothesisSpace - Fed from HypothesisSpaceGenerator()
                examples - a list of teacher example e.g. ['A','B',['B','C']]
                trueHypothesis - the combination that turns blicket detector on e.g. 'A'
                hUpdater - instance of HypothesisSpaceUpdater class, calculates posterior 
                            belief of the learner.
                lambda_noise - how much does learner mistrust teacher data 
                option - chooses recursive/nonrecursive update
                
        """

        exampleProbs = list()


        for i in range(len(examples)):

            if independent:
                hyp, prob, posterior = self.probabilityOfExample(hypothesisSpace, trueHypothesis, [examples[i]],
                                    lambda_noise, independent, option, tau, types)
                exampleProbs.append((hyp,prob))

            else:
                hyp, prob, posterior = self.probabilityOfExample(hypothesisSpace, trueHypothesis, [examples[i]],
                                    lambda_noise, independent, option, tau, types)
                exampleProbs.append((hyp,prob))
                hypothesisSpace[1] = posterior

            hypothesisSpace[2].pop(hypothesisSpace[2].index(examples[i]))

        return exampleProbs



    def probabilityOfExample(self, hypothesisSpace, trueHypothesis, examples, lambda_noise=.05,
                                 independent=True, option=0, tau=.1, types=False):
        """
            Returns the probability of teaching an example.

            Params:
                hypothesisSpace - Fed from HypothesisSpaceGenerator()
                examples - a list of teacher example e.g. ['A','B',['B','C']]
                trueHypothesis - the combination that turns blicket detector on e.g. 'A'
                hUpdater - instance of HypothesisSpaceUpdater class, calculates posterior 
                            belief of the learner.
                lambda_noise - how much does learner mistrust teacher data 
                option - chooses recursive/nonrecursive update
                
        """

        # Saves actionSpace contained in hypothesisSpace from generator
        # self.actionSpace = hypothesisSpace[2]
        self.actionSpace = list(itertools.permutations(hypothesisSpace[2], len(examples)))

        # Removes actionSpace from hypothesisSpace list
        # hypothesisSpace = hypothesisSpace[0:2]

        # Saves example index, to look up probability later
        exampleIndex = self.actionSpace.index(tuple(examples))

        # Initialize the probability distribution 
        actionDistribution = list()
        actionPosterior = list()
        posteriorTemp = list()

        # For each possible example, calculate its value, V(e)
        for action in self.actionSpace:

            actionVal, posterior = self.evaluateExample(hypothesisSpace, trueHypothesis, 
                list(action), lambda_noise, independent, option)

            actionDistribution.append(actionVal)
            posteriorTemp.append(posterior)

        # Turn the list of values into a distribution through softmax
        # print actionDistribution
        self.actionDistribution = self.softMax(actionDistribution,tau)
        self.actionPosterior = posteriorTemp[exampleIndex]

        # Returns probability of example being taught out of all possible examples
        if types == False:
            return self.actionSpace[exampleIndex], self.actionDistribution[exampleIndex], \
            self.actionPosterior
        else:
            return self.actionSpace[exampleIndex], \
            self.addTypes(self.actionSpace, self.actionDistribution,self.actionDistribution[exampleIndex]),\
            self.actionPosterior

    def rankExamples(self, hypothesisSpace, trueHypothesis, teacherData, lambda_noise=.05,
                                         independent=True, option=0, tau=.1, types=False):
            depth = len(teacherData)
            ranks_t = self.bestExamples(deepcopy(hypothesisSpace), trueHypothesis, teacherData, depth, lambda_noise, independent,option, tau, types)
            ranks = deepcopy(ranks_t[2])
            ranks_probs = ranks_t[1]
            evals = ranks_t[3]
            rankings = list()
            temp = list()
            temp2 = list()
            temp3 = list()
            # print teacherData
            # print ranks[0]
            # print ranks[1]
            # print ranks[2]


            for i in range(len(teacherData)):
                rankings.append((teacherData[i], ranks[i][teacherData[i]]))
                temp.append((teacherData[i], ranks[i]))
                temp2.append(ranks_probs[i])
                temp3.append(evals[i])

            return rankings, temp, temp2, temp3


    def bestExamples(self, hypothesisSpace, trueHypothesis, teacherData='NONE', depth=5, lambda_noise=.05,independent=True, option=0, tau=.1, types=False):

        exampleList = list()
        probList = list()
        postList = list()
        valsList = list()

        if teacherData != 'NONE':
                depth = len(teacherData)

        for i in range(depth):

            if teacherData == 'NONE':

                    temp = self.bestExample(deepcopy(hypothesisSpace), trueHypothesis, teacherData,\
                                            lambda_noise, independent, option, tau, types)
            else:
                    temp = self.bestExample(deepcopy(hypothesisSpace), trueHypothesis, teacherData[i],\
                                            lambda_noise, independent, option, tau, types)

            example = temp[0]
            prob = temp[1]
            posterior = temp[2]
            fullpost = temp[3]

            exvals = temp[4]

            exampleList.append((example, prob))
            hypothesisSpace[1] = posterior
            probList.append(fullpost)
            postList.append(posterior)
            valsList.append(exvals)

        return exampleList, postList, probList, valsList

    def rank_dict(self,x):

        # first sort it by value
        sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
        # sorted_x = sorted_x.reverse()
        sorted_x = [list(i) for i in sorted_x]
        matching = list()

        for i in range(len(sorted_x)):
            if i != len(sorted_x)-1:


                if sorted_x[i][1] == sorted_x[i+1][1]:
                    matching.append((i,i+1))

            sorted_x[i][1] = i+1
            sorted_x[i][0] = sorted_x[i][0][0]

        for pair in matching:
            sorted_x[pair[1]][1] = sorted_x[pair[0]][1]

        return dict(sorted_x)

    def bestExample(self, hypothesisSpace, trueHypothesis, teacherExample="NONE", lambda_noise=.05,
                                 independent=True, option=0, tau=.1, types=False):
        """
            Returns the best example to teach.

            Params:
                hypothesisSpace - Fed from HypothesisSpaceGenerator()
                examples - a list of teacher example e.g. ['A','B',['B','C']]
                trueHypothesis - the combination that turns blicket detector on e.g. 'A'
                hUpdater - instance of HypothesisSpaceUpdater class, calculates posterior 
                            belief of the learner.
                lambda_noise - how much does learner mistrust teacher data 
                option - chooses recursive/nonrecursive update
                
        """

        # Saves actionSpace contained in hypothesisSpace from generator
        self.actionSpace = hypothesisSpace[2]
        self.actionSpace = list(itertools.permutations(self.actionSpace,1))


        # Removes actionSpace from hypothesisSpace list
        # hypothesisSpace = hypothesisSpace[0:2]


        # Initialize the probability distribution 
        actionDistribution = list()
        actionPosterior = list()
        posteriorTemp = list()

        # For each possible example, calculate its value, V(e)
        for action in self.actionSpace:

            actionVal, posterior = self.evaluateExample(hypothesisSpace, trueHypothesis, 
                list(action), lambda_noise, independent, option)

            actionDistribution.append(actionVal)
            posteriorTemp.append(posterior)

        # Turn the list of values into a distribution through softmax
        # print actionDistribution

        if teacherExample == 'NONE':
                self.actionDistribution = self.softMax(actionDistribution,tau)
                self.actionPosterior = posteriorTemp[np.argmax(self.actionDistribution)]

                # Returns probability of example being taught out of all possible examples
                if types == False:
                        return self.actionSpace[np.argmax(self.actionDistribution)], \
                        np.max(self.actionDistribution), self.actionPosterior, self.rank_dict(dict(zip(self.actionSpace, self.actionDistribution))),dict(zip(self.actionSpace, self.actionDistribution))
                else:
                        temp = self.maxTypes(self.actionSpace, self.actionDistribution)
                        return temp[0], temp, self.actionPosterior, self.rank_dict(dict(zip(self.actionSpace, self.actionDistribution))),dict(zip(self.actionSpace, self.actionDistribution))

        else:
                temp = deepcopy(self.actionSpace)
                temp = [i[0] for i in temp]
                ind = temp.index(teacherExample)
                self.actionDistribution = self.softMax(actionDistribution,tau)
                self.actionPosterior = posteriorTemp[ind]

                if types == False:
                        return self.actionSpace[ind], \
                        self.actionDistribution[ind], self.actionPosterior, self.rank_dict(dict(zip(self.actionSpace, self.actionDistribution))), dict(zip(self.actionSpace, self.actionDistribution))
 



    def softMax(self, arg, tau):
        """
            Returns the softmax of arg.

            Params:
                arg - a list of values
                tau - rationality paramater 

        """
        # e^(i/tau) for each value in arg
        # arg = [np.exp(i/tau) for i in arg]
        arg = np.array(arg)
        arg = np.exp(arg/tau)

        # compute sum to normalize
        arg /= arg.sum()
        
        return list(arg)


    def addTypes(self, space, distribution, val):
        total = 0
        names = list()
        for i in range(len(distribution)):
            if distribution[i] == val:
                total += val
                names.append(space[i])

        return names, total

    def maxTypes(self, space, distribution):

        a = [self.addTypes(space, distribution,i) for i in distribution]

        maxProb = 0
        maxNames = list()
        for i in range(len(a)):
            if a[i][1] > maxProb:
                maxProb = a[i][1]
                maxNames = a[i][0]

        return maxNames, maxProb


    def getOutcome(self, examples, trueHypothesis, lambda_noise = 0.05):
        """
            Returns the examples, tagged with whether they would turn the blicket
            detector on or off. Used as a helper function for the updaters.

            Params:
                examples - a list of block examples e.g. ['A','B','C',['A','B'],['AB']]
                trueHypothesis - the combination that turns on the blicket detector e.g. ['AB']
                lambda_noise - adjusts degree of mistrust the learner has in the teacher

        """

        # Initialize an example space class variable
        self.exampleSpace = list()

        # Converts trueHypothesis to a setf
        trueHypothesis = set(trueHypothesis)

        # Check for each example if it turns on the blicket detector
        for i in range(len(examples)):

            # Generate example space 
            self.exampleSpace.append(self.getExampleSpace(examples[i]))

            # Checks if example is a subset of true hypothesis
            # If so, the blicket turns on, tag with 1-lambda
            if any([set([e]).issubset(trueHypothesis) for e in self.exampleSpace[i]]):
                examples[i] = (examples[i], 1-lambda_noise, True)
                
            # If not, the blicket is off, tag with lambda
            else:
                examples[i] = (examples[i], lambda_noise, False)


        # Examples are now tagged to indicate if they turn the detector on/off
        # e.g. ('A', 0) if trueHypothesis='B'
        examples = examples[0]
        return examples


    def getExampleSpace(self, example):
        """
            Returns the example space. All the permutations possible given a particular example.

            Param:
                examples - a list of examples

        """
        exampleSpace = list()

        # Generate every possible permutation from example
        for i in range(1, len(example)+1):
            for e in itertools.combinations(example, i):
                exampleSpace.append(''.join(list(e)))

        return exampleSpace

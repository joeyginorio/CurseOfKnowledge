"""

[description]


"""
import csv
import sys
sys.path.append("..")

from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachine import InferenceMachine

###First we need to import the teacher examples from our CSV in a helpful format###
"""


reader = csv.reader(open('tester.csv', newline = ''), delimiter = ',')
inputList = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	inputList.append(rowTemp)
"""


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

trueHypothesis = ['BE']
lambda_noise = .05
independent = True
optionList = 0, 1
tau = .1
types = False
inputList = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'], ['BE', 'ABE', 'A', 'ABDE'] # for debugging
#examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'] # for debugging
labels= [['H.unorderedAnd()', 'H.unorderedAndOr()', 'H.orderedAnd()', 'H.orderedAndOr()'],['non-recursive', 'recursive']]





######## PART ONE #########

# returns the learner posterior of the True Hypothesis after each of the teacher's examples

def posteriorAfterEachExample(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option):
	
	# Initializing our InferenceMachine class
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	taggedActions = infer.taggedActions

	# Initializing our HypothesisSpaceUpdater class (so we can access its functions)
	hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples, taggedActions, 
		lambda_noise, independent, option)

	trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)

	temp = list()

	for i in examples:
		exampleProbs = (infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, [i], lambda_noise, independent, option, tau, types))
		temptemp = i, hypothesisSpace[1][trueHypothesisIndex]
		temp.append(temptemp)
	
	return temp


# Writes the results of the above function to a csv for every set of teacher examples, hypothesis space, and recursion option

def posteriorWriter1(labels, trueHypothesis, inputList, lambda_noise, independent, optionList):
	with open ('posteriorAfterEachExample.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')
		for examples in inputList:	
			recursionCounter = 0
			for option in optionList:
				spaceCounter = 0
				hypothesisSpaceList = [H.unorderedAnd(), H.unorderedAndOr(), H.orderedAnd(), H.orderedAndOr()]
				for hypothesis in hypothesisSpaceList:
					temp = [labels[0][spaceCounter], labels[1][recursionCounter]]
					temp.append(posteriorAfterEachExample(hypothesis, trueHypothesis, examples, lambda_noise, independent, option))
					writer.writerow(temp)
					#print(temp)
					spaceCounter = spaceCounter + 1
				recursionCounter = recursionCounter + 1



#posteriorWriter1(labels, trueHypothesis, inputList, lambda_noise, independent, optionList)





######## PART TWO #########

# uses HypothesisSpaceUpdater to retrieve the posterior distribution for all hypotheses given every single teacher example
# (without updating the inferred learner posterior after each example)

def posteriorGivenAllExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option):
	# Initializing our InferenceMachine class
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	taggedActions = infer.taggedActions

	# Initializing our HypothesisSpaceUpdater class (so we can access its functions)
	hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples, taggedActions, 
		lambda_noise, independent, option)

	print(infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types))

	#posterior = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types)[1]
	#return posterior #hUpdater.hSpacePosterior



hypothesisSpace = H.unorderedAnd()
examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC']
option = 0
print(posteriorGivenAllExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option))

# writes the results of posteriorGivenAllExamples to a csv file, for every set of teacher examples, hypothesis space, and recursion option

def posteriorWriter2(labels, trueHypothesis, inputList, lambda_noise, independent, optionList):
	with open ('overallPosterior.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')
		for examples in inputList:	
			recursionCounter = 0
			for option in optionList:
				spaceCounter = 0
				hypothesisSpaceList = [H.unorderedAnd(), H.unorderedAndOr(), H.orderedAnd(), H.orderedAndOr()]
				for hypothesisSpace in hypothesisSpaceList:
					posterior = posteriorGivenAllExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option)
					trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)
					
					#temp = [labels[0][spaceCounter], labels[1][recursionCounter], posterior[trueHypothesisIndex], list(zip(hypothesisSpace[0], posterior))]
					print(labels[0][spaceCounter], labels[1][recursionCounter], posterior[trueHypothesisIndex], list(zip(hypothesisSpace[0], posterior)))
					#writer.writerow(temp)
					spaceCounter = spaceCounter + 1
				recursionCounter = recursionCounter + 1


#posteriorWriter2(labels, trueHypothesis, inputList, lambda_noise, independent, optionList)


"""


def sumPosteriorDifference(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option):
	# Initializing our InferenceMachine class
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	taggedActions = infer.taggedActions

	# Initializing our HypothesisSpaceUpdater class (so we can access its functions)
	hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples, taggedActions, 
		lambda_noise, independent, option)

	firstPosterior = posteriorGivenAllExamples(hypothesisSpace, trueHypothesis, ['BE'], lambda_noise, independent, option)[3]
	print('first posterior', firstPosterior)

	differenceList = list()

	# for every possible action, get the total 
	for i in hypothesisSpace[2]:
		posteriorOfI = posteriorGivenAllExamples(hypothesisSpace, trueHypothesis, i, lambda_noise, independent, option)
		difference = [a - b for a, b in zip(firstPosterior, posteriorOfI)]
		posteriorSum = sum(difference)
		differenceList.append(posteriorSum)
	return differenceList

examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC']


sumPosteriorDifference(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option)

"""



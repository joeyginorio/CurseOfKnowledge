# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------

"""First we need to import the teacher examples from our CSV in a helpful format"""

import csv

reader = csv.reader(open('tester.csv', newline = ''), delimiter = ',')
input = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	input.append(rowTemp)

#print(input) # for debugging

import sys
sys.path.append("..")
from InferenceMachine import InferenceMachine
from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater

blockList = ['A','B','C','D', 'E']

H = GenerateHypothesisSpace(blockList)
allHypothesisSpaces = H.unorderedAnd(), H.unorderedAndOr(), H.orderedAnd(), H.orderedAndOr()

trueHypothesis = ['BE']

examples = input
#examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC']
#examples = ['BE', 'ACD', 'ABCDE']

# Determine amount of mistrust learner has in teacher. [0,1)
lambda_noise = .05

# are teacher-provided examples dependent upon one another, or independent?
independent = False

# recursive or non-recursive updating
option = 1

# rationality parameter
tau = .1

# True: hypotheses are grouped based on similarity. False: hypotheses are not grouped.
types = False

"""
temp = list()
for space in allHypothesisSpaces:
	infer = InferenceMachine(space, trueHypothesis, examples, lambda_noise)
	exampleProbs = (infer.probabilityOfExamples(space, trueHypothesis, examples, lambda_noise, independent, option, tau, types))
	temp.append(exampleProbs)
"""


"""

# Attempting to write the results of every hypothesis space for every teaching vector (n = 20) to a csv

with open ('teachProb2.csv', 'w', newline = '') as myfile:
	writer = csv.writer(myfile)
	for teachVector in examples:
		allHypothesisSpaces = H.unorderedAnd(), H.unorderedAndOr(), H.orderedAnd(), H.orderedAndOr()
		for space in allHypothesisSpaces:
			#print('hypothesis space', space)
			infer = InferenceMachine(space, trueHypothesis, teachVector, lambda_noise)
			exampleProbs = (infer.probabilityOfExamples(space, trueHypothesis, teachVector, lambda_noise, independent, option, tau, types))
			writer.writerow(exampleProbs)
			print(exampleProbs)
		print('ok onto the next teacher')
	print('really done')


"""


"""

# writes the result of all hypothesis spaces given 1 teaching vector at a time to a csv

with open ('teachProb.csv', 'w', newline = '') as myfile:
	writer = csv.writer(myfile)
	for space in allHypothesisSpaces:
		infer = InferenceMachine(space, trueHypothesis, examples, lambda_noise)
		exampleProbs = (infer.probabilityOfExamples(space, trueHypothesis, examples, lambda_noise, independent, option, tau, types))
		writer.writerow(exampleProbs)
		print(exampleProbs)
	print('ok onto the next teacher')

"""




import csv
import sys
sys.path.append("..")

from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachine import InferenceMachine

###First we need to import the teacher examples from our CSV in a helpful format###



reader = csv.reader(open('tester.csv', newline = ''), delimiter = ',')
inputList = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	inputList.append(rowTemp)


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)
#hypothesisSpace = H.depthSampler(2)

trueHypothesis = ['BE']
lambda_noise = .05
independenceAssumptionList = True, False
optionList = 0, 1 # 0 = non-recursive, 1 = recursive
tau = .1
types = False
#inputList = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'], ['BE', 'ABE', 'A', 'ABDE'] # for debugging				
labels = [['depth 2'],['non-recursive', 'recursive'], ['independent', 'dependent']]
#labels = [['unorderedAnd', 'unorderedAndOr'],['non-recursive', 'recursive'], ['independent', 'dependent']]




def teachProbANDposteriorGivenAllExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types, teachProb):


	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)

	# will return the probability of teaching each example
	if teachProb == 1:
		return infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, 
										independent, option, tau, types)[0]
	
	# will return the posterior after all examples are shown 
	elif teachProb == 2:
		return infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, 
										independent, option, tau, types)[1]
	
	# will return the posterior belief in the TH after EACH example
	elif teachProb == 3:
		trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)
		temp = list()

		for i in examples:
			exampleProbs, posterior = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, \
																	[i], lambda_noise, independent, \
																	option, tau, types)
		
			superTemp = i, posterior[trueHypothesisIndex]
			temp.append(superTemp)
	
		return temp



#print(teachProbANDposteriorGivenAllExamples(hypothesisSpace, trueHypothesis, ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'], lambda_noise, independent = False, option = 1, tau = .1, types = False, teachProb = 1))


def printer(labels, trueHypothesis, inputList, lambda_noise, independent, optionList, tau, types, uniform, teachProb):
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')

		teachCounter = 1
		
		for examples in inputList:	
			recursionCounter = 0

			# for recursive & non-recursive
			for option in optionList:
				independenceCounter = 0

				# for independent & dependent
				for independenceAssumption in independenceAssumptionList:
					spaceCounter = 0
					#hypothesisSpaceList = [H.unorderedAnd(), H.unorderedAndOr()]
					hypothesisSpaceList = [H.depthSampler(2, uniform)]

					# for each of our hypothesis spaces (currently only 1)
					for hypothesis in hypothesisSpaceList:

						temp = ['Teacher {}'.format(teachCounter), labels[0][spaceCounter], \
								labels[1][recursionCounter], labels[2][independenceCounter], teachProbANDposteriorGivenAllExamples(hypothesis, trueHypothesis, \
								examples, lambda_noise, independenceAssumption, option, tau, types, teachProb)]

						#print(temp)
						writer.writerow(temp)

						spaceCounter = spaceCounter + 1
					independenceCounter = independenceCounter + 1
				recursionCounter = recursionCounter + 1
			teachCounter = teachCounter + 1


printer(labels, trueHypothesis, inputList, lambda_noise, \
	independenceAssumptionList, optionList, tau, types, uniform = False, teachProb = 1)




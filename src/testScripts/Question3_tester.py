# IMPORTANT!
# This is the script for my last SPP analysis!
# currently it includes only the 2 most complex of our hypothesis spaces
# It includes independent & dependent
# it includes ONLY recursive
# it includes ONLY uniform prior

import csv
import sys
sys.path.append("..")


from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
#from InferenceMachine import InferenceMachine 
from InferenceMachineRemoveDuplicates import InferenceMachine
 

# original data: CofKnowlv2.csv
# v3 data: CofKnowlv3.csv
# v3 with examples that produce a 99% or above posterior for the TH removed: CofKnowlv3_above99removed.csv
# v3 with all duplicates removed: CofKnowlv3_duplicatesRemoved.csv

###First we need to import the teacher examples from our CSV in a helpful format###



reader = csv.reader(open('v4 duplicates removed_unordered morph.csv', newline = ''), delimiter = ',')
inputList = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	inputList.append(rowTemp)

print(inputList)


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

trueHypothesis = ['BE']
lambda_noise = .05
independenceAssumptionList = True, False
optionList = 0, 1 # 0 = non-recursive, 1 = recursive
option = 1
tau = .1
types = False
uniformList = True, False
#uniformOptions = True, False
#inputList = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'], ['BE', 'ABE', 'A', 'ABDE'] # for debugging				
labels = [['Simpler', 'Complex'],\
		['non-recursive', 'recursive'], ['independent', 'dependent'], ['uniform', 'simplicity']]
#labels = [['unorderedAnd', 'unorderedAndOr'],['non-recursive', 'recursive'], ['independent', 'dependent']]

# ['embeddedAndOr_2', 'unembeddedAnd_2', 'unembeddedAnd_3', 'unembeddedAndOr_2', 'unembeddedAndOr_3']


def teachProbANDposteriorGivenAllExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types, teachProb, Sum):


	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)

	# will return the probability of teaching each example
	if teachProb == 1:
		temp = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, 
										independent, option, tau, types)
		if Sum and types == False:
			tempTemp = [i[1] for i in temp]
			tempTotal = sum(tempTemp)/len(tempTemp)
			return tempTotal
		else:
			return temp


	# will return the posterior after all examples are shown 
	elif teachProb == 2:
		length = len(examples) - 1
		return infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, 
										independent, option, tau, types)[length]
	
	# will return the posterior belief in the TH after EACH example
	elif teachProb == 3:
		trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)
		temp = list()
		print("examples", examples)

		for i in examples:
			print("example", i)
			exampleProbs, posterior = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, i, lambda_noise, 
										independent, option, tau, types)

			print("exampleprobs", exampleProbs)
			print("posterior", posterior)
		
			superTemp = i, posterior[trueHypothesisIndex]
			temp.append(superTemp)
	
		return temp



#print(teachProbANDposteriorGivenAllExamples(hypothesisSpace, trueHypothesis, ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'], lambda_noise, independent = False, option = 1, tau = .1, types = False, teachProb = 1))


def printer(labels, trueHypothesis, inputList, lambda_noise, independenceAssumptionList, option, tau, types, uniform, teachProb, Sum, plot):
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		temp = list()
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
					"""
					hypothesisSpaceList = [H.depthSampler(2, uniform), H.unorderedAndDepth(2, uniform), \
						H.unorderedAndDepth(3, uniform), H.simpleDepthSampler(2, uniform), \
						H.simpleDepthSampler(3, uniform)]
					"""

					hypothesisSpaceList = [H.unorderedAndDepth(3, uniform), H.depthSampler(2, uniform)]

					# for each of our hypothesis spaces (currently only 1)
					for hypothesis in hypothesisSpaceList:

						# for plotting in ggplot2 - ignore otherwise!
						if plot == True:
							#print("examples", examples)
							counter = 1
							exampleList = list()
							alsoTemp = teachProbANDposteriorGivenAllExamples(hypothesis, trueHypothesis, \
									examples, lambda_noise, independenceAssumption, option, tau, types, teachProb, Sum)


							#print("alsotemp", alsoTemp)
							for i in alsoTemp:
								temp = [teachCounter, labels[2][independenceCounter],\
										'{}_{}'.format(labels[0][spaceCounter], labels[1][recursionCounter]), \
										't{}'.format(counter), i[1]]
								counter += 1
								print(temp)
								#writer.writerow(temp)
									

						else: 	
							
							temp = [teachCounter, labels[2][independenceCounter], \
									'{}_{}'.format(labels[0][spaceCounter], labels[1][recursionCounter]), \
									teachProbANDposteriorGivenAllExamples(hypothesis, trueHypothesis, \
									examples, lambda_noise, independenceAssumption, option, tau, types, teachProb, Sum)]

							print(temp)
							#writer.writerow(temp)

						spaceCounter = spaceCounter + 1
					
					independenceCounter = independenceCounter + 1
				recursionCounter += 1
			teachCounter = teachCounter + 1


printer(labels, trueHypothesis, inputList, lambda_noise, \
	independenceAssumptionList, optionList, tau, types, uniform = True, teachProb = 2, Sum = False, plot = True)




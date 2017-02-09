import csv
import sys
sys.path.append("..")


from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachine import InferenceMachine 
 

# original data: CofKnowlv2.csv
# v3 data: CofKnowlv3.csv

###First we need to import the teacher examples from our CSV in a helpful format###

reader = csv.reader(open('CofKnowlv2.csv', newline = ''), delimiter = ',')
inputList = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	inputList.append(rowTemp)

#print(inputList)


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

trueHypothesis = ['BE']
lambda_noise = .05
independenceAssumptionList = True
optionList = 0, 1 # 0 = non-recursive, 1 = recursive
tau = .1
types = False
uniformList = True, False
#uniformOptions = True, False
#inputList = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC'], ['BE', 'ABE', 'A', 'ABDE'] # for debugging				
labels = [['embeddedAndOr_2', 'unembeddedAnd_2', 'unembeddedAnd_3', \
			'unembeddedAndOr_2', 'unembeddedAndOr_3'],\
		['non-recursive', 'recursive'], ['uniform', 'simplicity']]


def teachProbANDposteriorGivenAllExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types, teachProb, Sum):


	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)

	# will return the probability of teaching each example
	if teachProb == 1:
		temp = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, \
										independent, option, tau, types)[0]
		if Sum and types == False:
			tempTemp = [i[1] for i in temp]
			tempTotal = sum(tempTemp)/len(tempTemp)
			return tempTotal
		else:
			return temp


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


def printer(labels, trueHypothesis, inputList, lambda_noise, independenceAssumption, optionList, tau, types, uniformList, teachProb, Sum, plot):
	with open ('posteriorAfterEachEx.csv', 'w', newline = '') as myfile:
		temp = list()
		writer = csv.writer(myfile, delimiter = ' ')

		teachCounter = 1
		
		for examples in inputList:	
			recursionCounter = 0

			# for recursive & non-recursive
			for option in optionList:
				uniformCounter = 0
				

				# for uniform = True, uniform = False
				for uniform in uniformList:

					spaceCounter = 0
					#hypothesisSpaceList = [H.unorderedAnd(), H.unorderedAndOr()]
					hypothesisSpaceList = [H.depthSampler(2, uniform), H.unorderedAndDepth(2, uniform), \
							H.unorderedAndDepth(3, uniform), H.simpleDepthSampler(2, uniform), \
							H.simpleDepthSampler(3, uniform)]

					# for each of our hypothesis spaces (currently only 1)
					for hypothesis in hypothesisSpaceList:
						# for plotting in ggplot2 - ignore otherwise!
						if plot == True:
							counter = 1
							exampleList = list()
							alsoTemp = teachProbANDposteriorGivenAllExamples(hypothesis, trueHypothesis, \
										examples, lambda_noise, independenceAssumption, option, tau, types, teachProb, Sum)
							#print(alsoTemp)
							for i in alsoTemp:
								temp = ['Teacher{}'.format(teachCounter), labels[0][spaceCounter], \
											labels[1][recursionCounter], \
											labels[2][uniformCounter], counter, \
											i[1]]
								counter += 1
								#print(temp)
								#writer.writerow(temp)
								

						else: 	

							temp = ['Teacher{}'.format(teachCounter), labels[0][spaceCounter], \
									labels[1][recursionCounter], labels[2][uniformCounter], \
									teachProbANDposteriorGivenAllExamples(hypothesis, trueHypothesis, \
									examples, lambda_noise, independenceAssumption, option, tau, types, teachProb, Sum)]

							print(temp)
							#writer.writerow(temp)

						spaceCounter = spaceCounter + 1
					uniformCounter += 1
				recursionCounter = recursionCounter + 1
			teachCounter = teachCounter + 1


printer(labels, trueHypothesis, inputList, lambda_noise, \
	independenceAssumptionList, optionList, tau, types, uniformList, teachProb = 1, Sum = True, plot = False)






import csv
import sys
sys.path.append("..")


from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachineRemoveDuplicates import InferenceMachine
# alternative: from InferenceMachine import InferenceMachine 


# this reads the teacher-provided examples and imports them in a good format

reader = csv.reader(open('CofKnowlv3_above99 and duplicates removed.csv', newline = ''), delimiter = ',')
inputList = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	inputList.append(rowTemp)

#print(inputList)



# let's define our tester functions, which will call a more general print function

# 1. teachProb

def teachProb(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum):
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	teachProb = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, \
										independent, option, tau, types)

	# this returns an average of the teaching probabilities for every example
	if Sum == True and types == False:
		teachProbTemp = [i[1] for i in teachProb]
		teachProbAverage = sum(teachProbTemp)/len(teachProbTemp)
		return teachProbAverage

	# this just returns the teaching probability of each example separately
	else:
		return teachProb


# 2. finalPosterior: shows the posterior after ALL teacher examples are shown

def finalPosterior(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum):
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	return infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, \
										independent, option, tau, types)[1]


# 3. eachExamplePosterior: returns the posterior in the TH after every example

def eachExamplePosterior(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum):
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	trueHypothesisIndex = hypothesisSpace[0].index(trueHypothesis)
	data = list()

	for i in examples:
		exampleProbs, posterior = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, \
																	[i], lambda_noise, independent, \
																	option, tau, types)
		temp = i, posterior[trueHypothesisIndex]
		data.append(temp)
	return data




def printer(functionName, labels, trueHypothesis, inputList, lambda_noise, independenceList, optionList, tau, types, uniform, Sum, plot):
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		temp = list()
		writer = csv.writer(myfile, delimiter = ' ')
		teachCounter = 1
		
		# for every set of teacher examples
		for examples in inputList:
			recursionCounter = 0

			# for recursive & non-recursive
			for option in optionList:	
				independenceCounter = 0

				# for independent & dependent
				for independent in independenceList:
					spaceCounter = 0
					hypothesisSpaceList = [H.unorderedAndDepth(3, uniform), H.depthSampler(2, uniform)]

					# for each of our hypothesis spaces (currently only 2)
					for hypothesis in hypothesisSpaceList:

						# for plotting in ggplot2 - ignore otherwise!
						if plot == True:
							counter = 1
							exampleList = list()
							alsoTemp = functionName(hypothesis, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum)
							#print(alsoTemp)
							for i in alsoTemp:
								temp = [teachCounter, labels[2][independenceCounter],\
										labels[0][spaceCounter], labels[1][recursionCounter], \
										't{}'.format(counter), i[1]]
								counter += 1
								print(temp)
								#writer.writerow(temp)
									

						else: 	

							temp = [teachCounter, labels[2][independenceCounter], \
									labels[0][spaceCounter], labels[1][recursionCounter], \
									functionName(hypothesis, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum)]

							#print(temp)
							writer.writerow(temp)

						spaceCounter += 1
					independenceCounter += 1
				recursionCounter += 1 
			teachCounter += 1



# let's define our variables

blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)
trueHypothesis = ['BE']
lambda_noise = .05
independent = True
independenceList = True, False
optionList = 0, 1 # 0 = non-recursive, 1 = recursive
option = 1 # in case we only want to use 1 at a time
tau = .1
types = False
uniformList = True, False
labels = [['Simpler', 'Complex'], ['non-recursive', 'recursive'], \
		['independent', 'dependent'], ['uniform', 'simplicity']]

printer(teachProb, labels, trueHypothesis, inputList, lambda_noise, \
	independenceList, optionList, tau, types, uniform = True, Sum = False, plot = True)




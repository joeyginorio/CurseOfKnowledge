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
		




# now let's work on our print functions. We'll start with the most basic & build from there

def basicPrinter(functionName, labels, hypothesisSpaceList, trueHypothesis, examples, lambda_noise, independent, option, tau, types, uniform, Sum, plot):
	spaceCounter = 0
	data = list()
	splitData = list()

	for hypothesis in hypothesisSpaceList:

		# prints out each trial separately, for ease of plotting (i.e., prints in "long" format)
		if plot == True:
			totalData = plotter(functionName, labels, hypothesisSpaceList, trueHypothesis, examples, lambda_noise, independent, option, tau, types, uniform, Sum, plot)

			for i in totalData:

				splitData = [labels[0][spaceCounter], 



			trialCounter = 1
			temp = functionName(hypothesis, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum)
			
			for i in temp:
				data = [labels[0][spaceCounter], 't{}'.format(trialCounter), i[1]]
				trialCounter += 1
				yield data
				#data.append(temp2)
				#writer.writerow(data)
		
		else:
			data = [labels[0][spaceCounter], functionName(hypothesis, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum)] 
			return data
			#writer.writerow(data)

		spaceCounter += 1
	#return data


def plotter(functionName, labels, hypothesisSpaceList, trueHypothesis, examples, lambda_noise, independent, option, tau, types, uniform, Sum, plot):
	trialCounter = 1
	totalData = list()
	temp = functionName(hypothesis, trueHypothesis, examples, lambda_noise, independent, option, tau, types, Sum)

	for i in temp:
		data = 't{}'.format(trialCounter), i[1]]
		totalData.append(data)
		trialCounter += 1
	return totalData


def settings(functionName, labels, trueHypothesis, inputList, lambda_noise, independenceList, optionList, tau, types, uniform, Sum, plot):
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')

		teachCounter = 1

		for examples in inputList:
			recursionCounter = 0

			# for recursive & non-recursive
			for option in optionList:
				independenceCounter = 0

				# for independent or dependent
				for independent in independenceList:
					hypothesisSpaceList = [H.unorderedAndDepth(3, uniform), H.depthSampler(2, uniform)]
					data = [teachCounter, labels[2][independenceCounter], labels[1][recursionCounter], \
					basicPrinter(functionName, labels, hypothesisSpaceList, trueHypothesis, examples, \
					lambda_noise, independent, option, tau, types, uniform, Sum, plot)]
					
					print(data)
					#writer.writerow(data)
					

					independenceCounter += 1
					#print("independence counter", independenceCounter)
				recursionCounter += 1
				#print("recursion counter", recursionCounter)

			teachCounter += 1



#examples = ['BE', 'ACD', 'ABCDE', 'ABCD']
settings(teachProb, labels, trueHypothesis, inputList, lambda_noise, independenceList, optionList, tau, types, uniform = True, Sum = False, plot = True)


#basicPrinter(teachProb, labels, hypothesisSpaceList, trueHypothesis, inputList, lambda_noise, independenceList, option, tau, types, uniform = True, Sum = False, plot = False)






















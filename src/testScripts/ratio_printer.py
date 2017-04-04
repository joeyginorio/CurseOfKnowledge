import csv
import sys
sys.path.append("..")


from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachineRemoveDuplicates import InferenceMachine
# alternative: from InferenceMachine import InferenceMachine 


# let's define our variables

blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)
trueHypothesis = ['BE']
lambda_noise = .05
option = 1 # 0 = non-recursive, 1 = recursive
tau = .1
types = False # no grouping based on type
uniform = True # uniform prior (alt: simplicity)


# this reads the teacher-provided examples and imports them in format we can work with

reader = csv.reader(open('CofKnowlv3_above99 and duplicates removed.csv', newline = ''), delimiter = ',')
inputList = list()
for row in reader:
	rowTemp = list()
	for i in row:
		if i != '':
			rowTemp.append(i)
	inputList.append(rowTemp)

#print(inputList)



# Now let's define our tester functions

# 1. teachProb: calculates the teaching probability of any set of examples

def teachProb(hypothesisSpace, trueHypothesis, examples, lambda_noise, tau, types, uniform, option, independent):
	infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
	teachProb = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, \
										independent, option, tau, types)
	return teachProb

# 2. when called by "compiler", uses teachProb to generate the teaching probabilities of each teacher-generated example

def generator(labels, hypothesisSpace, trueHypothesis, examples, lambda_noise, tau, types, uniform, option, independent):
	finalList = list()
	index = list()
	myList = teachProb(hypothesisSpace, trueHypothesis, examples, lambda_noise, tau, types, uniform, option, independent)
	counter = 1

	for i in myList:
		finalList.append(i[1])
		index.append([labels, 't{}'.format(counter)])
		counter += 1

	return finalList, index

# to test this:
#print(generator("test independent recursive", H.unorderedAndDepth(3, uniform), trueHypothesis, inputList[1], lambda_noise, tau, types, uniform, option, independent = False))


# 3. calls generator to generate independent & dependent teachProb's, as well as labels for each instance

def compiler(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option):
	indep, indepIndex, dep, depIndex = list(), list(), list(), list()
	teachCounter = 1

	for examples in inputList:

		hypothesisCopy1, hypothesisCopy2 = H.unorderedAndDepth(3, uniform), H.unorderedAndDepth(3, uniform)

		# calculating the independent teachProb
		independentLabels = [teachCounter, "independent", "simple", "recursive"]
		tempIndep, tempIndepIndex = generator(independentLabels, hypothesisCopy1, trueHypothesis, examples, lambda_noise, tau, types, uniform, option, independent = True)

		# calculating the dependent teachProb
		dependentLabels = [teachCounter, "dependent", "simple", "recursive"]
		tempDep, tempDepIndex = generator(dependentLabels, hypothesisCopy2, trueHypothesis, examples, lambda_noise, tau, types, uniform, option, independent = False)

		# storing the index values:
		indepIndex.append(tempIndepIndex)
		depIndex.append(tempDepIndex)

		# storing the teachProb values:
		indep.append(tempIndep)
		dep.append(tempDep)

		teachCounter += 1


	#print(list(zip(indep, indepIndex)))
	return indep, indepIndex, dep, depIndex

# to test this:
#print(compiler(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option))


# 4. This calculates the ratio we need 

def ratioCalculator(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option):
	indep, indepIndex, dep, depIndex = compiler(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)
	ratio = list()

	for list1, list2 in zip(indep, dep):
		#print(list1, list2)

		for num1, num2 in zip(list1, list2):
			ratio.append(float(num1)/float(num2))

	return indepIndex, depIndex, ratio


# to test this:
#print(ratioCalculator(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option))



# 5. This prints the ratios we need to a csv so I can visualize the data

def printer(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option):
	indexList = list()
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')
		indepIndex, depIndex, ratio = ratioCalculator(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)

		for teacherLabels in indepIndex:
			for i in teacherLabels:
				indexList.append(i)

		for index, r in zip(indexList, ratio):
			#print(index, r)
			writer.writerow(zip(index, r))


		#print(indexList)






		


printer(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)





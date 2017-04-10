import csv
import sys
import numpy as np
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


# data csv files: CofKnowlv3_above99 and duplicates removed.csv

# this reads the teacher-provided examples and imports them in format we can work with

reader = csv.reader(open('CofKnowlv3_duplicatesRemoved.csv', newline = ''), delimiter = ',')
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

		#hypothesisCopy1, hypothesisCopy2 = H.depthSampler(2, uniform), H.depthSampler(2, uniform)

		# calculating the independent teachProb
		independentLabels = [teachCounter, "independent", "simple_recursive"]
		tempIndep, tempIndepIndex = generator(independentLabels, hypothesisCopy1, trueHypothesis, examples, lambda_noise, tau, types, uniform, option, independent = True)

		# calculating the dependent teachProb
		dependentLabels = [teachCounter, "dependent", "simple_recursive"]
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

	return indepIndex, depIndex, ratio, 


# to test this:
#print(ratioCalculator(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option))



# 5. This takes the natural log of the ratio (to help with the skewed nature of this data)

def naturalLog(ratio):
	ratioList = list()
	for i in ratio:
		ratioList.append(np.log(i))
	return ratioList

# to test this:
#indepIndex, depIndex, ratio = ratioCalculator(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)
#print(naturalLog(ratio))


# 6. this calcuates whether independent or dependent fit the data better (or whether they are equal)

def depVSindepCalculator(naturalLogRatio):
	ratioLabels = list()
	for i in naturalLogRatio:
		if i == 0:
			ratioLabels.append(["0", "equal"])
		elif i > 0:
			ratioLabels.append(["2", "independent_better"])
		else:
			ratioLabels.append(["1", "dependent_better"])

	return ratioLabels



# 7. This prints the ratios we need to a csv so I can visualize the data

def printer(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option):
	indexList = list()
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')
		indepIndex, depIndex, ratio = ratioCalculator(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)


		# this creates labels for each ratio entry
		for teacherLabels in indepIndex:
			for i in teacherLabels:
				indexList.append(i)

		# now we calculate our ln(ratio)
		naturalLogRatio = naturalLog(ratio)
		#print(naturalLogRatio)

		# now we calculate whether independent or dependent is better for each ln(ratio)
		winner = depVSindepCalculator(naturalLogRatio)

		# this merges the ratio, the naturalLogRatio, and whether independent or dependent was better
		finalRatio = list(zip(naturalLogRatio, winner))
		#print(finalRatio)

		# this merges the teacher labels & the non-normlaized ratio
		labelsAndRatio = list(zip(indexList, ratio))
		#print(labelsAndRatio)

		for i, j in zip(labelsAndRatio, finalRatio):
			print(i, j)
			#writer.writerow(zip(i, j))

		#print(indexList)



def compilerPrinter(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option):
	with open ('teachProb.csv', 'w', newline = '') as myfile:
		writer = csv.writer(myfile, delimiter = ' ')

		indep, indepIndex, dep, depIndex = compiler(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)

		all = list(zip(indep, dep))

		for i in all:
			print(i)


		

compilerPrinter(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)
#printer(trueHypothesis, inputList, lambda_noise, tau, types, uniform, option)





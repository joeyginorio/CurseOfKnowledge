# Joey Velez-Ginorio
# Raboody (Radish)
# --------------------
# Curse of Knowledge Project
# --------------------
#
# This script will compute analysis #1 for the CoK project

import sys
import csv
sys.path.append("..")
from InferenceMachine import InferenceMachine
from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from copy import deepcopy


"""
1. Get the teacher data
"""
# Read in the teacher data
teacherData = list()
reader = csv.reader(open('CofKnowlv3_duplicatesRemoved.csv','rU'), delimiter=',',dialect=csv.excel_tab)

# Creates 2D list of all teachers data
for row in reader:
	teacherData.append(row)

# Cleans up data (there are redundant '' in the data)
for i in range(len(teacherData)):
	while '' in teacherData[i]:
		teacherData[i].remove('')

"""
2. Run analysis #1 
"""
# Specify blockList
blockList = ['A','B','C','D','E']

# Initialize H, make list of all hypothesisSpaces
H = GenerateHypothesisSpace(blockList)
hSpaces = list()

# our hypothesis spaces:
hSpaces.append(H.simpleDepthSampler(2, uniform = True))
#hSpaces.append(H.depthSampler(2, uniform = True))

# their names:
hSpacesNames = list()
hSpacesNames.append('simple_d2')
#hSpacesNames.append('complex_d2')

"""
# Hypothesis spaces over uniform prior 
hSpaces.append(H.depthSampler(2,uniform=True))
hSpaces.append(H.simpleDepthSampler(2,uniform=True))
hSpaces.append(H.simpleDepthSampler(3,uniform=True))
hSpaces.append(H.unorderedAndDepth(2,uniform=True))
hSpaces.append(H.unorderedAndDepth(3,uniform=True))

# Hypothesis spaces over simplicity prior
hSpaces.append(H.depthSampler(2,uniform=False))
hSpaces.append(H.simpleDepthSampler(2,uniform=False))
hSpaces.append(H.simpleDepthSampler(3,uniform=False))
hSpaces.append(H.unorderedAndDepth(2,uniform=False))
hSpaces.append(H.unorderedAndDepth(3,uniform=False))

# Hand-code names for each hSpace, for when writing the .csv
hSpacesNames = list()
hSpacesNames.append('embeddedAndOr_2_uniform')
hSpacesNames.append('unembeddedAndOr_2_uniform')
hSpacesNames.append('unembeddedAndOr_3_uniform')
hSpacesNames.append('unembeddedAnd_2_uniform')
hSpacesNames.append('unembeddedAnd_3_uniform')

hSpacesNames.append('embeddedAndOr_2_simplicity')
hSpacesNames.append('unembeddedAndOr_2_simplicity')
hSpacesNames.append('unembeddedAndOr_3_simplicity')
hSpacesNames.append('unembeddedAnd_2_simplicity')
hSpacesNames.append('unembeddedAnd_3_simplicity')
"""

# Prepare the csv we'll be writing results to
oFile = open('analysis1.csv','w')
oFile2 = open('analysis2.csv','w')
CSV = csv.writer(oFile)
CSV2 = csv.writer(oFile2)
CSV.writerow(['Teacher #', 'Hypothesis Space', "Type", "Trial","Posterior"])
CSV2.writerow(['Teacher #', 'Hypothesis Space', "Type", "Count to Threshold"])
# Run the analysis!!!!!!!!!

lambda_noise = .05


##
# Threshold
thresh = .95
##

# Loop through all hypothesis spaces
for i in range(len(hSpaces)):

	# Loop through all teachers
	for j in range(len(teacherData)):

		boolSpaces1 = [False]*len(hSpaces)
		boolSpaces2 = [False]*len(hSpaces)
		boolSpaces3 = [False]*len(hSpaces)
		boolSpaces4 = [False]*len(hSpaces)

		# Loop through all teacher's teaching sequences
		for k in range(len(teacherData[j])):

			# Recursive + Dependent 
			infer = InferenceMachine(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)], lambda_noise)
			hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
				infer.taggedActions, lambda_noise , False, 1)

			# Get 'BE' index, record posterior in csv
			ind = hUpdater.hypothesisSpace.index(['BE'])
			CSV.writerow([j+1, hSpacesNames[i], 'Recursive + Dependent', k+1, 
				hUpdater.hSpacePosterior[ind]])

			if hUpdater.hSpacePosterior[ind] > thresh and boolSpaces1[i] is False:
				CSV2.writerow([j+1, hSpacesNames[i], 'Recursive + Dependent', k+1])
				boolSpaces1[i] = True

			if hUpdater.hSpacePosterior[ind] < thresh and boolSpaces1[i] is False and k==len(teacherData[j])-1:
				CSV2.writerow([j+1, hSpacesNames[i], 'Recursive + Dependent', 0])

			"""
			# Recursive + Independent
			infer = InferenceMachine(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)], lambda_noise)
			hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
				infer.taggedActions, lambda_noise , True, 1)

			# Get 'BE' index, record posterior in csv
			ind = hUpdater.hypothesisSpace.index(['BE'])
			CSV.writerow([j+1, hSpacesNames[i], 'Recursive + Independent', k+1, 
				hUpdater.hSpacePosterior[ind]])

			if hUpdater.hSpacePosterior[ind] > thresh and boolSpaces2[i] is False:
				CSV2.writerow([j+1, hSpacesNames[i], 'Recursive + Independent', k+1])
				boolSpaces2[i] = True

			if hUpdater.hSpacePosterior[ind] < thresh and boolSpaces2[i] is False and k==len(teacherData[j])-1:
				CSV2.writerow([j+1, hSpacesNames[i], 'Recursive + Independent', 0])
			"""

			# Non-Recursive + Dependent
			infer = InferenceMachine(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)], lambda_noise)
			hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
				infer.taggedActions, lambda_noise , False, 0)

			# Get 'BE' index, record posterior in csv
			ind = hUpdater.hypothesisSpace.index(['BE'])
			CSV.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Dependent', k+1, 
				hUpdater.hSpacePosterior[ind]])

			if hUpdater.hSpacePosterior[ind] > thresh and boolSpaces3[i] is False:
				CSV2.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Dependent', k+1])
				boolSpaces3[i] = True

			if hUpdater.hSpacePosterior[ind] < thresh and boolSpaces3[i] is False and k==len(teacherData[j])-1:
				CSV2.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Dependent', 0])

			"""
			# Non-Recursive + Independent
			infer = InferenceMachine(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)], lambda_noise)
			hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
				infer.taggedActions, lambda_noise , True, 0)

			# Get 'BE' index, record posterior in csv
			ind = hUpdater.hypothesisSpace.index(['BE'])
			CSV.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Independent', k+1, 
				hUpdater.hSpacePosterior[ind]])

			if hUpdater.hSpacePosterior[ind] > thresh and boolSpaces4[i] is False:
				CSV2.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Independent', k+1])
				boolSpaces4[i] = True

			if hUpdater.hSpacePosterior[ind] < thresh and boolSpaces4[i] is False and k==len(teacherData[j])-1:
				CSV2.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Independent', 0])
			"""
				

oFile.close()
oFile2.close()
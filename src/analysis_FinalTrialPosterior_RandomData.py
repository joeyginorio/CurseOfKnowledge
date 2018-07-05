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
1. Randomly generate teacher data
"""
# Specify blockList
blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)
teacherData = list()
teacherData.append(H.random_depth_sampler(7,2,uniform=True))



"""
2. Get the posterior belief in the TH after all of the examples
"""
# Specify blockList
blockList = ['A','B','C','D','E']

# Initialize H, make list of all hypothesisSpaces
H = GenerateHypothesisSpace(blockList)
hSpaces = list()
hSpacesNames = list()

# our hypothesis spaces:
#hSpaces.append(H.simpleDepthSampler(2, uniform = True))
#hSpaces.append(H.simpleDepthSampler(3, uniform = True))
#hSpaces.append(H.simpleDepthSampler(4, uniform = True))
#hSpaces.append(H.simpleDepthSampler(5, uniform = True))
hSpaces.append(H.depthSampler(2, uniform = True))


# their names:
#hSpacesNames.append('simple_d2')
#hSpacesNames.append('simple_d3')
#hSpacesNames.append('simple_d4')
#hSpacesNames.append('simple_d5')
hSpacesNames.append('complex_d2')




# Prepare the csv we'll be writing results to
oFile = open('finalTrialposterior_RandomData.csv','w')
CSV = csv.writer(oFile)
CSV.writerow(['Teacher #', 'Hypothesis Space', "Type", "Trial","Posterior"])
# Run the analysis!!!!!!!!!

lambda_noise = .05

# repeat N times
for n in range(10):

	# Loop through all hypothesis spaces
	for i in range(len(hSpaces)):

		# Loop through all teachers
		for j in range(len(teacherData)):

			# Loop through all teacher's teaching sequences
			for k in [len(teacherData[j])-1]:

				# Recursive + Dependent 
				infer = InferenceMachine(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)], lambda_noise)
				hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
					infer.taggedActions, lambda_noise , False, 1)

				# Get 'BE' index, record posterior in csv
				ind = hUpdater.hypothesisSpace.index(['BE'])
				CSV.writerow([j+1, hSpacesNames[i], 'Recursive + Dependent', k+1, 
					hUpdater.hSpacePosterior[ind]])

				# Non-Recursive + Dependent
				infer = InferenceMachine(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)], lambda_noise)
				hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
					infer.taggedActions, lambda_noise , False, 0)

				# Get 'BE' index, record posterior in csv
				ind = hUpdater.hypothesisSpace.index(['BE'])
				CSV.writerow([j+1, hSpacesNames[i], 'Non-Recursive + Dependent', k+1, 
					hUpdater.hSpacePosterior[ind]])




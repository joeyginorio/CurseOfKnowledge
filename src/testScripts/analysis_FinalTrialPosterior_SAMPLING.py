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
#reader = csv.reader(open('Study1_TeacherReplication_DuplicatesRemoved.csv','rU'), delimiter=',',dialect=csv.excel_tab)
reader = csv.reader(open('CofKnowlv3_duplicatesRemoved.csv','rU'), delimiter=',',dialect=csv.excel_tab)
#reader = csv.reader(open('In-Lab Pedagogy Replication.csv','rU'), delimiter=',',dialect=csv.excel_tab)



"""
2. Run analysis #1 
"""
# Specify blockList
blockList = ['A','B','C','D','E']

# Initialize H, make list of all hypothesisSpaces
H = GenerateHypothesisSpace(blockList)
hSpaces = list()
hSpacesNames = list()

# our hypothesis spaces:
hSpaces.append(H.random_depth_sampler(30,2,uniform=True))

# their names:
hSpacesNames.append('complex_d2_sampled')


# Prepare the csv we'll be writing results to
oFile = open('finalTrialposterior_SAMPLING.csv','w')
CSV = csv.writer(oFile)
CSV.writerow(['Teacher #', 'Hypothesis Space', "Type", "Trial","Posterior"])
# Run the analysis!!!!!!!!!

lambda_noise = .05

####### ####### ####### 
####### add a loop that runs this X number of times (e.g., 1,000)
####### ####### ####### 

for k in [len(teacherData) - 1]:
	# Recursive + Dependent 
	infer = InferenceMachine(deepcopy(hSpaces),['BE'],teacherData, lambda_noise)
	hUpdater = HypothesisSpaceUpdater(deepcopy(hSpaces[i]),['BE'],teacherData[j][0:(k+1)],
		infer.taggedActions, lambda_noise , False, 1)

	# Get 'BE' index, record posterior in csv
	ind = hUpdater.hypothesisSpace.index(['BE'])
	print(ind)
	CSV.writerow([1, hSpacesNames[i], 'Recursive + Dependent', k+1, 
		hUpdater.hSpacePosterior[ind]])

"""

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
"""


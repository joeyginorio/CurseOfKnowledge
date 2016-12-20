# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------


import itertools	# useful module for combinations/permutations

def generateActionSpace(blockList):
	"""
	
		Takes a list of blocks e.g. ['A','B','C'] and generates every possible
		action a teacher may take, i.e. every combination possible within the list.

		Params: 
			blockList - a list of characters corresponding to blocks

	"""

	# Initialize empty action space
	actionSpace = list()

	# Generate every possible combination of actions from blockList
	for i in range(1, len(blockList)+1):
		for actions in itertools.combinations(blockList, i):
			actionSpace.append(list(actions))

	return actionSpace


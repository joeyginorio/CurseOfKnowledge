# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------

import itertools

class GenerateHypothesisSpace():
	"""
		Class which holds several hypothesis space generator functions. 

	"""

	def __init__(self, blockList):
		self.blockList = blockList
		self.unorderedArgs = self.unorderedArgs(self.blockList)
		self.orderedArgs = self.orderedArgs(self.blockList)


	def unorderedArgs(self, blockList):
		"""
			Generates a list of arguments for the unordered set of hypothesis
			generators. Takes a blockList, and generates every combination.

			Param: 
				blockList - a list of characters
				uniform - boolean, if true, will set prior to uniform distribution
		"""

		# Initialize empty action space
		args = list()
		args += blockList

		# Generate every possible combination of arguments from blockList
		for i in range(2, len(blockList)+1):
			for arg in itertools.combinations(blockList, i):
				args.append(list(arg))

		return args


	def orderedArgs(self, blockList):
		"""
			Generates a list of arguments for the unordered set of hypothesis
			generators. Takes a blockList, and generates every combination.

			Param: 
				blockList - a list of characters
		"""

		# Initialize empty action space
		args = list()
		args += blockList

		# Generate every possible combination of arguments from blockList
		for i in range(2, len(blockList)+1):
			for arg in itertools.permutations(blockList, i):
				args.append(list(arg))

		return args


	def unorderedOr(self, uniform=True):
		"""
			Hypothesis Space #1:
			Generates a list of hypotheses, including all combinations of
			Or logic rules.

			Param:
				uniform - if true, prior for H is uniform, else t.b.d

		"""

		# Initializes hypothesis space and prior
		hypothesisSpace = list()
		hypothesisSpacePrior = list()

		# Add the single-block hypotheses to hypothesis space
		hypothesisSpace += [[i] for i in self.unorderedArgs[0:len(self.blockList)]]

		# Remove the single-block hypotheses from arguments
		args = self.unorderedArgs[len(self.blockList):]

		# Use args as arguments for Or(), add to hyp. space
		for arg in args:
			hypothesisSpace.append(self.Or(*arg))

		if uniform:
			# Calculate prior distribution of hypothesis space
			hypothesisSpacePrior = [1.0/len(self.unorderedArgs) for i in self.unorderedArgs]


		return [hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]]


	def unorderedAnd(self, uniform=True):
		"""
			Hypothesis Space #1:
			Generates a list of hypotheses, including all combinations of
			And logic rules.

			Param:
				uniform - if true, prior for H is uniform, else t.b.d

		"""

		# Initializes hypothesis space and prior
		hypothesisSpace = list()
		hypothesisSpacePrior = list()

		# Add the single-block hypotheses to hypothesis space
		hypothesisSpace += [[i] for i in self.unorderedArgs[0:len(self.blockList)]]

		# Remove the single-block hypotheses from arguments
		args = self.unorderedArgs[len(self.blockList):]

		# Use args as arguments for Or(), add to hyp. space
		for arg in args:
			hypothesisSpace.append(self.And(*arg))

		if uniform:
			# Calculate prior distribution of hypothesis space
			hypothesisSpacePrior = [1.0/len(self.unorderedArgs) for i in self.unorderedArgs]

		return [hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]]

	
	def unorderedAndOr(self, uniform = True):
		"""
			Hypothesis Space # 3:
			Generates a list of hypotheses, including all combinations of
			And and Or logic rules.

			Param:
				uniform - if ture, prior for H is uniform, else t.b.d.
		"""

		# Initializes hypothesis space and prior
		hypothesisSpace = list()
		hypothesisSpacePrior = list()

		# Add hypotheses to the hypothesis space
		hypothesisSpace += [[i] for i in self.unorderedArgs[0:len(self.blockList)]]

		# Remove the single-block hypotheses from arguments so they don't get
		# needlessly duplicated.
		args = self.unorderedArgs[len(self.blockList):]

		# Use args as arguments for And() as well as Or(), add to hypothesis space
		for arg in args:
			hypothesisSpace.append(self.And(*arg))
			hypothesisSpace.append(self.Or(*arg))

		if uniform:
			# Calculate prior distribution of hypothesis space
			hypothesisSpacePrior = [1.0/len(self.unorderedArgs) for i in self.unorderedArgs]

		
		# hypothesisSpace = all possible And & Or hypotheses
		# hypothesisSpacePrior = either uniform, or simplicity biased (tba)
		# the last statement makes up the actionSpace, by taking all the combinations 
		# we made in unorderedArgs and simply taking away all the spaces etc. 
		return hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]


	def orderedAnd(self, uniform = True):

		"""
			Hypothesis space #4
			Generates a list of ordered hypotheses, including all combinations
			of the And logical operator. 
		"""
		# Initializes the hypothesis space and prior
		hypothesisSpace, hypothesisSpacePrior = list(), list()

		# Add hypotheses to the hypothesis space:
		hypothesisSpace += [[i] for i in self.orderedArgs[0:len(self.blockList)]]

		# Remove the single-block hypotheses from the list of arguments
		args = self.orderedArgs[len(self.blockList):]

		# use the args as arguments for the And() function & add to hypothesisSpace
		for arg in args:
			hypothesisSpace.append(self.And(*arg))

		if uniform:
			# Calculate prior
			hypothesisSpacePrior = [1.0/len(self.orderedArgs) for i in self.orderedArgs]

		return hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]


	def orderedAndOr(self, uniform = True):

		""" 
			Hypothesis space # 5:
			Generates a lsit of ordered hypotheses, including all combinations of
			the And && Or logical operators
		"""

		# Initializes the hypothesis space & prior
		hypothesisSpace, hypothesisSpacePrior = list(), list()

		# Add hypotheses to the hypothesis space:
		hypothesisSpace += [[i] for i in self.orderedArgs[0:len(self.blockList)]]

		# remove the single-block hypotheses from the list of arguments
		args = self.orderedArgs[len(self.blockList):]

		# use the args as arguments for the And() and Or() functions and add to hyopthesisSpace
		for arg in args:
			hypothesisSpace.append(self.And(*arg))
			hypothesisSpace.append(self.Or(*arg))

		if uniform:
			# calculate prior
			hypothesisSpacePrior = [1.0/len(self.orderedArgs) for i in self.orderedArgs]

		return hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]

	
	def Or(self, *args):
		"""
			Logical Or, e.g. Or('A','B') = ['A','B']
			Can handle 2 or more arguments

			Param: 
				*args - May accept any argument, but
				for the model, block characters generally used

		"""

		# Our return list
		temp = list()

		# Sift through arguments to add to final list
		for arg in args:

			# If argument is a tuple, convert to list then add
			if type(arg) is tuple:
				temp.append(list(arg))

			# Standard character, add as usual
			else:
				temp.append(arg)

		return temp


	def And(self, *args):
		

		"""
			Logical And, e.g. And('A','B') -> ['AB','BA']
			Can handle 2 or more arguments.

			Param:
				*args - May accept any argument, but
				for the model, block characters generally used.

		"""

		args = list(args)

		# Convert arguments to list if not already
		for i in range(len(args)):
 			if type(args[i]) is not list:
 				args[i] = list([args[i]])

 		# Initialize final list
		final = list()

		# Generate all permutations of arguments
		temp = list(itertools.permutations(args))

		# Compute all products within each permutation
		for arg in temp:
			final.append(list([''.join(s) for s in list(itertools.product(*arg))]))

		
		return [''.join(i) for i in final]
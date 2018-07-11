# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------

import itertools
import numpy as np

class GenerateHypothesisSpace():
	"""
		Class which holds several hypothesis space generator functions. 

	"""

	def __init__(self, blockList):
		self.blockList = blockList
		self.unorderedArgs = self.unorderedArgs(self.blockList)
		self.orderedArgs = self.orderedArgs(self.blockList)

	def simpleDepthSampler(self, depth, uniform):
		"""
			Samples AND, OR hypotheses at several depths.
		"""
		x = lambda x: ''.join(x)	# Beautiful function to make hypotheses pretty
		
		hypotheses = []
		args = []

		for i in range(1,depth+1):
			args = itertools.chain(args, map(x,itertools.combinations('ABCDE',i)))

		args = [[i] for i in args]
		
		args = list(args)


		y = lambda y: self.Or(*y)

		for i in range(1, depth+1):
			hypotheses = itertools.chain(hypotheses, map(y, 
												itertools.combinations('ABCDE',i)))

		hypotheses = args + list(hypotheses)

		if uniform:
			prior = list()
			prior = [1.0/len(hypotheses) for i in hypotheses]

		else:
			prior = list()
			for h in hypotheses:
				prior.append(1.0/self.priorHelp(h))
			normal = sum(prior)
			prior = [i/normal for i in prior]

			

		return [hypotheses, prior, [''.join(i) for i in self.unorderedArgs]]

	def depthSampler(self, depth,uniform=True):
		"""
			Samples AND, OR hypotheses at several depths.

		"""
		x = lambda x: ''.join(x)	# Beautiful function to make hypotheses pretty
	
		hypotheses = []
		args = []

		for i in range(1,depth+1):
			args = itertools.chain(args, itertools.imap(x,itertools.combinations('ABCDE',i)))

		args = list(args)


		y = lambda y: self.Or(*y)

		for i in range(1, depth+1):
			hypotheses = itertools.chain(hypotheses, itertools.imap(y, 
											itertools.combinations(args,i)))
		
		hypotheses = list(hypotheses)
		if uniform:
			prior = list()
			prior = [1.0/len(hypotheses) for i in hypotheses]

		else:
			prior = list()
			for h in hypotheses:
				prior.append(1.0/self.priorHelp(h))
			normal = sum(prior)
			prior = [i/(5+normal) for i in prior]

			

		return [hypotheses, prior, [''.join(i) for i in self.unorderedArgs]]

	
	"""
		Same thing as depthSampler, except you first specify how many samples
		you want from the hypothesis space depthSampler gives.
	"""
	def random_depth_sampler(self, samples, depth, uniform=True, th = ['BE']):

		
		temp = self.depthSampler(depth,uniform)
		hyps = temp[0]
		arg = temp[2]

		if len(hyps) < samples:
			print 'Desired sample size is larger than total hypothesis space, choose larger depth'
			return None

		final_hyps = list()
		final_hyps.append(th)
		
		for i in range(samples-1):
			ind = np.random.choice(len(hyps))
			while hyps[ind] == th:
				ind = np.random.choice(len(hyps))

			temp = hyps.pop(ind)
			final_hyps.append(temp)

		if uniform:
			prior = list()
			prior = [1.0/len(final_hyps) for i in final_hyps]

		np.random.shuffle(final_hyps)

		return [final_hyps, prior, arg]

	def random_teacher(self, num_examples):

		temp = self.depthSampler(1,uniform=True)
		examples = temp[2]

		return list(np.random.choice(examples,size=num_examples,replace=False))



	def priorHelp(self, hypothesis):
		total = 0
		for h in hypothesis:
			total += len(h)

		return total

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


	def unorderedAndDepth(self, depth, uniform=True):
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
		args = [i for i in args if len(i) <= depth]

		# Use args as arguments for Or(), add to hyp. space
		for arg in args:
			hypothesisSpace.append(self.And(*arg))

		if uniform:
			# Calculate prior distribution of hypothesis space
			hypothesisSpacePrior = [1.0/len(hypothesisSpace) for i in hypothesisSpace]

		else:
			for h in hypothesisSpace:
				hypothesisSpacePrior.append(1.0/self.priorHelp(h))
				normal = sum(hypothesisSpacePrior)
				hypothesisSpacePrior = [i/normal for i in hypothesisSpacePrior]

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
			hypothesisSpacePrior = [1.0/len(hypothesisSpace) for i in hypothesisSpace]

		
		# hypothesisSpace = all possible And & Or hypotheses
		# hypothesisSpacePrior = either uniform, or simplicity biased (tba)
		# the last statement makes up the actionSpace, by taking all the combinations 
		# we made in unorderedArgs and simply taking away all the spaces etc. 
		return [hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]]


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

		return [hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]]


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
		args2 = self.unorderedArgs[len(self.blockList):]

		# use the args as arguments for the And() and Or() functions and add to hyopthesisSpace
		for arg in args:
			hypothesisSpace.append(self.And(*arg))
		for arg in args2:
			hypothesisSpace.append(self.Or(*arg))

		if uniform:
			# calculate prior
			hypothesisSpacePrior = [1.0/len(hypothesisSpace) for i in hypothesisSpace]

		return [hypothesisSpace, hypothesisSpacePrior, [''.join(i) for i in self.unorderedArgs]]

	
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


	# def And(self, *args):
		

	# 	"""
	# 		Logical And, e.g. And('A','B') -> ['AB','BA']
	# 		Can handle 2 or more arguments.

	# 		Param:
	# 			*args - May accept any argument, but
	# 			for the model, block characters generally used.

	# 	"""

	# 	args = list(args)

	# 	# Convert arguments to list if not already
	# 	for i in range(len(args)):
 # 			if type(args[i]) is not list:
 # 				args[i] = list([args[i]])

 # 		# Initialize final list
	# 	final = list()

	# 	# Generate all permutations of arguments
	# 	temp = list(itertools.permutations(args))

	# 	# Compute all products within each permutation
	# 	for arg in temp:
	# 		final.append(list([''.join(s) for s in list(itertools.product(*arg))]))

		
	# 	return [''.join(i) for i in final]

   	def And(self,*args):
 		
 		args = list(args)

 		for i in range(len(args)):
 		
 			if type(args[i]) is not list:
 				args[i] = list([args[i]])

		return [''.join(s) for s in list(itertools.product(*args))]
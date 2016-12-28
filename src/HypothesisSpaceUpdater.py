# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------


import itertools
from GenerateHypothesisSpace import GenerateHypothesisSpace


class HypothesisSpaceUpdater():
	"""
		Class which holds non-recursive / recursive hypothesis space updater

	"""
	
	def __init__(self, hypothesisSpace, trueHypothesis, examples, lambda_noise=.05, 
					independent=True, option=0):
		"""	
			Params:
				hypothesisSpace - feed using GenerateHypothesisSpace
				trueHypothesis - the combination that lights blicket detector
				option - 0 for nonrecursive, 1 for recursive

		"""
		
		# Saving inputs as class variables, helpful for debugging/interacting w/ model
		self.hypothesisSpace = hypothesisSpace[0]
		self.examples = examples
		self.trueHypothesis = trueHypothesis
		self.lambda_noise = lambda_noise
		self.option = option

		# Tag examples to see if they turn blicket detector on or off
		examples = examples[:]
		examples = self.getOutcome(examples, trueHypothesis, lambda_noise)

		# Nonrecursive update, calculating posterior, P(H|E)
		if option == 0:
			self.hypothesisSpaceUpdater(hypothesisSpace, examples, independent)

		# Recursive update, for future.....
		else:
			self.recursiveSpaceUpdater(hypothesisSpace, examples, independent)
	
	def recursiveSpaceUpdater(self, hypothesisSpace, examples, independent=True):
		"""

		Returns the posterior distribution of of learner's hypothesis space after 
		being shown examples. The likelihood is calculated through a nonrecursive
		model of P_learner(H|E) to reflect what the teacher knows about the learner's 
		hypothesis space.

		P_learner(H|E) = P_teacher(E|H)P_learner(H)

		Params:
			hypothesisSpace - a list, where index 0 contains a hypothesisSpace
			and index 1 contains its prior distribution. Use the GenerateHypothesisSpace
			class for this argument (provides the hypSpace with prior in a list).

			examples - a list of tuples, where each example is tagged 0 or 1 depending
			on whether it turns the blicket detector on or off. 
	
		"""

		# If using the independence assumption, calculate as such
		if independent:
			self.hSpacePosterior, self.hSpaceLikelihood, self.hSpacePrior = \
			self.independentRBayes(hypothesisSpace, examples, independent)

		# Else calculate w/out independence assumption
		else:
			self.hSpacePosterior, self.hSpaceLikelihood, self.hSpacePrior = \
			self.dependentRBayes(hypothesisSpace, examples, independent)


	def hypothesisSpaceUpdater(self, hypothesisSpace, examples, independent=True):
		"""
			Returns posterior distribution of learner's hypothesis space
			after being shown examples.  

			P_learner(H|E) = P_learner(E|H)P_learner(H)

			NOTE: examples must be ran through getOutcome() so that they are tagged
			0 (off) or 1 (on) - to indicate their effect on the blicket detector.

			Params:
				hypothesisSpace - a list, where index 0 contains a hypothesisSpace
				and index 1 contains its prior distribution. Use the GenerateHypothesisSpace
				class for this argument (provides the hypSpace with prior in a list).

				examples - a list of tuples, where each example is tagged 0 or 1 depending
				on whether it turns the blicket detector on or off. 

		"""


		# If using the independence assumption, calculate as such
		if independent:
			self.hSpacePosterior, self.hSpaceLikelihood, self.hSpacePrior = \
			self.independentBayes(hypothesisSpace, examples)

		# Else calculate w/out independence assumption
		else:
			self.hSpacePosterior, self.hSpaceLikelihood, self.hSpacePrior = \
			self.dependentBayes(hypothesisSpace, examples)
		

	def independentRBayes(self, hypothesisSpace, examples, independent):
		"""
			Returns the likelihood with the independent examples assumption.
			Recursive version.

			Params:
				hypothesisSpace - a list of hypotheses
				hypothesisSpacePrior - a prior distribution for hypotheses
				examples - list of examples

	
		"""

		hSpace = hypothesisSpace[:]

		hSpacePrior = hypothesisSpace[1]
		hSpaceLikelihood = list()
		hSpacePosterior = list()

		hypothesisSpace = hypothesisSpace[0]

		for i in range(len(hypothesisSpace)):

			# For each hypothesis, initialize a likelihood to 1
			# to be multiplied by P(E|H) for all e in E
			# e.g. P(H|E) = P(e_1|H)P(e_2|H)...P(H)
			likelihood = 1

			# Iterate over all examples
			for j in range(len(examples)):

				self.hypothesisSpaceUpdater(hSpace, examples, independent)
				likelihood *= self.hSpacePosterior[i]

			hSpaceLikelihood.append(likelihood)


		hSpacePosterior = [hSpacePrior[i]*hSpaceLikelihood[i] for i in 
									range(len(hSpacePrior))]
		
		# Normalize Posterior
		normalize = sum(hSpacePosterior)
		hSpacePosterior = [i/normalize for i in hSpacePosterior]

		return hSpacePosterior, hSpaceLikelihood, hSpacePrior


	def dependentRBayes(self, hypothesisSpace, examples, independent):
		"""
			Returns the likelihood without the independent examples assumption.
			Recursive version.

			Params:
				hypothesisSpace - a list of hypotheses
				hypothesisSpacePrior - a prior distribution for hypotheses
				examples - list of examples

	
		"""

		hSpace = hypothesisSpace[:]

		hSpacePrior = hypothesisSpace[1]
		hSpaceLikelihood = list()
		hSpacePosterior = list()

		hypothesisSpace = hypothesisSpace[0]

		for i in range(len(hypothesisSpace)): 

			# For each hypothesis, initialize a likelihood to 1
			# to be multiplied by P(E|H) for all e in E
			# e.g. P(H|E) = P(e_1|H_1)P(e_2|H_2)..P(e_n|H_n)P(H_n)
			# 				P(H_1) = P(H), P(H2) = P(e_1|H_1), ....
			likelihood = 1
			prior = hSpacePrior[i]
			hSpacePrior.append(prior)
			
			# Iterate over all examples 
			for j in range(len(examples)):

				self.hypothesisSpaceUpdater(hSpace, examples, independent)
				likelihood *= self.hSpacePosterior[i] 

				# Get posterior
				posterior = likelihood * prior
				
				# Posterior becomes new prior
				prior = posterior
		
			hSpacePosterior.append(posterior)

		# Normalize Posterior
		normalize = sum(hSpacePosterior)
		hSpacePosterior = [i/normalize for i in hSpacePosterior]

		return hSpacePosterior, hSpaceLikelihood, hSpacePrior


	def independentBayes(self, hypothesisSpace, examples):
		"""
			Returns the likelihood with the independent examples assumption.

			Params:
				hypothesisSpace - a list of hypotheses
				hypothesisSpacePrior - a prior distribution for hypotheses
				examples - list of examples

	
		"""

		hSpacePrior = hypothesisSpace[1]
		hSpaceLikelihood = list()
		hSpacePosterior = list()

		hypothesisSpace = hypothesisSpace[0]

		for i in range(len(hypothesisSpace)):

			# For each hypothesis, initialize a likelihood to 1
			# to be multiplied by P(E|H) for all e in E
			# e.g. P(H|E) = P(e_1|H)P(e_2|H)...P(H)
			likelihood = 1

			# Iterate over all examples
			for j in range(len(examples)):

				# Check if any of the example space is a subset of hypothesis space
				if any(set([e]).issubset(set(hypothesisSpace[i])) for e in self.exampleSpace[j]):
					likelihood *= examples[j][1]

				else:
					likelihood *= 1.0/len(hypothesisSpace)


			hSpaceLikelihood.append(likelihood)


		hSpacePosterior = [hSpacePrior[i]*hSpaceLikelihood[i] for i in 
									range(len(hSpacePrior))]
		
		# Normalize Posterior
		normalize = sum(hSpacePosterior)
		hSpacePosterior = [i/normalize for i in hSpacePosterior]


		return hSpacePosterior, hSpaceLikelihood, hSpacePrior


	def dependentBayes(self, hypothesisSpace, examples):
		"""
			Returns the likelihood without the independent examples assumption.

			Params:
				hypothesisSpace - a list of hypotheses
				hypothesisSpacePrior - a prior distribution for hypotheses
				examples - list of examples

	
		"""

		hSpacePrior = hypothesisSpace[1]
		hSpaceLikelihood = list()
		hSpacePosterior = list()

		hypothesisSpace = hypothesisSpace[0]

		for i in range(len(hypothesisSpace)): 

			# For each hypothesis, initialize a likelihood to 1
			# to be multiplied by P(E|H) for all e in E
			# e.g. P(H|E) = P(e_1|H_1)P(e_2|H_2)..P(e_n|H_n)P(H_n)
			# 				P(H_1) = P(H), P(H2) = P(e_1|H_1), ....
			likelihood = 1
			prior = hSpacePrior[i]
			hSpacePrior.append(prior)
			
			# Iterate over all examples 
			for j in range(len(examples)):

				# Check if any of the example space is a subset of hypothesis space
				if any(set([e]).issubset(set(hypothesisSpace[i])) for e in self.exampleSpace[j]):
					likelihood *= examples[j][1]

				else:
					likelihood *= 1.0/len(hypothesisSpace)

				# Get posterior
				posterior = likelihood * prior
				
				# Posterior becomes new prior
				prior = posterior
		
			hSpacePosterior.append(posterior)

		# Normalize Posterior
		normalize = sum(hSpacePosterior)
		hSpacePosterior = [i/normalize for i in hSpacePosterior]

		return hSpacePosterior, hSpaceLikelihood, hSpacePrior


	def getOutcome(self, examples, trueHypothesis, lambda_noise = 0.05):
		"""
			Returns the examples, tagged with whether they would turn the blicket
			detector on or off. Used as a helper function for the updaters.

			Params:
				examples - a list of block examples e.g. ['A','B','C',['A','B'],['AB']]
				trueHypothesis - the combination that turns on the blicket detector e.g. ['AB']
				lambda_noise - adjusts degree of mistrust the learner has in the teacher

		"""

		# Initialize an example space class variable
		self.exampleSpace = list()

		# Converts trueHypothesis to a setf
		trueHypothesis = set(trueHypothesis)

		# Check for each example if it turns on the blicket detector
		for i in range(len(examples)):

			# Generate example space 
			self.exampleSpace.append(self.getExampleSpace(examples[i]))

			# Checks if example is a subset of true hypothesis
			# If so, the blicket turns on, tag with 1-lambda
			if any([set([e]).issubset(trueHypothesis) for e in self.exampleSpace[i]]):
				examples[i] = (examples[i], 1-lambda_noise)
				
			# If not, the blicket is off, tag with lambda
			else:
				examples[i] = (examples[i], lambda_noise)


		# Examples are now tagged to indicate if they turn the detector on/off
		# e.g. ('A', 0) if trueHypothesis='B'
		return examples


	def getExampleSpace(self, example):
		"""
			Returns the example space. All the permutations possible given a particular example.

			Param:
				examples - a list of examples

		"""
		exampleSpace = list()

		# Generate every possible permutation from example
		for i in range(1, len(example)+1):
			for e in itertools.combinations(example, i):
				exampleSpace.append(''.join(list(e)))

		return exampleSpace




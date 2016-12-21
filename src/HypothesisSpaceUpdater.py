# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------



from GenerateHypothesisSpace import GenerateHypothesisSpace


class HypothesisSpaceUpdater():
	"""
		Class which holds non-recursive / recursive hypothesis space updater

	"""
	
	def __init__(self, hypothesisSpace, examples, trueHypothesis, lambda_noise=.2, option=0):
		"""	
			Params:
				hypothesisSpace - feed using GenerateHypothesisSpace
				trueHypothesis - the combination that lights blicket detector
				option - 0 for nonrecursive, 1 for recursive

		"""
		
		# Saving inputs as class variables, helpful for debugging/interacting w/ model
		self.hypothesisSpace = hypothesisSpace[0]
		self.examples = examples
		self.trueHypotheses = trueHypothesis
		self.lambda_noise = lambda_noise
		self.option = option

		# Tag examples to see if they turn blicket detector on or off
		examples = self.getOutcome(examples, trueHypothesis, lambda_noise)

		# Nonrecursive update, calculating posterior, P(H|E)
		if option == 0:
			self.hypothesisSpacePosterior = self.hypothesisSpaceUpdater(hypothesisSpace, examples)

		# Recursive update, for future.....
		else:
			pass
		


	def hypothesisSpaceUpdater(self, hypothesisSpace, example):
		"""
			Returns posterior distribution of learner's hypothesis space
			after being shown examples.  

			P(H|E) = P(E|H)P(H)

			NOTE: examples must be ran through getOutcome() so that they are tagged
			0 (off) or 1 (on) - to indicate their effect on the blicket detector.

			Params:
				hypothesisSpace - a list, where index 0 contains a hypothesisSpace
				and index 1 contains its prior distribution. Use the GenerateHypothesisSpace
				class for this argument (provides the hypSpace with prior in a list).

				examples - a list of tuples, where each example is tagged 0 or 1 depending
				on whether it turns the blicket detector on or off. 

		"""

		# Extract prior
		hypothesisSpacePrior = hypothesisSpace[1]

		# Extract hypothesis space
		hypothesisSpace = hypothesisSpace[0]

		# Calculate likelihood
		hypothesisSpaceLikelihood = list()


		for hypothesis in hypothesisSpace:

			# For each hypothesis, initialize a likelihood to 1
			# to be multiplied by P(E|H) for all e in E
			# e.g. P(E|H) = P(e_1|H)P(e_2|H)...P(H)
			likelihood = 1

			# for example in examples:
			# 	if example[0].issubset(hypothesis):
			# 		likelihood *= example[1]
			# 	else:
			# 		likelihood *= 1.0/len(examples)
			if set(example[0]).issubset(hypothesis) or \
				set([example[0]]).issubset(hypothesis):

				likelihood *= example[1]

			else:
				likelihood *= 1.0/len(hypothesisSpace)

			hypothesisSpaceLikelihood.append(likelihood)


		# Save prior and likelihood as class variables
		self.hypothesisSpacePrior = hypothesisSpacePrior
		self.hypothesisSpaceLikelihood = hypothesisSpaceLikelihood

		# Posterior = Likelihood * Prior
		hypothesisSpacePosterior = [hypothesisSpacePrior[i]*hypothesisSpaceLikelihood[i] 
										for i in range(len(hypothesisSpacePrior))]
		
		# Normalize Posterior
		normalize = sum(hypothesisSpacePosterior)
		hypothesisSpacePosterior = [i/normalize for i in hypothesisSpacePosterior]

		return hypothesisSpacePosterior


	def getOutcome(self, example, trueHypothesis, lambda_noise = 0.2):
		"""
			Returns the examples, tagged with whether they would turn the blicket
			detector on or off. Used as a helper function for the updaters.

			Params:
				examples - a list of block examples e.g. ['A','B','C',['A','B'],['AB']]
				trueHypothesis - the combination that turns on the blicket detector e.g. ['AB']
				lambda_noise - adjusts degree of mistrust the learner has in the teacher

		"""

		# Converts each example to a set
		# examples = [set(example) for example in examples]

		# Converts trueHypothesis to a setf
		trueHypothesis = set(trueHypothesis)

		# Checks if example is a subset of true hypothesis
		# If so, the blicket turns on, tag with 1-lambda
		if set(example).issubset(trueHypothesis) or \
			set([example]).issubset(trueHypothesis):
			
			example = (example, 1-lambda_noise)
			
		# If not, the blicket is off, tag with lambda
		else:
			example = (example, lambda_noise)


		# Examples are now tagged to indicate if they turn the detector on/off
		# e.g. ('A', 0) if trueHypothesis='B'
		return example
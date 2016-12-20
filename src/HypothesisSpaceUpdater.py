# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------


class HypothesisSpaceUpdater():
	"""
		Class which holds non-recursive / recursive hypothesis space updater

	"""
	
	# def __init__(self, trueHypothesis):
		# pass


	def hypothesisSpaceUpdater(self, hypothesisSpace, examples):
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

			# Formats the hypothesis so it is easy to calculate likelihood
			temp = hypothesis
			hypothesis = list()
			hypothesis.append(temp)

			# For each hypothesis, initialize a likelihood to 1
			# to be multiplied by P(E|H) for all e in E
			# e.g. P(E|H) = P(e_1|H)P(e_2|H)...P(H)
			likelihood = 1
			for example in examples:
			
				# If example is not relevant to hypothesis i.e. E independent of H
				# P(H|E) = P(H), where P(E|H) is 1
				# if example[0] not in hypothesis:
				if type(hypothesis[0]) is list:
					likelihood = example[1] if example[0] in hypothesis[0] else 1.0/len(examples)

				
					print "likelihood list"
					print example[0], hypothesis, likelihood
					print "-----------"

				elif type(hypothesis[0]) is str:
					likelihood = example[1] if example[0] is hypothesis[0] else 1.0/len(examples)
					# likelihood *= example[1]
					print "likelihood str"
					print example[0], hypothesis, likelihood
					print '-----------'

			hypothesisSpaceLikelihood.append(likelihood)

		return hypothesisSpaceLikelihood



	# def exampleInHypothesis(self, example, hypothesis):
	# 	"""
	# 		Returns True or False, depending on whether the example is in 
	# 		the space of the hypothesis: checks if the example is irrelevant 
	# 		to the hypothesis. A helper function to hypothesisSpaceUpdater.

	# 		Param:
	# 			example - a tuple containing an example, and 0 or 1 tag
	# 			hypothesis - e.g. A -> 'A' , Or(A,B) -> ['A','B']

	# 	"""
	# 	if type(hypothesis[0]) is list:
	# 		likelihood = example[1] if example in hypothesis[0] else 1.0/len(examples)

	# 	elif type(hypothesis[0]) is str:
	# 		likelihood = example[1] if example is hypothesis[0] else 1.0/len(examples)






	def getOutcome(self, examples, trueHypothesis, lambda_noise = 0.0):
		"""
			Returns the examples, tagged with whether they would turn the blicket
			detector on or off. Used as a helper function for the updaters.

			Params:
				examples - a list of block examples e.g. ['A','B','C',['A','B']]

		"""

		# Formats the trueHypothesis so it is easy to check which
		# examples turn it on.
		trueHypothesis = [trueHypothesis,]

		# Go through examples, see which ones turn on blicket detector
		for i in range(len(examples)):

			if type(trueHypothesis[0]) is list:
				examples[i] = (examples[i],1-lambda_noise) if examples[i] in trueHypothesis \
								else (examples[i],lambda_noise)


			elif type(trueHypothesis[0]) is str:
				examples[i] = (examples[i],1-lambda_noise) if examples[i] is trueHypothesis[0] \
								else (examples[i],lambda_noise)


			# # If the example meets condition to turn on blicket, assign 1
			# if examples[i] in trueHypothesis:
			# 	examples[i] = (examples[i],1-lambda_noise)
			
			# # Else, if example doesn't turn on blicket, assign 0
			# else:
			# 	examples[i] = (examples[i],lambda_noise)

		# Examples are now tagged to indicate if they turn the detector on/off
		# e.g. ('A', 0) if trueHypothesis='B'
		return examples
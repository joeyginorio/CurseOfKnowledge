# Rosie Aboody
# Joey Velez-Ginorio
# Julian Jara-Ettinger
# Curse of Knowledge Project
# -----------------------------------------------------------------------------


"""
	Overall Description:

	This script shows how to use the Curse of Knowledge source code to
	calculate the probability that a specific example would be taught
	in the blicket detector test.

	- Tips:
		There are quite a few parameters to check out, but a nice experiment is
		keeping everything constant and only changing the example - to see which
		examples are good/bad given a trueHypothesis.

"""


""" Imports """
# Allows us to import parent directory
import sys
sys.path.append("..")

import numpy as np

# Import our inference machine, which handles all the inference
from InferenceMachine import InferenceMachine
from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater


""" Input Specification """
# Specify the blocks we will be using
blockList = ['A','B','C','D', 'E']

# Initialize H, so that it may call multiple hypothesisSpaceGenerators
# e.g. H.unorderedOr() generates hypothesis space for unorederedOr
H = GenerateHypothesisSpace(blockList)
hypothesisSpace = H.unorderedAnd()

# Determine amount of mistrust learner has in teacher. [0,1)
# low values = high trust, high values = low trust
lambda_noise = .05

# True Hypothesis
# Or(A,B) -> ['A','B']
trueHypothesis = ['BE']

# Pick example
# e.g. 'AB' means both A and B are on blicket detector

#examples = ['BE', 'B', 'E']
#examples = ['BE']
#examples = H.unorderedAnd()[2]
examples = ['A']


"""Calculations"""
# Initialize an instance of our InferenceMachine
infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)

# Print probability of teaching example given a hypothesisSpace and the trueHypothesis
exampleProbs = (infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent=True, option=1, tau=.1, types=False))
print(exampleProbs)
#probs = [[i[1]] for i in exampleProbs] # to get the probabilities alone



"""Now, how did we get those probabilities?"""

# STEP ONE: calculate the posterior probability of the (th|Example) by running evaluateExample:

#evaluateExample = infer.evaluateExample(hypothesisSpace, trueHypothesis, examples, lambda_noise = 0.05, independent = True, option = 1)
# evaluateExample returns not only the values, but also the highst value. To get only the values:
#evaluateExampleProb = evaluateExample[1]
#exampleValue = evaluateExampleProb[1]

# STEP TWO: compute the probability of the action

# 2.1: figure out what the posterior of the TH is for every single action in the action space

"""allExampleValues = infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise=.05,
								 independent=True, option=1, tau=.1, types=False)"""
#infer.actionDistribution


# to get value of all actions (i.e., the posterior for BE given this example would be: )

"""
for i in H.unorderedAnd()[0]:
	exampleList = list()
	exampleList.append(infer.evaluateExample(hypothesisSpace, trueHypothesis, i, lambda_noise = 0.05, independent = True, option = 1))

"""






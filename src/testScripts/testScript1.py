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
		There are quite a few parameters to check out, but a nice experiment is
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
hypothesisSpace = H.depthSampler(2, uniform = False)
#hypothesisSpace = H.unorderedAnd()


# True Hypothesis
# Or(A,B) -> ['A','B']
trueHypothesis = ['BE']

# Pick example
# e.g. 'AB' means both A and B are on blicket detector
#examples = ['BE', 'B', 'E']
#examples = ['BE']
#examples = H.unorderedAnd()[2]
#examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC']
examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC']

# Determine amount of mistrust learner has in teacher. [0,1)
# low values = high trust, high values = low trust
lambda_noise = .05

# are teacher-provided examples dependent upon one another, or independent?
independent = True

# recursive or non-recursive updating; 0 == non-recursive, 1 == recursive
option = 1

# rationality parameter
tau = .1

# True: hypotheses are grouped based on similarity. False: hypotheses are not grouped.
types = False




"""Calculations"""
# Initialize an instance of our InferenceMachine
infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)


print('recursive, dependent')
print(infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, 
									independent, option, tau, types)[0])

# Print probability of teaching example given a hypothesisSpace and the trueHypothesis
#exampleProbs, posterior = (infer.probabilityOfExamples(hypothesisSpace, trueHypothesis, examples, lambda_noise, independent, option, tau, types))
#print('DEpendent, recursive', exampleProbs)


"""
# if types = True, use the following code to get all the actions & their aggregated probabilities
actions = infer.actionSpace
temp = [(infer.addTypes(infer.actionSpace, infer.actionDistribution, i)[1]) for i in infer.actionDistribution]
zipped = list(zip(actions, temp))
print(zipped) 
"""






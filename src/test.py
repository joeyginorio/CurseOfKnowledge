# Joey Velez-Ginorio
# Rosie Aboody
# Laurie R. Santos
# Julian Jara-Ettinger
# -----------------------------
# When teaching breaks down...
# -----------------------------

"""
This script serves as a general template for running any tests you want
from the model. Feed in the examples you want to teach, and it returns
the belief in the true hypothesis after teaching those examples.
"""

# Import the model
from InferenceMachine import InferenceMachine
from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from copy import deepcopy

# Specify the blocks you use, set up the hypothesis space
blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)
hSpace = H.depthSampler(2,2)

# Specify the true hypothesis
th = ['BE']

# Specify the examples to teach
teacherData = ['B','E','BE']

# Specify model parameters
recursion = 1 # recursive reasoning on
independent = False # treat examples as independent (probabilistically)
lambda_noise = 0.05 # the lower it is, the more the student trusts teacher examples


# Feed everything into the model
infer = InferenceMachine(deepcopy(hSpace),th ,teacherData, lambda_noise)
hUpdater = HypothesisSpaceUpdater(deepcopy(hSpace), th, teacherData,
				infer.taggedActions, lambda_noise , independent, recursion)

# Extract the posteriors for each hypothesis after teaching
final_posterior = zip(hUpdater.hypothesisSpace, hUpdater.hSpacePosterior)
print final_posterior


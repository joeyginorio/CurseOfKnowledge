import sys
sys.path.append("..")

from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachine import InferenceMachine


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

hypothesisSpace = H.unorderedAnd()
trueHypothesis = ['BE']
#examples = ['BE', 'AB', 'DE', 'ABE', 'ABCDE', 'AC']
examples = ['BE']
#taggedActions = ['BE']
lambda_noise = .05
independent = True
option = 1 # 1 = recursive, 0 = non-recursive


# Initializing our InferenceMachine class
infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
taggedActions = infer.taggedActions


# Initializing our HypothesisSpaceUpdater class (so we can access its functions)
hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples, taggedActions,  
					lambda_noise, independent, option)



# prints the posterior of the TH after being shown a series of examples
# prints the posterior for exactly ONE hypothesis space & ONE non/recursion rule
# see "Question1.py" for a more comprehensive tester of our 1st goal/question

if option == 0: # NON-RECURSIVE
	posterior, likelihood, prior = hUpdater.independentBayes(hypothesisSpace, examples)
	overallSpace = hUpdater.hypothesisSpaceUpdater(hypothesisSpace, examples, independent)
	trueHypothesisPosterior = posterior[11]
	print('non-recursive', trueHypothesisPosterior)

else: # RECURSIVE
	posterior, likelihood, prior = hUpdater.independentRBayes(hypothesisSpace, examples, independent)
	overallSpace = hUpdater.recursiveSpaceUpdater(hypothesisSpace, examples, independent)
	trueHypothesisPosterior = posterior[11]
	print('recursive', trueHypothesisPosterior)


"""
#### ADDITIONAL CHECKS ####

# checking Bayes math:
non_normalizedPosterior = [prior*likelihood for prior, likelihood in zip(prior, likelihood)]
normalizedPosterior = [i/sum(non_normalizedPosterior) for i in non_normalizedPosterior]

# prints the outcome of our examples (i.e., do they turn the machine on or not)
outcome = hUpdater.getOutcome(examples, trueHypothesis, lambda_noise)
print(outcome)

# to mess around with values: 
prior = hUpdater.hSpacePrior
likelihood = hUpdater.hSpaceLikelihood
posterior = hUpdater.hSpacePosterior

"""



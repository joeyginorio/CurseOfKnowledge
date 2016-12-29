import sys
sys.path.append("..")

from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

hypothesisSpace = H.unorderedAnd()
trueHypothesis = ['BE']
#example = ['AB', 'BA']
example = H.orderedArgs
lambda_noise = .05
independent = 1
option = 0



#print(hypothesisSpace, trueHypothesis, example, lambda_noise, option)
# you initialize the class. Only then can you access the objects within the class.

hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, example, 
					lambda_noise, independent, option)

prior = hUpdater.hSpacePrior
likelihood = hUpdater.hSpaceLikelihood
posterior = hUpdater.hSpacePosterior


# checking Bayes math:
# non_normalizedPosterior = [prior*likelihood for prior, likelihood in zip(prior, likelihood)]
# normalizedPosterior = [i/sum(non_normalizedPosterior) for i in non_normalizedPosterior]

# Print prior, likelihood and posterior
"""
print("Prior: ", prior)f
print("Likelihood: ", likelihood)
print("Posterior: ", posterior)
"""

outcome = hUpdater.getOutcome(example, trueHypothesis, lambda_noise)
print(outcome)


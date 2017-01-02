import sys
sys.path.append("..")

from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater
from InferenceMachine import InferenceMachine


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

hypothesisSpace = H.unorderedAndOr()
trueHypothesis = ['BE']
examples = ['BE'] #H.unorderedArgs
#examples = ['B', 'E']
#taggedActions = ['BE']
lambda_noise = .05
independent = True
option = 0

infer = InferenceMachine(hypothesisSpace, trueHypothesis, examples, lambda_noise)
taggedActions = infer.taggedActions


#print(hypothesisSpace, trueHypothesis, examples, lambda_noise, option)
# you initialize the class. Only then can you access the objects within the class.

hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, examples, taggedActions,  
					lambda_noise, independent, option)

prior = hUpdater.hSpacePrior
likelihood = hUpdater.hSpaceLikelihood
posterior = hUpdater.hSpacePosterior


# checking Bayes math:
non_normalizedPosterior = [prior*likelihood for prior, likelihood in zip(prior, likelihood)]
normalizedPosterior = [i/sum(non_normalizedPosterior) for i in non_normalizedPosterior]

# Print prior, likelihood and posterior

print("Prior: ", prior)
print("Likelihood: ", likelihood)
print("Posterior: ", posterior)


outcome = hUpdater.getOutcome(examples, trueHypothesis, lambda_noise)
print(outcome)


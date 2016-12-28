import sys
sys.path.append("..")

from GenerateHypothesisSpace import GenerateHypothesisSpace
from HypothesisSpaceUpdater import HypothesisSpaceUpdater


blockList = ['A','B','C','D','E']
H = GenerateHypothesisSpace(blockList)

hypothesisSpace = H.unorderedOr()
trueHypothesis = ['B', 'E']
example = ['AB']
lambda_noise = .1
independent = 1
option = 0


#print(hypothesisSpace, trueHypothesis, example, lambda_noise, option)
# you initialize the class. Only then can you access the objects within the class.

hUpdater = HypothesisSpaceUpdater(hypothesisSpace, trueHypothesis, example, 
					lambda_noise, independent, option)

print("Prior: ", hUpdater.hSpacePrior)
print("Likelihood: ", hUpdater.hSpaceLikelihood)
print("Posterior: ", hUpdater.hSpacePosterior)

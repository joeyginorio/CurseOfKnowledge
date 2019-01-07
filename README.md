# How to use this model.
This model lets us simulate how impactful a teachers' examples are on a students ability to learn a concept. Below is a guide as to how you would do so. Its contents are all stored in test.py. I recommend running test.py and then changing parameters to get a sense for how the model functions (as well as reading through below).

```Python
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
```
If you run the above example in test.py, you should see that the learner is confident that the true hypothesis is 'BE'. 

### Reference
*Aboody, R., Velez-Ginorio, J., Santos, L. R., & Jara-Ettinger, J. When teaching breaks down: Teachers rationally select what information to share, but misrepresent learners’ hypothesis spaces.*

http://jjara.scripts.mit.edu/cdl/docs/2018/Aboody_pedagogy_cogsci2018.pdf

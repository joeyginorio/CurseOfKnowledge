import sys
sys.path.append("..")

import csv
from GenerateHypothesisSpace import GenerateHypothesisSpace

blockList = ['A','B','C','D', 'E']
H = GenerateHypothesisSpace(blockList)

#print(H.unorderedAnd()) # testing the complete function with unorderedAnd
#print(H.unorderedOr()) # testing the complete function with unorderedOr
#print(H.unorderedAndOr()) # testing the complete function with unorderedAndOr


# orderedAnd is too large for Rosie's IDE to handle so I've it writes to a csv instead.
"""
with open ('GenerateHypothesisSpace_orderedAnd.csv', 'w', newline = '') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(H.orderedAnd()[0])
"""


# Same as above; orderedAndOr too large for Rosie's IDE to handle w/out crashing.
"""
with open ('GenerateHypothesisSpace_orderedAndOr.csv', 'w', newline = '') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(H.orderedAndOr()[0])
"""

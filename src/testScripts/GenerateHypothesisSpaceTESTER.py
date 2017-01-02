import sys
sys.path.append("..")

import csv
from GenerateHypothesisSpace import GenerateHypothesisSpace

blockList = ['A','B', 'C', 'D', 'E']
H = GenerateHypothesisSpace(blockList)

#print(H.unorderedAnd()) # testing the complete function with unorderedAnd
print(H.unorderedOr()) # testing the complete function with unorderedOr
#print(H.unorderedAndOr()) # testing the complete function with unorderedAndOr
#print(H.orderedAnd())
#print(H.orderedAndOr())

# Code to write to a csv instead:
"""
with open ('GenerateHypothesisSpace_orderedAnd.csv', 'w', newline = '') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(H.orderedAnd()[0])
"""




with open ('overallPosterior.csv', 'w', newline = '') as myfile:
	writer = csv.writer(myfile, delimiter = ' ')

	allHypothesisSpaces = H.unorderedAnd(), H.unorderedAndOr(), H.orderedAnd(), H.orderedAndOr()
	hypothesisSpaceNames = ['H.unorderedAnd()', 'H.unorderedAndOr()', 'H.orderedAnd()', 'H.orderedAndOr()']
	options = 0, 1


	# for every teach vector in list "input"
	for teachVector in input:
		i = -1
		# for each of our 4 hypothesis spaces
		for hypothesisSpace in allHypothesisSpaces:
			#print('hypothesis space', hypothesisSpace)
			i = i + 1
			# true hypothesis index to recover the posterior
			
			originalSpace = hypothesisSpace


			for option in options:
				print(hypothesisSpaceNames[i])
				hypothesisSpace = originalSpace
				#print('hypothesis space', hypothesisSpace)

				for example in teachVector:



					if option == 0: # NON-RECURSIVE


						
						posterior, likelihood, prior = hUpdater.independentBayes(hypothesisSpace, [example])
						overallSpace = hUpdater.hypothesisSpaceUpdater(hypothesisSpace, [example], independent)
						trueHypothesisPosterior = posterior[trueHypothesisIndex]
						print(trueHypothesisPosterior)
						hypothesisSpace[1] = posterior
						#temp = ['non-recursive', hypothesisSpaceNames[i], trueHypothesisPosterior]#, list(zip(hypothesisSpace[0], posterior))]
						#writer.writerow(temp)
						#print(temp)
						
	 
					elif option == 1:
						posterior, likelihood, prior = hUpdater.independentRBayes(hypothesisSpace, [example], independent)
						overallSpace = hUpdater.independentRBayes(hypothesisSpace, [example], independent)
						trueHypothesisPosterior = posterior[trueHypothesisIndex]
						print(trueHypothesisPosterior)
						hypothesisSpace[1] = posterior
						#temp = ['recursive', hypothesisSpaceNames[i], trueHypothesisPosterior]#, list(zip(hypothesisSpace[0], posterior))]
						#writer.writerow(temp)
						#print(temp)
					
					
				#hypothesisSpace = originalSpace
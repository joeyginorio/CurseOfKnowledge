import csv
#import sys
#sys.path.append("..")



reader = csv.reader(open('Practice.csv', newline = ''), delimiter = ',')
inputList = list()


for row in reader:
	counter = 0
	rowTotal = 0
	rowTemp = list()
	for i in row:
		print(float(i))

		if isinstance(i, float) or str.isdigit(str(i)):
			rowTotal = rowTotal + float(i)
			counter +=1
			print('rowtotal, counter', rowTotal, counter)
		#inputList.append(rowTotal/counter)
	print(inputList)





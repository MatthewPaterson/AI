def movingAverage(filename,moving):
	# openfile = file(filename, 'r+')
	# size = 2400
	# f
	counter = 0 
	
	with open(filename) as f:
		lines = f.read().splitlines()

	newfile = open('laboratory5MovingAverage.txt','r+')

	while counter<2400:
		total = 0
		start = counter-5
		end = counter+6

		total = lines[start:end]
		print total
		total = map(int,total)

		total = sum(total)

		total = total/11
		print total

		newfile.write(str(total)+"\n")
		counter+=1

movingAverage('laboratory.txt',5)
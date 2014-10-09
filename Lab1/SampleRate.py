def sampleRate(filename):
	counter = 0
	openfile = file(filename, 'r')
	for line in openfile:
		counter = counter + 1
	return counter/0.3

print sampleRate('laboratory.txt')

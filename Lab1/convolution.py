import numpy

def convolve(filename,window):
	counter = 0 
	with open(filename) as f:
		lines = f.read().splitlines()

	newfile = open('laboratory5Convolution.txt','r+')

	# while counter<2400:
	# 	total = 0

	# 	total = lines[(counter):(counter+80)]
	# 	print total
	# 	total = map(int,total)
	# 	total = sum(total)
	# 	print total

	# 	newfile.write(str(total)+"\n")
	# 	counter+=1

	total = 0
	counter = 0
	window_size = window * 8
	while (counter < len(lines)):
		print lines
		if (counter-window) < 0:
			signal = 0
		else:
			signal = lines[counter-window]

		total += int(signal)
		counter+=1
		newfile.write(str(total)+"\n")

def main():
	convolve("laboratory.txt",10)

main()


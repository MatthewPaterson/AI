import numpy,os,math,itertools
import matplotlib.pyplot as plt



def movingAverage(filename,moving):

	counter = 0 
	
	with open(filename) as f:
		lines = f.read().splitlines()

	newfile = open('laboratory5MovingAverage.txt','r+')

	while counter<len(lines):
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


def convolve(filename,window):
	counter = 0 
	with open(filename) as f:
		lines = f.read().splitlines()
	newfile = open('laboratory5Convolution.txt','r+')

	while counter<len(lines):
		total = 0
		window = counter - 80
		start = max(0,window)
		total = lines[(start):(counter)]
		
		total = map(int,total)
		total = sum(total)

		# newfile.write(str(total)+"\n")
		counter+=1

def energy(lines,window):
	counter = 0 
	# with open(filename) as f:
	# 	lines = f.read().splitlines()
	# newfile = open('laboratoryEnergy.txt','r+')
	lists=[]
	while counter<len(lines):

		total = 0
		window = counter - 80
		start = max(0,window)
		total = lines[(start):(counter)]
		total = map(int,total)
		total = sum(total)
		total = total**2
		lists += [total]
		# newfile.write(str(total)+"\n")
		counter+=1
	return lists

def magnitude(lines,window):
	counter = 0 
	# with open(filename) as f:
	# 	lines = f.read().splitlines()
	# newfile = open('laboratoryMagnitude.txt','r+')
	lists = []
	while counter<len(lines):
		total = 0
		window = counter - 80
		start = max(0,window)
		total = lines[(start):(counter)]
		total = map(int,total)
		total = sum(total)
		total = abs(total)
		lists += [total]

		# newfile.write(str(total)+"\n")
		counter+=1
	return lists

def delayOp(filename,delay):

	openfile = open(filename, 'r+')
	buffer = ""
	buffer += openfile.read()
	openfile.close()

	counter = 0
	newfile = open('laboratory15.txt','r+')
	while counter <= ((8*delay)-1):
		newfile.write('0\n')
		counter += 1
	else:
		newfile.write(buffer)



def sampleRate(filename):
	counter = 0
	openfile = file(filename, 'r')
	for line in openfile:
		counter = counter + 1

	return counter/0.3


def sign(val):
	x = 0
	if int(val) >= 0:
		x = 1

	return x

# def zcr(lines,filename,window):
# 	sign_change = 0
# 	last_sign = 1
# 	counter = 0 
# 	total = 0
# 	counter = 0
# 	lists = []
# 	while (counter < len(lines)):

# 		window = counter - 80
# 		start = max(0,window)
# 		total = lines[(start):(counter)]

# 		#for x in total:
# 		i = start
# 		sy = 0
# 		while start < counter:

# 			y = sign(lines[start]) - sign(lines[start-1])

# 			start += 1
# 			sy += y
		
# 		print (sy)
# 		lists += [sy]
# 		counter +=1

# 		plt.plot(lists)

def zcr(lines, window):

	x = 0
	lists = []
	while x < len(lines):

		summation = 0

		low = max(1, x-80)

		# Over window
		while low < x:
			val = sign(lines[low]) - sign(lines[low - 1])
			summation += abs(val)

			low += 1

		#output = (1 / (2 * 80)) * summation
		lists.append(summation)
		x += 1
	return lists


def feature_value():
	list_energy = []
	list_magnitude = []
	list_zcr = []
	list_file = []
	for root,dirs,files in os.walk("/users/level4/1102374p/AI/Lab1/samples/"):
		for f in files:
			with open("/users/level4/1102374p/AI/Lab1/samples/"+f) as line:
				lines = []
				lines = line.read().splitlines()
			fn = os.path.splitext(f)[0]
			list_file += [fn]

			short_energy = energy(lines,30)
			short_magnitude = magnitude(lines,30)
			z = zcr(lines,30)

			energy_average = numpy.mean(short_energy)
			magnitude_average = numpy.mean(short_magnitude)
			zcr_average = numpy.mean(z)


			log_energy = math.log10(energy_average)
			log_magnitude = math.log10(magnitude_average)
			list_energy += [log_energy]
			list_magnitude += [log_magnitude]
			list_zcr += [zcr_average]

	zipped_list = zip(list_energy,list_magnitude,list_zcr)

	for i in range(len(list_file)):
		file = open(list_file[i]+".txt",'w')
		file.write(str(zipped_list[i][0]) + '\n')
		file.write(str(zipped_list[i][1]) + '\n')
		file.write(str(zipped_list[i][2]) + '\n')
		file.close()




	return




def main():
	feature_value()
	# convolve("laboratory.txt",10)
	# sampleRate("laboratory.txt")
	# delayOp("laboratory.txt",10)
	# magnitude("laboratory.txt",30)
	# energy("laboratory.txt",30)
	# movingAverage("laboratory.txt",10)
	# zcr("laboratory.txt",30)
main()


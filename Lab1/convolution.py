import numpy,os,math,itertools,random
import matplotlib.pyplot as plt
import pylab

def movingAverage(lines,moving):

	# Calculates the moving average of the signal
	# Returns signal in form of a list.
	moving = []
	counter = 0 
	while counter<len(lines):
		total = 0
		start = counter-5
		end = counter+6

		total = lines[start:end]
		total = map(int,total)
		total = sum(total)
		total = total/11

		moving.append(total)
		counter+=1
	return moving

def convolve(lines,window):
	convolution = []
	counter = 0 

	while counter<len(lines):
		total = 0
		window = counter - 240
		# Need to include "start" as otherwise list will loop to the end of the list
		start = max(0,window)
		# Will only loop through the range of values in the list.
		for sample in lines[(start):(counter)]:
			total += int(sample)
		convolution.append(total)
		counter+=1
	return convolution

def energy(lines,window):
	# Calculates the energy over the window
	# Same as convolution except each value is squared  before being added together.
	counter = 0 
	energies=[]
	while counter<len(lines):
		total = 0
		window = counter - 240
		start = max(0,window)
		for sample in lines[(start):(counter)]:
		 	total += int(sample)**2
		energies.append(total)
		counter+=1
	return energies

def magnitude(lines,window):
	# Calculates the short-term magnitude of the signal
	# Same as convolution except taking the absolute value before being added together.
	counter = 0 
	mag = []
	while counter<len(lines):
		total = 0
		window = counter - 240
		start = max(0,window)
		for sample in lines[(start):(counter)]:
			total += abs(int(sample))
		mag.append(total)

		counter+=1
	return mag

def delayOp(lines,delay):
	# Will append "0" onto the start of the signal
	delay = [0]*(delay*8) + lines
	return delay

def sign(val):

	# Will return 1 or 0
	# Used for ZCR
	x = 0
	if int(val) >= 0:
		x = 1
	return x

def zcr(lines, window):

	counter = 0
	lists = []
	while counter < len(lines):

		total = 0
		window = counter-240
		# Start is now 1 otherwise will error.
		start = max(1, window)
		while start < counter:
			val = sign(lines[start]) - sign(lines[start - 1])
			total += abs(val)

			start += 1
		lists.append(total)
		counter += 1
	return lists

def feature_value():

	# This was only used once as was quicker to read in files 
	# Than continually recall this function

	list_energy = []
	list_magnitude = []
	list_zcr = []
	list_file = []

	# Crawls through the directory of silence and speech files
	for root,dirs,files in os.walk("/users/level4/1102374p/AI/Lab1/samples/"):
		for f in files:
			with open("/users/level4/1102374p/AI/Lab1/samples/"+f) as line:
				lines = []
				lines = line.read().splitlines()
			fn = os.path.splitext(f)[0]
			# Keeps a list of filenames
			list_file += [fn]

			# For each file, calculates the energy, magnitude and zcr
			short_energy = energy(lines,30)
			short_magnitude = magnitude(lines,30)
			z = zcr(lines,30)

			# Find the average value of the energy, magnitude and zcr
			energy_average = numpy.mean(short_energy)
			magnitude_average = numpy.mean(short_magnitude)
			zcr_average = numpy.mean(z)

			#  Finds the log10 of energy and magnitude
			log_energy = math.log10(energy_average)
			log_magnitude = math.log10(magnitude_average)
			list_energy += [log_energy]
			list_magnitude += [log_magnitude]
			list_zcr += [zcr_average]

	# Zips the three lists together to create a 2d list each containing
	# log10 energy, log10 magnitude and average zcr for each file

	zipped_list = zip(list_energy,list_magnitude,list_zcr)

	# writes each tuple to a new file.
	for i in range(len(list_file)):
		file = open(list_file[i]+".txt",'w')
		file.write(str(zipped_list[i][0]) + '\n' + str(zipped_list[i][1]) + '\n' + str(zipped_list[i][2]))
		file.close()
	return

def read():
	list_energy = []
	list_magnitude = []
	list_zcr = []
	list_type = []
	# Crawls through the list of files that were previously created in "feature_value()"
	for root,dirs,files in os.walk("/users/level4/1102374p/AI/Lab1/files/"):
		for f in files:
			with open("/users/level4/1102374p/AI/Lab1/files/"+f) as line:

				lines = []
				lines = line.read().splitlines()
				list_energy.append(lines[0])
				list_magnitude.append(lines[1])
				list_zcr.append(lines[2])
				if f.startswith("silence"):
					# If the file was silence then a new value was entered. Either 0 or 1
					list_type.append(0)
				else:
					list_type.append(1)
	# Splits the tuples back into separate lists
	return list_energy,list_magnitude,list_zcr,list_type


def kfold(energy,magnitude,zcr,types,k,used):

	random_sound = []
	random_silence = []
	i = 0 
	zipped = zip(energy,magnitude,zcr,types)

	# Splits the new list into half, the first being sound
	# Take 5 samples randomly from each list
	sound = zipped[0:50]
	silence = zipped[50:100]

	while i < 5:
		temp1 = random.choice(sound)
		temp2 = random.choice(silence)
		if temp1 not in used:
			if temp2 not in used:
				random_sound.append(temp1)
				random_silence.append(temp2)
				used.append(temp1)
				used.append(temp2)
				i += 1

	test_set = random_sound + random_silence

	random.shuffle(test_set)

	# Remove test_set from the training set.
	for i in zipped[:]:
		if i in test_set:
			zipped.remove(i)


	sound = zipped[0:45]
	no_sound = zipped[45:90]

	return sound,no_sound,test_set,used

def average(samples):
	# Calculates the average values
	e_average = 0
	m_average = 0
	z_average = 0 

	for i in range(len(samples)):
		e_average += float(samples[i][0])
		m_average += float(samples[i][1])
		z_average += float(samples[i][2])

	e_average = e_average/len(samples)
	m_average = m_average/len(samples)
	z_average = z_average/len(samples)

	return e_average,m_average,z_average

def deviation(samples,e_average,m_average,z_average):

	# Calculates how much each value deviates from the mean and then sums them
	# to find the variance
	e_dev = []
	m_dev = []
	z_dev = []
	t_dev = []

	for i in range(len(samples)):
		e_dev.append(((float(samples[i][0]) - e_average))**2)
		m_dev.append(((float(samples[i][1]) - m_average))**2)
		z_dev.append(((float(samples[i][2]) - z_average))**2)
		t_dev.append(samples[i][3])

	e_var = sum(e_dev)/(len(samples))
	m_var = sum(m_dev)/(len(samples))
	z_var = sum(z_dev)/(len(samples))

	return e_var,m_var,z_var


def probability(e_var, m_var, z_var, test_set, e_average, m_average, z_average):

	# Calculates the probability of the e m and z values.

	probability_e = (1/numpy.sqrt(2*math.pi*e_var)) * math.exp( (-(float(test_set[0])-e_average)**2) / (2*(e_var)**2) )
	probability_m = (1/numpy.sqrt(2*math.pi*m_var)) * math.exp( (-(float(test_set[1])-m_average)**2) / (2*(m_var)**2) )
	probability_z = (1/numpy.sqrt(2*math.pi*z_var)) * math.exp( (-(float(test_set[2])-z_average)**2) / (2*(z_var)**2) )

	prob = 0.5*probability_e*probability_m*probability_z
	return prob

def main():






	# Main() code for part 1

	filename = "/users/level4/1102374p/AI/Lab1/laboratory.txt"
	lines = []
	with open(filename) as f:
		lines = f.read().splitlines()

	# sample_rate = len(lines)/0.3
	# moving = movingAverage(lines,10)
	# delay = delayOp(lines,30)
	energies = energy(lines,30)
	mag = magnitude(lines,30)
	z = zcr(lines,30)
	# conv = convolve(lines,30)

	lines = map(float,lines)
	z = map(float,z)
	maxe = max(z)
	maxl = max(lines)

	newe=[]
	new=[]

	for i in range(len(z)):
		new.append(lines[i]/maxl)
		newe.append(z[i]/maxe)

	plt.figure()

	plt.plot(new,color='blue')
	plt.plot(newe,color='red')
	plt.show()
	# Main() code for part2
	# Used to get log e, log m and average zcr and put into files.
	# Only used once as function is slow to complete.
	# feature_value()
	# used = []
	# correct = 0 
	# incorrect = 0
	# energy,magnitude,zcr,types = read()


	# # Maps all values to floats
	# energy = map(float,energy)
	# magnitude = map(float,magnitude)
	# zcr = map(float,zcr)

	# for i in range(10):
	#  	sound,no_sound,test_set,used = kfold(energy,magnitude,zcr,types,10,used)

	# 	e_average_sound,m_average_sound,z_average_sound = average(sound)
	# 	e_average_no_sound,m_average_no_sound,z_average_no_sound = average(sound)

	# 	e_var_sound,m_var_sound,z_var_sound = deviation(sound, e_average_sound, m_average_sound, z_average_sound)
	# 	e_var_no_sound,m_var_no_sound,z_var_no_sound = deviation(no_sound, e_average_no_sound, m_average_no_sound, z_average_no_sound)

	# 	for r in range(10):
	# 		prob_sound = probability(e_var_sound, m_var_sound, z_var_sound,test_set[r], e_average_sound, m_average_sound, z_average_sound)
	# 		prob_no_sound = probability(e_var_no_sound, m_var_no_sound, z_var_no_sound,test_set[r], e_average_no_sound, m_average_no_sound, z_average_no_sound)

	# 		# Find the posterior of being sound or not sound/
	# 		posterior_sound = prob_sound/(prob_sound + prob_no_sound)
	# 		posterior_no_sound = prob_no_sound/(prob_sound + prob_no_sound)

	# 		# Adds up the number of correct and incorrect guesses of the classifier
	# 		if  (posterior_no_sound > posterior_sound) and test_set[r][3] == 0:
	# 			correct += 1
	# 		elif(posterior_sound > posterior_no_sound) and test_set[r][3] == 1:
	# 			correct += 1
	# 		elif(posterior_sound > posterior_no_sound) and test_set[r][3] == 0:
	# 			incorrect += 1
	# 		else:
	# 			incorrect += 1
	# # Output.
	# print "Percentage guessed correctly: " + str(correct) +"%"
	# print "Percentage guessed incorrectly: " + str(incorrect) +"%" 


main()


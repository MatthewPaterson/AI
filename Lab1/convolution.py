import numpy,os,math,itertools,random
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold





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


def zcr(lines, window):

	x = 0
	lists = []
	while x < len(lines):

		summation = 0

		low = max(1, x-80)

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

def read():
	list_energy = []
	list_magnitude = []
	list_zcr = []
	list_type = []

	for root,dirs,files in os.walk("/users/level4/1102374p/AI/Lab1/files/"):
		for f in files:
			with open("/users/level4/1102374p/AI/Lab1/files/"+f) as line:


				lines = []
				lines = line.read().splitlines()
				list_energy.append(lines[0])
				list_magnitude.append(lines[1])
				list_zcr.append(lines[2])
				if f.startswith("silence"):
					list_type.append(0)
				else:
					list_type.append(1)

	return list_energy,list_magnitude,list_zcr,list_type


def kfold(energy,magnitude,zcr,types,k):
	random_sound = []
	random_silence = []

	e_dev_sound = []
	m_dev_sound = []
	z_dev_sound = []
	t_dev_sound = []

	e_dev_no_sound = []
	m_dev_no_sound = []
	z_dev_no_sound = []
	t_dev_no_sound = []

	e_average_sound = 0
	m_average_sound = 0 
	z_average_sound = 0

	e_average_no_sound = 0
	m_average_no_sound = 0 
	z_average_no_sound = 0

	zipped = zip(energy,magnitude,zcr,types)

	sound = zipped[0:50]
	silence = zipped[50:100]

	for i in range(5):
		temp1 = random.choice(sound)
		temp2 = random.choice(silence)
		random_sound.append(temp1)
		random_silence.append(temp2)

	test_set = random_sound + random_silence

	for i in zipped[:]:
		if i in test_set:
			zipped.remove(i)

	sound = zipped[0:45]
	no_sound = zipped[45:90]

	for i in range(len(sound)):
		e_average_sound += float(sound[i][0])
		m_average_sound += float(sound[i][1])
		z_average_sound += float(sound[i][2])

	e_average_sound = e_average_sound/len(sound)
	m_average_sound = m_average_sound/len(sound)
	z_average_sound = z_average_sound/len(sound)

	for i in range(len(no_sound)):
		e_average_no_sound += float(no_sound[i][0])
		m_average_no_sound += float(no_sound[i][1])
		z_average_no_sound += float(no_sound[i][2])

	e_average_no_sound = e_average_no_sound/len(no_sound)
	m_average_no_sound = m_average_no_sound/len(no_sound)
	z_average_no_sound = z_average_no_sound/len(no_sound)











	for i in range(len(sound)):
		e_dev_sound.append(((float(sound[i][0]) - e_average_sound))**2)
		m_dev_sound.append(((float(sound[i][1]) - m_average_sound))**2)
		z_dev_sound.append(((float(sound[i][2]) - z_average_sound))**2)
		t_dev_sound.append(sound[i][3])

	for i in range(len(no_sound)):
		e_dev_no_sound.append(((float(no_sound[i][0]) - e_average_no_sound))**2)
		m_dev_no_sound.append(((float(no_sound[i][1]) - m_average_no_sound))**2)
		z_dev_no_sound.append(((float(no_sound[i][2]) - z_average_no_sound))**2)
		t_dev_no_sound.append(no_sound[i][3])

	e_var_sound = sum(e_dev_sound)/(len(sound)-1)
	m_var_sound = sum(m_dev_sound)/(len(sound)-1)
	z_var_sound = sum(z_dev_sound)/(len(sound)-1)

	e_var_no_sound = sum(e_dev_no_sound)/(len(no_sound)-1)
	m_var_no_sound = sum(m_dev_no_sound)/(len(no_sound)-1)
	z_var_no_sound = sum(z_dev_no_sound)/(len(no_sound)-1)



	probability_e_sound = (1/numpy.sqrt(2*math.pi*e_var_sound)) * math.exp( (-(float(test_set[6][0])-e_average_sound)**2) / (2*(e_var_sound)**2) )
	probability_m_sound = (1/numpy.sqrt(2*math.pi*m_var_sound)) * math.exp( (-(float(test_set[6][1])-m_average_sound)**2) / (2*(m_var_sound)**2) )
	probability_z_sound = (1/numpy.sqrt(2*math.pi*z_var_sound)) * math.exp( (-(float(test_set[6][2])-z_average_sound)**2) / (2*(z_var_sound)**2) )

	probability_e_nosound = (1/numpy.sqrt(2*math.pi*e_var_no_sound)) * math.exp( (-(float(test_set[6][0])-e_average_no_sound)**2) / (2*(e_var_no_sound)**2) )
	probability_m_nosound = (1/numpy.sqrt(2*math.pi*m_var_no_sound)) * math.exp( (-(float(test_set[6][1])-m_average_no_sound)**2) / (2*(m_var_no_sound)**2) )
	probability_z_nosound = (1/numpy.sqrt(2*math.pi*z_var_no_sound)) * math.exp( (-(float(test_set[6][2])-z_average_no_sound)**2) / (2*(z_var_no_sound)**2) )

	prob_sound   = 0.5* probability_e_sound*probability_m_sound*probability_z_sound
	prob_nosound = 0.5* probability_e_nosound*probability_m_nosound*probability_z_nosound

	posterior_sound = prob_sound/(prob_sound+prob_nosound)
	posterior_no_sound = prob_nosound/(prob_sound+prob_nosound)
	print test_set[6]
	print posterior_sound
	print posterior_no_sound
def main():

	energy,magnitude,zcr,types = read()
	kfold(energy,magnitude,zcr,types,10)

	# feature_value()
	# convolve("laboratory.txt",10)
	# sampleRate("laboratory.txt")
	# delayOp("laboratory.txt",10)
	# magnitude("laboratory.txt",30)
	# energy("laboratory.txt",30)
	# movingAverage("laboratory.txt",10)
	# zcr("laboratory.txt",30)
main()


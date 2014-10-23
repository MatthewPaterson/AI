import numpy

def convolve(filename,window):
	counter = 0 
	with open(filename) as f:
		lines = f.read().splitlines()

	newfile = open('LaboratoryEnergy.txt','r+')

	while counter<2400:
		total = 0

		total = lines[(counter):(counter+(window*5))]
		
		total = map(int,total)

		total = sum(total)
		print total**2

		newfile.write(str(total)+"\n")
		counter+=1

		





def main():
	convolve("laboratory.txt",30)

main()
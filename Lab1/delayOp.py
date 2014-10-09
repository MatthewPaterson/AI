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

			





delayOp('laboratory.txt',15)

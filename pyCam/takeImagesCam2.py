import sys
import time
import serial

BAUD = 38400 
PORT = "/dev/ttyO1"      # change this to your com port!
TIMEOUT = 0.2

SERIALNUM = 0x00

COMMANDSEND = 0x56
COMMANDEND = 0x00

CMD_GETVERSION = 0x11
CMD_RESET = 0x26

FBUF_CTRL = [ COMMANDSEND, SERIALNUM, 0x36, 0x01, 0x00]
GET_FBUF_LEN = [ COMMANDSEND, SERIALNUM, 0x34, 0x01]
READ_FBUF = [ COMMANDSEND, SERIALNUM, 0x32, 0x0c]

getDataCmd = [COMMANDSEND, 0x00, 0x32, 0x0c, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
getversioncommand = [COMMANDSEND, SERIALNUM, CMD_GETVERSION, COMMANDEND]
systemresetcommand = [COMMANDSEND, SERIALNUM, CMD_RESET, COMMANDSEND]

def checkreply(r, b):
	try:
		r = map (ord, r)
		print r
		if (r[0] == 0x76 and r[1] == SERIALNUM and r[2] == b and r[3] == 0x00):
			print "\tcheck reply is true"
			return True
		else:
			print "\tcheck reply is false"
	except:
		e = sys.exc_info()[0]
		print "checkreply error"
		print e
	return False

def sendCommand(cmd, rply_hex):
	cmd = ''.join (map (chr, cmd))
	print "sending................"
	print cmd
	s.write(cmd)
	time.sleep(1)
	reply = s.read(100)
	print "reply.................."
	print reply
	print "end of reply..........."
	r = list(reply)
	if (checkreply(r, rply_hex)):
		return True
	return False   

def controlFrame(fbuf_ctrl_cmd, ctrl_code):
	fbuf_ctrl_cmd[-1] = ctrl_code
	print "frame controlling"
	print fbuf_ctrl_cmd
	cmd_b = ''.join(map(chr, fbuf_ctrl_cmd))
	s.write(cmd_b)
	time.sleep(1)
	reply = s.read(5)
	rp = map(ord, list(reply))
	print rp
	if rp[3] == 0x00:
		print "frame control success"
		return True
	return False

def getBufferLen(get_fbuf_cmd, fbuf_type):
	get_fbuf_cmd.append(fbuf_type)
	cmd_b = ''.join(map(chr, get_fbuf_cmd))
	s.write(cmd_b)
	time.sleep(1)
	reply = s.read(9)
	rp = map(ord, list(reply))
	print rp
	if rp[3] == 0x00:
		print "get buffer length success"
		print rp[len(rp)-4:]
		return rp[len(rp)-4:] 
	return

def readBuffer(*args, **kwargs):
	# flatten the list
	read_fbuf_cmd = []
	for arg in args:
		try:
			read_fbuf_cmd.extend(arg)
		except TypeError:
			read_fbuf_cmd.append(arg)
	highbit = kwargs['highbit'] 
	lowbit = kwargs['lowbit']
	
	print "reading buffer"
	print read_fbuf_cmd
	cmd = ''.join(map(chr, read_fbuf_cmd))
	s.write(cmd)
	time.sleep(1)

	length = highbit << 8 | lowbit
	print length
	reply = s.read(length + 10000)
	rp = map(ord, list(reply))

	dataStart = [0x76, 0x00, 0x32, 0x00, 0x00, 0xFF, 0xD8]
	dataEnd = [0xFF, 0xD9, 0x76, 0x00, 0x32, 0x00, 0x00]

	if rp[:7] == dataStart and rp[len(rp)-7:] == dataEnd:
		print "image data received"
		return rp[5:len(rp)-5]
	return
	
######## main ################

s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
#sendCommand(systemresetcommand, 0x26)

sendCommand(getversioncommand, 0x11)

for i in range(2):
	# Send FBUF_CTRL command to stop current frame updating, the parameter is 0x00.
	controlFrame(FBUF_CTRL, 0x00)

	# Send GET_FBUF_LEN command to get image lengths in FBUF.
	buff_len = getBufferLen(GET_FBUF_LEN, 0x00)

	# Send READ_FBUF to read image data, the parameters are as follows in READ_FBUF command.
	# the FBUF frame type is 0x00
	# control mode is 0x0F
	# starting address is 0x00
	# the image data is the one that we get with GET_FBUF_LEN command.
	# delay time is used to prolong the time between image data and return command,
	#	the default value is 3000 , and can be modified. 
	if buff_len:
		buff = readBuffer(READ_FBUF, 0x00, 0x0A, 
							0x00, 0x00, 0x00, 0x00, 
							buff_len,
							0x01,0x00, # delay
							highbit=buff_len[2],
							lowbit=buff_len[3])

		if buff:
			with open("image" + str(i) + ".jpg", 'w') as f:
				for i in buff:
					f.write(chr(i))
			print "got photo :D"

		# After all have finished, we need to send FBUF_CTRL command to resume frame,
		# the parameter is 0x02
		controlFrame(FBUF_CTRL, 0x02)
	time.sleep(1)


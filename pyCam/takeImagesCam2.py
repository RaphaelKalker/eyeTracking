import sys
import time
import serial
import copy

BAUD = 38400 
PORT = "/dev/ttyO4"      # change this to your com port!
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

setBaudRateCmd = [0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x00, 0x00]
baudrates = {115200: [0x1A,0x26], 38400: [0x2A, 0xF2]}

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

def getVersion(cmd, replyCheck):
	rp = serialComm(cmd, 100)
	if rp[2] == replyCheck:
		return True
	return False   

def controlFrame(fbuf_ctrl_cmd, ctrl_code):
	fbuf_ctrl_cmd[-1] = ctrl_code
	rp = serialComm(fbuf_ctrl_cmd, 5)

	if rp[3] == 0x00:
		return True
	return False

def getBufferLen(get_fbuf_cmd, fbuf_type):
	get_fbuf = get_fbuf_cmd
	get_fbuf.append(fbuf_type)

	rp = serialComm(get_fbuf_cmd, 9)

	if rp[3] == 0x00:
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
	length = highbit << 8 | lowbit
	
	print "reading buffer"
	rp = serialComm(read_fbuf_cmd, length+10000)

	dataStart = [0x76, 0x00, 0x32, 0x00, 0x00, 0xFF, 0xD8]
	dataEnd = [0xFF, 0xD9, 0x76, 0x00, 0x32, 0x00, 0x00]

	if rp[:7] == dataStart and rp[len(rp)-7:] == dataEnd:
		print "image data received"
		return rp[5:len(rp)-5]
	return

def setBaudRate(rate):
	setBaudRateCmd[len(setBaudRateCmd)-2:] = baudrates[rate]
	rp = serialComm(setBaudRateCmd, 10)
	
def setImageSize():
	setSizeCmd = [ 0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19, 0x22]
	return serialComm(setSizeCmd, 10)

def setImageCompression(ratio):
	compCmd = [0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x1A, ratio ]
	return serialComm(compCmd, 10)

def serialComm(cmd_list, readLen):
	cmd = ''.join(map(chr,cmd_list))
	s.write(cmd)
	reply = s.read(readLen)
	rp = map(ord, list(reply))
	return rp

s = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
getVersion(getversioncommand, 0x11)

# Resume frame to "start" the camera
controlFrame(FBUF_CTRL, 0x02)

# Currently only sets to 160x120
setImageSize()

# Compression ratio is between 0x00 to 0xFF
setImageCompression(0x26)

setBaudRate(115200)
serial.baudrate = 115200

for i in range(1):
	# Send FBUF_CTRL command to stop current frame updating, the parameter is 0x00.
	controlFrame(FBUF_CTRL, 0x00)

	# Send GET_FBUF_LEN command to get image lengths in FBUF.
	buff_len = getBufferLen(GET_FBUF_LEN, 0x00)

	# READ_FBUF to get the image data
	if buff_len:
		buff = readBuffer(READ_FBUF, 0x00, 0x0A, 
							0x00, 0x00, 0x00, 0x00, 
							buff_len,
							0x01, 0x00, # delay
							highbit=buff_len[2],
							lowbit=buff_len[3])

		if buff:
			with open("./output/cam2/image" + str(int(time.time())) + ".jpg", 'w') as f:
				for i in buff:
					f.write(chr(i))
			print "got photo :D"

		# Send FBUF_CTRL command to resume frame,
		controlFrame(FBUF_CTRL, 0x02)

setBaudRate(38400)

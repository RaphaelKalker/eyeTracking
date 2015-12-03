import sys
import time
import serial
import copy

class Cam1():
	def __init__(self, outputDir ):
		self.opDir = outputDir
		# Initialize camera
		self.conn = serial.Serial("/dev/ttyO4", baudrate=38400)

		#reset the camera
		self.conn.write(b'\x56\0\x26\0')

		resp = ""
		time.sleep(0.5)
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data

		print " ".join(hex(ord(n)) for n in resp)
		    
		if "Init end\r\n" in resp:
		   print "Ready"


		#lower image size to 160x120
		self.conn.write(b'\x56\0\x31\x05\x04\x01\x00\x19\x22')

		resp = ""
		time.sleep(0.5)
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data
		print " ".join(hex(ord(n)) for n in resp)

		#increase compression ratio
		self.conn.write(b'\x56\0\x31\x05\x01\x01\x12\x04\x25')

		resp = ""
		time.sleep(0.5)
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data
		print " ".join(hex(ord(n)) for n in resp)

		#change baud rate to 115200
		self.conn.write(b'\x56\0\x24\x03\x01\x0d\0xa6')

		resp = ""
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data

		print " ".join(hex(ord(n)) for n in resp)

		#change the baudrate set earlier
		self.conn.baudrate = 115200
		print "camera 1 init finished"

	def takeImg(self): 
		#take photo
		self.conn.write(b'\x56\0\x36\x01\0')
		resp = ""
		time.sleep(0.5)
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data
		print resp

		if b'\x76\0\x36\0\0' in resp:
		    print "Picture taken"

	def getImg(self):
		#Get JPG size
		self.conn.write(b'\x56\0\x34\x01\0')
		resp = ""
		time.sleep(0.5)
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data
		    if b'\x76\0\x34\0\x04\0\0' in resp:
			msb = self.conn.read()
			lsb = self.conn.read()
			size = (ord(msb) << 8 | ord(lsb))
		print "picture size response"
		print resp

		# Write image to file
		self.conn.write(b'\x56\0\x32\x0C\0\x0A\0\0\0\0\0\0%c%c\0\x0A' % (msb,lsb))
		resp = self.conn.read(5)
		if b'\x76\0\x32\0\0' in resp:
#			buff = self.conn.read(size)  #might work
			fileName = self.opDir + "R" +str(int(time.time())) + ".jpg"
			with open(fileName, 'wb') as f:
				while (self.conn.inWaiting() > 0):
				    data = self.conn.read()
				    f.write('%c' % data)
			print "Image written to output/%s" % (fileName)
			return fileName

	def closeConn(self):
		#change baud rate to 38400 (default)
		self.conn.write(b'\x56\0\x24\x03\x01\x2a\0xf2')

		resp = ""
		while (self.conn.inWaiting() > 0):
		    data = self.conn.read()
		    resp += data

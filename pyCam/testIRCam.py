import serial
import time
import datetime

# Initialize camera
serial = serial.Serial("/dev/ttyO4", baudrate=38400)

#reset the camera
serial.write(b'\x56\0\x26\0')

resp = ""
time.sleep(1)
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data

print " ".join(hex(ord(n)) for n in resp)
    
if "Init end\r\n" in resp:
   print "Ready"
#  break


#lower image size to 160x120
serial.write(b'\x56\0\x31\x05\x04\x01\x00\x19\x22')

resp = ""
time.sleep(1)
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data
print " ".join(hex(ord(n)) for n in resp)

#increase compression ratio
serial.write(b'\x56\0\x31\x05\x01\x01\x12\x04\x25')

resp = ""
time.sleep(1)
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data
print " ".join(hex(ord(n)) for n in resp)

#change baud rate to 115200
serial.write(b'\x56\0\x24\x03\x01\x0d\0xa6')

resp = ""
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data

#print " ".join(hex(ord(n)) for n in resp)

#change the baudrate set earlier
serial.baudrate=115200

#take photo
serial.write(b'\x56\0\x36\x01\0')
resp = ""
time.sleep(1)
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data

if b'\x76\0\x36\0\0' in resp:
    print "Picture taken"
#break

#Get JPG size
serial.write(b'\x56\0\x34\x01\0')
resp = ""
time.sleep(1)
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data
    if b'\x76\0\x34\0\x04\0\0' in resp:
        msb = serial.read()
        lsb = serial.read()
        print "Image file size: %d bytes" % (ord(msb) << 8 | ord(lsb))

# Write image to file
serial.write(b'\x56\0\x32\x0C\0\x0A\0\0\0\0\0\0%c%c\0\x0A' % (msb,lsb))
#time.sleep(3)
now = datetime.datetime.now()
filename = "%d.%02d.%02d.%02d.%02d.%02d.jpg" % (now.year,now.month,now.day,now.hour,now.minute,now.second)
resp = serial.read(size=5)
if b'\x76\0\x32\0\0' in resp:
    with open("output/cam1/" + filename, 'wb') as f:
        while (serial.inWaiting() > 0):
            data = serial.read()
            f.write('%c' % data)
print "Image written to output/%s" % (filename)

#change baud rate to 38400 (default)
serial.write(b'\x56\0\x24\x03\x01\x2a\0xf2')

resp = ""
while (serial.inWaiting() > 0):
    data = serial.read()
    resp += data

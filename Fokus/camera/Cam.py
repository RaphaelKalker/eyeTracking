import sys
import time
import serial
import copy
import logging

logger = logging.getLogger(__name__)

BAUD = 38400
TIMEOUT = 0.2

SERIALNUM = 0x00

COMMANDSEND = 0x56
COMMANDEND = 0x00

CMD_GETVERSION = 0x11
CMD_RESET = 0x26

FBUF_CTRL = [COMMANDSEND, SERIALNUM, 0x36, 0x01, 0x00]
GET_FBUF_LEN = [COMMANDSEND, SERIALNUM, 0x34, 0x01]
READ_FBUF = [COMMANDSEND, SERIALNUM, 0x32, 0x0c]

getDataCmd = [COMMANDSEND, 0x00, 0x32, 0x0c, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
getversioncommand = [COMMANDSEND, SERIALNUM, CMD_GETVERSION, COMMANDEND]
systemresetcommand = [COMMANDSEND, SERIALNUM, CMD_RESET, COMMANDSEND]

setBaudRateCmd = [0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x00, 0x00]
baudrates = {115200: [0x1A, 0x26], 38400: [0x2A, 0xF2]}


class Cam():
    def __init__(self, outputDir, side):
        self.opDir = outputDir

        self.eyeSide = side
        if side == 'L':
            port_num = 1
        elif side == 'R':
            port_num = 4

        PORT = "/dev/ttyO" + str(port_num)
        logger.info("About to set port: %s", PORT)

        self.conn = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
        logger.info("port: %s", PORT)

        self.getVersion(getversioncommand, 0x11)

        # Resume frame to "start" the camera
        self.controlFrame(FBUF_CTRL, 0x02)

        # Currently only sets to 160x120
        self.setImageSize()

        # Compression ratio is between 0x00 to 0xFF
        self.setImageCompression(0x26)
        self.setBaudRate(115200)
        logger.info("init successful")


    def checkreply(self, r, b):
        try:
            r = map(ord, r)
            if (r[0] == 0x76 and r[1] == SERIALNUM and r[2] == b and r[3] == 0x00):
                logger.warning("check reply is true")
                return True
            else:
                logger.warning("check reply is false")
        except:
            e = sys.exc_info()[0]
            logger.error("checkreply error: %s", e)
        return False


    def getVersion(self, cmd, replyCheck):
        rp = self.serialComm(cmd, 100)
        if rp[2] == replyCheck:
            return True
        return False


    def controlFrame(self, fbuf_ctrl_cmd, ctrl_code):
        fbuf_ctrl_cmd[-1] = ctrl_code
        rp = self.serialComm(fbuf_ctrl_cmd, 5)

        if rp[3] == 0x00:
            return True
        return False


    def getBufferLen(self, get_fbuf_cmd, fbuf_type):
        get_fbuf = get_fbuf_cmd
        get_fbuf.append(fbuf_type)
        logger.info('Starting get img')


        rp = self.serialComm(get_fbuf_cmd, 9)

        logger.info('accessing serialcom')


        if rp[3] == 0x00:
            return rp[len(rp) - 4:]
        return


    def readBuffer(self, *args, **kwargs):
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


        rp = self.serialComm(read_fbuf_cmd, length + 10000)
        dataStart = [0x76, 0x00, 0x32, 0x00, 0x00, 0xFF, 0xD8]
        dataEnd = [0xFF, 0xD9, 0x76, 0x00, 0x32, 0x00, 0x00]

        if rp[:7] == dataStart and rp[len(rp) - 7:] == dataEnd:
            logger.info("image data received")
            return rp[5:len(rp) - 5]
        return


    def setBaudRate(self, rate):
        setBaudRateCmd[len(setBaudRateCmd) - 2:] = baudrates[rate]
        rp = self.serialComm(setBaudRateCmd, 10)
        serial.baudrate = rate


    def setImageSize(self):
        setSizeCmd = [0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19, 0x22]
        return self.serialComm(setSizeCmd, 10)


    def setImageCompression(self, ratio):
        compCmd = [0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x1A, ratio]
        return self.serialComm(compCmd, 10)


    def serialComm(self, cmd_list, readLen):
        cmd = ''.join(map(chr, cmd_list))
        logger.info('joined')
        self.conn.write(cmd)
        logger.info('did write')

        reply = self.conn.read(readLen)
        rp = map(ord, list(reply))
        return rp


    def takeImg(self):
        # Send FBUF_CTRL command to stop current frame updating, the parameter is 0x00.
        self.controlFrame(FBUF_CTRL, 0x00)


    def getImg(self, timestamp):
        t1 = time.time()
        # Send GET_FBUF_LEN command to get image lengths in FBUF.
        buff_len = self.getBufferLen(GET_FBUF_LEN, 0x00)



        # READ_FBUF to get the image data
        if buff_len:
            buff = self.readBuffer(READ_FBUF, 0x00, 0x0A,
                                   0x00, 0x00, 0x00, 0x00,
                                   buff_len,
                                   0x01, 0x00,  # delay
                                   highbit=buff_len[2],
                                   lowbit=buff_len[3])

            if buff:
                fileName = self.opDir + self.eyeSide + str(timestamp) + ".jpg"
                with open(fileName, 'w') as f:
                    for i in buff:
                        f.write(chr(i))

            # Send FBUF_CTRL command to resume frame,
            self.controlFrame(FBUF_CTRL, 0x02)
            return fileName
            # return buff


    def closeConn(self):
        self.setBaudRate(38400)

from multiprocessing import Process, Lock, Pipe
import sys
import time
from Analyzer import Analyzer
from actuation import Actuate
import db
from eyeVergence.BinaryTree import DecisionTree
import Utils
import logging

sys.path.insert(0, '../pyCam/')
from camera.Cam import Cam

from learning.ParamsConstructor import ParamsConstructor

__author__ = 'Raphael'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logger = logging.getLogger(__name__)

loggerRetrieval = logging.getLogger("ImageRetrieval")
loggerMain = logging.getLogger("Main")
loggerProcessor = logging.getLogger("Processing")

#GLOBAL VARS
PARAMS = ParamsConstructor().constructDefaultParams()
IMAGE_DIRECTORY = './processing/'
TREE_DIRECTORY = './eyeVergence/trees/tree1.csv'
ANALYZE_IMAGES = True #warning threadsafety
RETRIEVE_IMAGES = True #warning threadsafety


def retrieveImageBB(imageDir, recvPipe, sendPipe, cam, captureDelay):
    loggerRetrieval.info('Init Camera Loop')

    # doit =  recvPipe.recv()

    # initialize cameras
    # camRight = Cam.Cam(IMAGE_DIRECTORY, "R")
    # camLeft = Cam.Cam(IMAGE_DIRECTORY, "L")

    # looping to capture and process images
    # for i in range(1,100):
    while True:

        recvPipe.recv()
        timestamp = int(time.time())
        # camRight.takeImg()
        # camLeft.takeImg()
        cam.takeImg()

        # rightImg = camRight.getImg(timestamp)
        # leftImg = camLeft.getImg(timestamp)

        img = cam.getImg(timestamp)
        # rightImg = cam.getImg(timestamp)

        #Send images through the pipe to be received by the Analyzer
        sendPipe.send(img)
        # pipe.send(rightImg)

        if captureDelay:
            time.sleep(captureDelay)

    # close connections to cameras
    # camLeft.closeConn()
    # camRight.closeConn()


def analyzeImageBB(recvPipe, sendPipe):

    loggerProcessor.info('Init Analyzing Loop')

    dTree = DecisionTree()
    dTree.importTree(TREE_DIRECTORY)

    motor = Actuate.Actuate("P8_13", 3,-1)
    motor.startup()
    motor.actuate("FAR")

    currentPrescription = "FAR"
    
    while ANALYZE_IMAGES:
        pass

        img = recvPipe.recv()
        # rightImg = pipe.recv()

        if img is not None:
            (x, y) = Analyzer(img).getEyeData().getPupilCentreCandidate(db.Eyeball.FilterOptions.REFLECTION)
            loggerProcessor.info('Got x: {} y: {}'.format(x, y))
            sendPipe.send((x,y))
        else:
            loggerProcessor.error('Image was none')
            sendPipe((-1,-1))

if  __name__ == '__main__':

    if not Utils.isBeagalBone():
        raise AssertionError('The system was meant for the beaglebone! Use a different Start.py file')

    camLeft = Cam(IMAGE_DIRECTORY, 'L')
    camRight = Cam(IMAGE_DIRECTORY, 'R')

    # readyPipe = receives signal to start | sendReadyPipe = sends signal to start
    readyLeftPipe, sendLeftReadyPipe = Pipe()
    readyRightPipe, sendRightReadyPipe = Pipe()

    # readyPipe = receives signal to start | sendReadyPipe = sends signal to start
    analLeftPipe, camLeftPipe = Pipe()
    analRightPipe, camRightPipe = Pipe()

    resultLeftPipe, postAnalLeftPipe = Pipe()
    resultRightPipe, postAnalRightPipe = Pipe()


#    imageRetrieval = Process(target=retrieveImageBB, name = "CAMERA", args=(IMAGE_DIRECTORY, retrievePipe, 1))

    camLeftProcess = Process(target=retrieveImageBB, name = "CAMERA_L", args=(IMAGE_DIRECTORY, readyLeftPipe, camLeftPipe,camLeft, 0))
    camRightProcess = Process(target=retrieveImageBB, name = "CAMERA_R", args=(IMAGE_DIRECTORY, readyRightPipe, camRightPipe,camRight, 0))
    analLeftProcess = Process(target=analyzeImageBB, name = "ANALYZER", args=(analLeftPipe, postAnalLeftPipe,))
    analRightProcess = Process(target=analyzeImageBB, name = "ANALYZER", args=(analRightPipe, postAnalRightPipe,))

    camLeftProcess.start()
    camRightProcess.start()
    analLeftProcess.start()
    analRightProcess.start()

    while True:

        sendLeftReadyPipe.send(True)
        sendRightReadyPipe.send(True)

        leftXY = resultLeftPipe.recv()
        rightXY = resultRightPipe.recv()

        loggerMain('Left: ' + leftXY)
        loggerMain('Right: ' + rightXY)


    # while True:
    #
    #
    #
    #     leftXY = resultLeftPipe.recv()
    #     rightXY = resultLeftPipe.recv()
    #
    #     resultLeftPipe.send
    #
    #
    #     if all(v != -1 for v in (xL, yL, xR, yR)):
    #             pupils = {'x1': xR, 'x2': yR, 'x3': xL,'x4': yL}
    #             prescription = dTree.traverseTree(pupils, dTree.root)
    #             loggerProcessor.info('vergence computed: %s', prescription)
    #
    #             if currentPrescription is not prescription:
    #                 motor.actuate(prescription)
    #                 currentPrescription = prescription
    #
    #
    #
    #     imageRetrievalLeft.join()
    #     imageRetrievalRight.join()

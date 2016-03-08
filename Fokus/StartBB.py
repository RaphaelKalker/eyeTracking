from multiprocessing import Process, Lock, Pipe
import sys
import time
from Analyzer import Analyzer
import Utils
import logging

sys.path.insert(0, '../pyCam/')
import Cam

from learning.ParamsConstructor import ParamsConstructor

__author__ = 'Raphael'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logger = logging.getLogger(__name__)

loggerBB = logging.getLogger("BeagleBone")
loggerProcessor = logging.getLogger("Processing")

#GLOBAL VARS
PARAMS = ParamsConstructor().constructDefaultParams()
IMAGE_DIRECTORY = './processing/'
ANALYZE_IMAGES = True #warning threadsafety
RETRIEVE_IMAGES = True #warning threadsafety


def retrieveImageBB(imageDir, pipe, captureDelay):
    loggerBB.info('Init Camera Loop')

    # initialize cameras
    camRight = Cam.Cam(IMAGE_DIRECTORY, "R")
    camLeft = Cam.Cam(IMAGE_DIRECTORY, "L")

    # looping to capture and process images
    # for i in range(1,100):
    while RETRIEVE_IMAGES:
        timestamp = int(time.time())
        camRight.takeImg()
        camLeft.takeImg()

        rightImg = camRight.getImg(timestamp)
        leftImg = camLeft.getImg(timestamp)

        #Send images through the pipe to be received by the Analyzer
        pipe.send(leftImg)
        pipe.send(rightImg)

        if captureDelay:
            time.sleep(captureDelay)

    # close connections to cameras
    camLeft.closeConn()
    camRight.closeConn()


def analyzeImageBB(pipe):

    loggerBB.info('Init Analyzing Loop')

    while ANALYZE_IMAGES:
        pass

        leftImg = pipe.recv()
        rightImg = pipe.recv()

        if leftImg is not None and rightImg is not None:
            (xL, yL) = Analyzer(leftImg).getEyeData().getRandomPupilTruth()
            (xR, yR) = Analyzer(rightImg).getEyeData().getRandomPupilTruth()
            loggerBB.info('Got x: {} y: {}'.format(xL, yL))
            loggerBB.info('Got x: {} y: {}'.format(xR, yR))
        else:
            loggerBB.error('Image was none')

if  __name__ == '__main__':

    if not Utils.isBeagalBone():
        raise AssertionError('The system was meant for the beaglebone! Use a different Start.py file')

    # Pipe for connecting retrieval to analysis
    analyzePipe, retrievePipe = Pipe()

    imageRetrieval = Process(target=retrieveImageBB, name = "CAMERA", args=(IMAGE_DIRECTORY, retrievePipe, 1))
    imageAnalysis = Process(target=analyzeImageBB, name = "ANALYZER", args=(analyzePipe,))

    imageRetrieval.start()
    imageAnalysis.start()
import time
import sys
import logging
from multiprocessing import Lock

import os

from Analyzer import Analyzer
from db import Database
import Utils
from learning.ParamsConstructor import ParamsConstructor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if Utils.isBeagalBone():
    sys.path.insert(0, '../pyCam/')
    import Cam1
    import Cam2

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'
PROCESSING_DIR_JAN_11 = 'image/Jan11'
PROCESSING_DIR_JAN_13 = 'image/tim_jan13'

lockObj = Lock()


def compareResults(results, THRESHOLD=20):
    annotated , (truthX, truthY) = Database.getTruth(results.getFileName())

    if annotated:

        for entry in results.getHeuristics():
            heuristic = entry.itervalues().next()
            xDiff = abs(heuristic['x'] - truthX)
            yDiff = abs(heuristic['y'] - truthY)

            if xDiff < THRESHOLD and yDiff < THRESHOLD:
                pass
                # print 'SUCCESS'


def processImages():
    os.chdir(PROCESSING_DIR_JAN_13)

    params = ParamsConstructor().constructDefaultParams()

    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('jpg') or f.endswith('jpeg') ]
    for image in files:
        left = Analyzer(image, params)
        results = left.getEyeData()
        (x,y) = results.getRandomPupilTruth()
        logger.info('Random Pupil Truth: x: {}, y: {}'.format(x,y))
        compareResults(results)


def retrieveImagesBB(imageDir, lock, pipe):
    logger.info('Init BB System')

    # initialize cameras
    camRight = Cam1.Cam1(IMAGE_DIRECTORY)
    camLeft = Cam2.Cam2(IMAGE_DIRECTORY)

    # looping to capture and process images
    for i in range(1,100):
        timestamp = int(time.time())
        camRight.takeImg()
        camLeft.takeImg()

        rightImg = camRight.getImg(timestamp)
        leftImg = camLeft.getImg(timestamp)

        time.sleep(1)

    # close connections to cameras
    cam1.closeConn()
    cam2.closeConn()


if  __name__ == '__main__':

    if Utils.isBeagalBone():
        retrieveImagesBB(IMAGE_DIRECTORY, lockObj, None)

    else:
        logger.info('Init Mac System')
        processImages()


import time
from Analyzer import Analyzer
from db import Database
import sys
import logging
import os
import Utils
from learning.ParamsConstructor import ParamsConstructor
import math
import matplotlib.pyplot as plt

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'
PROCESSING_DIR_JAN_11 = 'image/Jan11'
PROCESSING_DIR_JAN_13 = 'image/tim_jan13'
TEST_DIR = 'image/DISTANCE_IMAGE'


# def compareResults(results, THRESHOLD=20):
#    annotated , (truthX, truthY) = Database.getTruth(results.getFileName())
#
#    if annotated:
#
#        for entry in results.getHeuristics():
#            heuristic = entry.itervalues().next()
#            xDiff = abs(heuristic['x'] - truthX)
#            yDiff = abs(heuristic['y'] - truthY)
#
#            if xDiff < THRESHOLD and yDiff < THRESHOLD:
#                pass
#                # print 'SUCCESS'


global dist_error
dist_error = []

def compareResults(img_file, pupil):
    annotated , (truthX, truthY) = Database.getTruth(img_file)

    if annotated:
        deltaX = (pupil[0] - truthX)
        deltaY = (pupil[1] - truthY)
            
        errorLen = math.sqrt(deltaX**2 + deltaY**2)
        logger.info('error: %s', errorLen)

        global dist_error
        dist_error.append(errorLen)

def processImages():
    os.chdir(TEST_DIR)

    params = ParamsConstructor().constructDefaultParams()

    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('jpg') or f.endswith('jpeg') ]
    for image in files:
        (x,y) = Analyzer(image, params).getEyeData().getRandomPupilTruth()
        logger.info('Random Pupil Truth: x: {}, y: {}'.format(x,y))
        compareResults(image, [x,y])

    plt.hist(dist_error, bins=100)
    plt.title(TEST_DIR)
    plt.xlabel('pixel distance')
    plt.ylabel('counts')
    plt.show()


if  __name__ == '__main__':

    if Utils.isBeagalBone():
        raise AssertionError('Do not start this on the beaglebone system, use StartBB.py instead.')

    processImages()


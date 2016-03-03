import time
import sys
import logging

import os

from Analyzer import Analyzer
from db import Database
import Utils
from learning.ParamsConstructor import ParamsConstructor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'
PROCESSING_DIR_JAN_11 = 'image/Jan11'
PROCESSING_DIR_JAN_13 = 'image/tim_jan13'


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
        (x,y) = Analyzer(image, params).getEyeData().getRandomPupilTruth()
        logger.info('Random Pupil Truth: x: {}, y: {}'.format(x,y))
        # compareResults(results)

if  __name__ == '__main__':

    if Utils.isBeagalBone():
        raise AssertionError('Do not start this on the beaglebone system, use StartBB.py instead.')

    processImages()


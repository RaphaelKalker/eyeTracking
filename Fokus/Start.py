from multiprocessing import Process, Lock, Pipe
import time
import sys
import logging
import os
import Cam

from Analyzer import Analyzer
import Test2
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




def analyzeImageBB(lock):
    (xL, yL) = Analyzer(Test2.getLeftImage()).getEyeData().getRandomPupilTruth()
    (xR, yR) = Analyzer(Test2.getRightImage()).getEyeData().getRandomPupilTruth()


if  __name__ == '__main__':

    if Utils.isBeagalBone():
        # Pipe for connecting retrieval to analysis
        analyzePipe, retrievePipe = Pipe()

        # Processes for
        imageRetrieval = Process(target=retrieveImagesBB, name = "CAMERA", args=(IMAGE_DIRECTORY, lockObj, retrievePipe))
        imageAnalysis = Process(target=retrieveImageBB, name = "ANALYZER", args=(lockObj))

        imageRetrieval.start()
        imageAnalysis.start()

    else:
        logger.info('Init Mac System')
        processImages()


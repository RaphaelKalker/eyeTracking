from multiprocessing import Process, Lock, Pipe, Pool
import sys
import time
from Analyzer import Analyzer
from actuation import Actuate
from camera.Cam import Cam
from serial import Serial
import db
from eyeVergence.BinaryTree import DecisionTree
import Utils
import logging
from debug.Benchmark import Benchmark

import db

from learning.ParamsConstructor import ParamsConstructor

__author__ = 'Raphael'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
loggerProcessor = logging.getLogger("Processing")
loggerMain = logging.getLogger("Main Loop")

#GLOBAL VARS
PARAMS = ParamsConstructor().constructDefaultParams()
IMAGE_DIRECTORY = './processing/'
TREE_DIRECTORY = './eyeVergence/trees/tree1.csv'
ANALYZE_IMAGES = True #warning threadsafety
RETRIEVE_IMAGES = True #warning threadsafety
LEFT = "L"
RIGHT = "R"
FAR = 'FAR'
NEAR = 'NEAR'

SIMULATE_BB = False


def retrieveImageBB(args):
    loggerRetrieval = logging.getLogger("ImageRetrieval")
    loggerRetrieval.info('Retrieving: ' + args[1])


    camL = args[0]


    # from camera.Cam import Cam
    # camL = Cam(IMAGE_DIRECTORY, LEFT)
    # camR = Cam(IMAGE_DIRECTORY, RIGHT)

    loggerRetrieval.info('Initialized cam object: ' + LEFT)


    # cam = args[0]
    # side = args[1]
    # loggerRetrieval.info('Retrieving: ' + LEFT)
    buffL = camL.getImg(int(time.time()))
    # buffR = camR.getImg(int(time.time()))
    loggerRetrieval.info('Got image: ' + buffL)
    # loggerRetrieval.info('Got image: ' + buffR)
    #
    # loggerRetrieval.info('RETURN VALUE: ' + buff)

    return buffL

def analyzeImageBB(args):
    img = args[0]
    side = args[1]
    loggerProcessor.info('Analyzing:' + side)

    if img is not None:
        return Analyzer(img).getEyeData().getPupilCentreCandidate(db.Eyeball.Eyeball.FilterOptions.REFLECTION)
    else:
        return (-1,-1)

if  __name__ == '__main__':

    if not Utils.isBeagalBone():
        raise AssertionError('The system was meant for the beaglebone! Use a different Start.py file')

    #Initialize Motor
    loggerMain.info('Init Motor')
    # motor = Actuate.Actuate("P8_13", 3,-1)
    # motor.startup()
    # motor.actuate("FAR")

    #Initialize Cameras:
    loggerMain.info('Init Cameras')
    cameraLeft = Cam(IMAGE_DIRECTORY, LEFT)
    cameraRight = Cam(IMAGE_DIRECTORY, RIGHT)

    #Initialize Decision Tree
    loggerMain.info('Init Decision Tree')
    dTree = DecisionTree()
    dTree.importTree(TREE_DIRECTORY)
    currentPrescription = FAR


    camPool = Pool(processes=2)
    analPool = Pool(processes=2)


    count = 0
    while count == 0:
        count = 1

        cameraLeft.takeImg()
        cameraRight.takeImg()

        camImages = camPool.map(retrieveImageBB, [(cameraLeft, LEFT)])
        camPool.close()
        camPool.join()

        loggerMain.info('Cam images came back')
        loggerMain.info(camImages[0])

        pupilCoordinates = analPool.map(analyzeImageBB, [(camImages[0], LEFT), (camImages[1], RIGHT)])
        analPool.join()

        if all(x != -1 for x in pupilCoordinates):
            pupils = {
                'x1': pupilCoordinates[0][0],
                'x2': pupilCoordinates[0][1],
                'x3': pupilCoordinates[1][0],
                'x4': pupilCoordinates[1][1]
            }

            loggerMain.info(pupils)

            prescription = dTree.traverseTree(pupils, dTree.root)
            loggerMain.info('Vergence Computed: %s', prescription)

            if currentPrescription is not prescription:
                # motor.actuate(prescription)
                currentPrescription = prescription

            pool.join()

        else:
            loggerMain.warn('No Pupil Detected')


    #Cleanly close camera
    cameraLeft.closeConn()
    cameraRight.closeConn()

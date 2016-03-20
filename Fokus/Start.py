import time
import numpy
from Analyzer import Analyzer
from db import Database
import sys
import logging
import os
import Utils
from debug import FeatureDebug
from learning.ParamsConstructor import ParamsConstructor
import math

if FeatureDebug.COMPARE_WITH_MATPLOTLIB:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'
PROCESSING_DIR_JAN_11 = 'image/Jan11'
PROCESSING_DIR_JAN_13 = 'image/tim_jan13'
TEST_DIR = 'image/DISTANCE_IMAGE'
TEST_DB = 'db-tim_distance'
PROCESSING_DIR_READING = 'image/READING_IMAGE'

dist_error = []
successCount = 0
totalImages = 0

global db
db = Database.Database(databaseName=TEST_DB)

def compareResults(img_file, pupil):
    global successCount
    global dist_error

    annotated , (truthX, truthY) = db.getTruth(img_file)

    if annotated:
        successCount += 1
        deltaX = (pupil[0] - truthX)
        deltaY = (pupil[1] - truthY)
            
        errorLen = math.sqrt(deltaX**2 + deltaY**2)
        # logger.info('error: %s', errorLen)

        dist_error.append(errorLen)

def logStats():
    correct = sum(1 for x in dist_error if x < 10)
    logger.info('Final Stats: \n\t Pupils Annoted: {} \n\t Total Images: {} \n\t Success Rate: {}'.format(successCount, totalImages, float(correct)/totalImages))
    pass

def processImages():
    global totalImages
    os.chdir(TEST_DIR)

    params = ParamsConstructor().constructDefaultParams()


    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('jpg') or f.endswith('jpeg') ]
    totalImages = len(files)
    for image in files:

        analysis = Analyzer(image, params)
        eyeData = analysis.getEyeData()

        reflections = eyeData.getReflection()
        likelyCandidate = eyeData.getPupilCentreCandidate(db.Eyeball.Eyeball.FilterOptions.REFLECTION)

        if reflections:
            (xReflect, yReflect) = (reflections[0]['x'], reflections[0]['y'])
            # logger.info('Reflection Location : x: {}, y: {}'.format(xReflect,yReflect))
        else:
            (xReflect, yReflect) = (-1, -1)

        logger.info(image)
        if FeatureDebug.COMPARE_WITH_MATPLOTLIB:
            compareResults(image, likelyCandidate)

    logStats()

    if  FeatureDebug.COMPARE_WITH_MATPLOTLIB:
        plt.hist(dist_error, bins=100)
        plt.title(TEST_DIR)
        plt.xlabel('pixel distance')
        plt.ylabel('counts')
        plt.show()

if  __name__ == '__main__':

    if Utils.isBeagalBone():
        raise AssertionError('Do not start this on the beaglebone system, use StartBB.py instead.')

    processImages()


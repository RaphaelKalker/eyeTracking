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
import glob
from eyeVergence.BinaryTree import DecisionTree

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
#TEST_DIR = 'image/march20-readLamp'

VERGENCE_TRUTH = 'reading'
TEST_DIR = 'image/read'
TEST_DB = 'db-LAMPread'

#VERGENCE_TRUTH = 'non_reading'
##TEST_DIR = 'image/lampDistance'
##TEST_DB = 'db-LAMPdistance'
#TEST_DIR = 'image/DISTANCE_IMAGE'
#TEST_DB = 'db-tim_distance'

PROCESSING_DIR_READING = 'image/READING_IMAGE'
TREE_DIRECTORY = './eyeVergence/trees/tree1.csv'

dist_error = []
successCount = 0
totalImages = 0

vergence_error = []

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

        print image
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

def processTwoEyeImages():
    dTree = DecisionTree()
    dTree.importTree(TREE_DIRECTORY)

    os.chdir(TEST_DIR)
    imgs = glob.glob("./L*.jpg")
    params = ParamsConstructor().constructDefaultParams()

    global totalImages
    totalImages = len(imgs)*2

    for img_name in imgs:
        pts = img_name.split('/')
        timestamp = pts[1][1:]

        left_img = pts[1]
        right_img = "R" + timestamp

        (xL, yL) = getPupil(left_img, params)        
        (xR, yR) = getPupil(right_img, params)        
        logger.info('Got Left x: {} y: {}'.format(xL, yL))
        logger.info('Got Right x: {} y: {}'.format(xR, yR))
        
        if all(v != -1 for v in (xL, yL, xR, yR)):
            pupils = {'x1': xR, 'x2': yR, 'x3': xL,'x4': yL}
            prescription = dTree.traverseTree(pupils, dTree.root) 
            logger.info('vergence computed: %s', prescription)
            compareVergenceResults(left_img, prescription)

        if FeatureDebug.COMPARE_WITH_MATPLOTLIB:
            compareResults(left_img, (xL, yL))
            compareResults(right_img, (xR, yR))

    print "vergence success rate: %.3f" % (sum(1 for x in vergence_error if x == VERGENCE_TRUTH)/float(len(vergence_error)))

    logStats()

    if  FeatureDebug.COMPARE_WITH_MATPLOTLIB:
        plt.hist(dist_error, bins=100)
        plt.title(TEST_DIR)
        plt.xlabel('pixel distance')
        plt.ylabel('counts')
        plt.show()

def getPupil(image, params):
    analysis = Analyzer(image, params)
    eyeData = analysis.getEyeData()

    reflections = eyeData.getReflection()
    likelyCandidate = eyeData.getPupilCentreCandidate(db.Eyeball.Eyeball.FilterOptions.REFLECTION)
    return likelyCandidate

def compareVergenceResults(imgName, prescription):
    
    global vergence_error
    eye = db.getImage(imgName)
    if eye:
        vergence = eye[0]['prescription_type']
        prescription = 'reading' if prescription == 'NEAR' else 'non_reading'
        vergence_error.append(prescription)

if  __name__ == '__main__':

    if Utils.isBeagalBone():
        raise AssertionError('Do not start this on the beaglebone system, use StartBB.py instead.')

#    processImages()
    processTwoEyeImages()


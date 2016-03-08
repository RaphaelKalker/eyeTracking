import time
import sys
import logging

import cv2
import numpy as np
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
PROCESSING_DIR_JAN_13 = 'image/DISTANCE_IMAGE'  #tim_jan13'

correct = 0
incorrect = 0

#compare the results (x,y) pair with the true values in the DB 
def compareResults(imagePath, (x,y), THRESHOLD=5):
        annotated , (truthX, truthY) = Database.getTruth(imagePath)

        if annotated:
            if abs(truthX - x) < THRESHOLD and abs(truthY - y) < THRESHOLD:
                global correct
                correct = correct + 1

            else:
                global incorrect
                incorrect = incorrect + 1


def processImages():
    os.chdir(PROCESSING_DIR_JAN_13)
    
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('jpg') or f.endswith('jpeg') ]
    for image in files:
        (x,y) = playground(image)
        #compareResults(image, (x,y))

        

def playground(imagePath):
    #segmentation in HSV space:
    logger.info("playground")
    image = cv2.imread(imagePath)

#    image = cv2.equalizeHist(image)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    _, thresh = cv2.threshold(img[:,:,1], 35, 255, cv2.THRESH_BINARY)
    _, thresh2 = cv2.threshold(img[:,:,0], 55, 255, cv2.THRESH_BINARY)

#    thresh2 = cv2.adaptiveThreshold(img[:,:,1],255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51,-5)
    
    cv2.imshow("H", img[:,:,0])
    cv2.imshow("S", img[:,:,1])
    cv2.imshow("V", img[:,:,2])

    cv2.imshow("TEST", thresh)
    cv2.imshow("TEST", thresh2)
    cv2.imshow("AND", cv2.bitwise_and(img[:,:,2],cv2.bitwise_and(thresh, thresh2)))
    
    cv2.waitKey()    
    x = 44
    y = 23
    return (x,y)
    
processImages()
logger.info("CORRECT IDENT IMAGES: %d", correct)
logger.info("INCORRECT IDENT IMAGES: %d", incorrect)

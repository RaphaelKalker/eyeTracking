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
#PROCESSING_DIR_JAN_13 = 'image/tim_jan13'
#PROCESSING_DIR_JAN_13 = 'image/READING_IMAGE'
PROCESSING_DIR_JAN_13 = 'image/DISTANCE_IMAGE'

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


prevImage = None        

def playground(imagePath):

    global prevImage
    
    #segmentation in HSV space:
    logger.info("playground")
    image = cv2.imread(imagePath)
    height, width, channels = image.shape
    

    #create a mask to remove some of the image which is irrelevant
    mask = np.zeros((height,width,channels), np.uint8)

    mask[0:0.66*height,:] = (255,255,255)
    #mask[0:1*height,:] = (255,255,255)

    #cv2.imshow("mask", blank_image)
    
    img = cv2.cvtColor(cv2.bitwise_and(mask, image), cv2.COLOR_BGR2HSV)
    #_, thresh = cv2.threshold(img[:,:,1], 45, 255, cv2.THRESH_BINARY)
    #_, thresh2 = cv2.threshold(img[:,:,0], 65, 255, cv2.THRESH_BINARY)
    #        thresh2 = cv2.adaptiveThreshold(img[:,:,1],255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51,-5)

    #first scale up the values
    minH, maxH, _, _ = cv2.minMaxLoc(img[:,:,0])
    minS, maxS, _, _ = cv2.minMaxLoc(img[:,:,1])

    Hchannel = (img[:,:,0]*255.0/float(maxH)).astype(np.uint8)
    Schannel = (img[:,:,1]*255.0/float(maxS)).astype(np.uint8)
    cv2.imshow("H", Hchannel)
    cv2.imshow("S", Schannel)
    cv2.imshow("V", img[:,:,2])

    #if prevImage is not None:
    #    img = cv2.absdiff(image, prevImage)

    #for the fuzzy type AND do MIN. Fuzzy type OR do MAX

    minImage = cv2.min(Hchannel, Schannel)
    minI, maxI, _, _ = cv2.minMaxLoc(minImage)
    _, minImg = cv2.threshold(cv2.blur((minImage[:,:]*255.0/float(maxI)).astype(np.uint8), (10,10)), 110, 255, cv2.THRESH_BINARY)

    #cv2.imshow("TEST", thresh2)

    segmentedImage = cv2.bitwise_and(img[:,:,2], minImg)
    cv2.imshow("AND", segmentedImage) #,cv2.bitwise_and(thresh, thresh2)))

    #do the canny
    edgeSegment = cv2.bitwise_and(cv2.Canny(minImg, 100, 50), mask[:,:,0])#minImg)
    cv2.imshow("EDGE", edgeSegment) 

    #do the circle
    circles = cv2.HoughCircles(edgeSegment, cv2.cv.CV_HOUGH_GRADIENT, 2, 10, None, 10, 35, 20, 35)

    if circles is not None and circles.shape > 0:
            circ = np.round(circles[0, :]).astype("int")
            for (x,y,r) in circ:
                    cv2.circle(image, (x,y), r, (0,0,255), 1)

    cv2.imshow("circles", image)
    
    prevImage = image
    
    cv2.waitKey()    
    x = 44
    y = 23
    return (x,y)
    
processImages()
logger.info("CORRECT IDENT IMAGES: %d", correct)
logger.info("INCORRECT IDENT IMAGES: %d", incorrect)

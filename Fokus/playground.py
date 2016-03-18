import time
import sys
import logging
import math

import cv2
import numpy as np
import os

from Analyzer import Analyzer
import CV_
from db import Database
import Utils
from learning.ParamsConstructor import ParamsConstructor
import matplotlib.pyplot as plt

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'
PROCESSING_DIR_JAN_11 = 'image/Jan11'
#PROCESSING_DIR_JAN_13 = 'image/tim_jan13'
#PROCESSING_DIR_JAN_13 = 'image/READING_IMAGE'
PROCESSING_DIR_JAN_13 = 'image/DISTANCE_IMAGE'

hist = []
successCount = 0
totalCount = 0

DB = Database.Database("database/db-tim_distance.json")
#DB = Database.Database("database/imgDB-2.json")

#compare the results (x,y) pair with the true values in the DB 
def compareResults(imagePath, (x,y), THRESHOLD=10):
        global hist
        global successCount
        annotated , (truthX, truthY) = DB.getTruth(imagePath)

        if annotated and x > 0 and y > 0:
            successCount += 1
            hist.append(int(math.sqrt(abs(truthX - x)*abs(truthX - x) + abs(truthY - y)*abs(truthY - y))))

def processImages():
    global totalCount
    os.chdir(PROCESSING_DIR_JAN_13)
    
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('jpg') or f.endswith('jpeg') ]
    for image in files:
        (x,y) = playground(image)
        compareResults(image, (x,y))
        totalCount += 1

def findPupilFromCircles(circles):
    blank = np.zeros((120,160,1), np.uint8)
    accumulator = np.copy(blank).astype(np.uint8)
    if circles is not None and circles.shape > 0:
        circ = np.round(circles[0, :]).astype("int")
        incrementDepth = 255.0 / float(len(circ))
        for (x,y,r) in circ:
                #create new image for the circle
                tempImage = np.copy(blank).astype(np.uint8)
                #draw on the circle
                cv2.circle(tempImage, (x,y), r, incrementDepth, -1)
                accumulator = cv2.add(tempImage, accumulator)
                
        cv2.imshow("accumulator", accumulator)
        #scale up incase not all circles are in same place
        minVal, maxVal, _, _ = cv2.minMaxLoc(accumulator)
        if maxVal < 250:
                accumulator = (accumulator * 255.0 / float(maxVal)).astype(np.uint8)
                
        #now find the location of the centre of this maximum region
        #threshold first
        _, accumulator = cv2.threshold(accumulator, 250, 255, cv2.THRESH_BINARY)
        contour, _ = CV_.findContours(accumulator, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        x,y,w,h = cv2.boundingRect(contour[0])
        
        #return the centre value
        return (x+w/2, y+h/2)
    else:
        return (0, 0)
    

prevImage = None        

def playground(imagePath):

    global prevImage

    #segmentation in HSV space:
    logger.info("%s", imagePath)
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
    cv2.imshow("V", image)

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
    #circles = cv2.HoughCircles(edgeSegment, cv2.cv.CV_HOUGH_GRADIENT, 2, 10, None, 10, 35, 7, 35)
    circles = CV_.HoughCirclesWithDefaultGradient(edgeSegment, 2, 10, None, 10, 35, 7, 35)
    # circles = cv2.HoughCircles(edgeSegment, cv2.HOUGH_GRADIENT, 2, 10, None, 20, 35, 7, 35)

    if circles is not None and circles.shape > 0:
            circ = np.round(circles[0, :]).astype("int")
            for (x,y,r) in circ:
                    cv2.circle(image, (x,y), r, (0,0,255), 1)

    centre = findPupilFromCircles(circles)

    cv2.circle(image, centre, 3, 255)
    
    cv2.imshow("circles", image)

    
    
    prevImage = image
    
    cv2.waitKey()    


    return centre
    
processImages()

logger.info("Successful pupils detected: %d", successCount)
logger.info("Total images: %d", totalCount)
plt.hist(hist, bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
plt.show()
logger.info("DONE")


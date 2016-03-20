import math

import cv2
import numpy as np

import CV_
# import database
from debug import FeatureDebug
from ImageHelper import ImageHelper

__author__ = 'Raphael'

MIN_AREA = 30 #the min value for creating circles
RED = (0,0,255)
GREEN = (0,255,0)
BLUE = (255,0,0)
YELLOW = (0,255,255)
DIFF_VALUES = 1
DP = 10 #Dimension in circle space (lower is faster to compute)
CROSSHAIRS = 5
PRINTDEBUG = True

HOUGH_PARAM1 = 1
HOUGH_MAX_PARAM2 = 300
HOUGH_MIN_RADIUS = 0
HOUGH_MAX_RADIUS = 40
HOUGH_MIN_DIST = 20 # the minimum distance two detected circles can be from one another
HOUGH_MAX_ATTEMPTS = 100 #define the number of attempts to find at least one circle

PARAM1 = 'param1'
PARAM2 = 'param2'
MIN_RAD = 'minRadius'
MAX_RAD = 'maxRadius'

DP = 10 #Dimension in circle space (lower is faster to compute)

#Values
DEBUG_RECT = 'Rect'
DEBUG_CENTER = 'Center'
DEBUG_RADIUS = 'Radius'
DEBUG_CANDIDATE_CORNER = 'CandidateCorner'

class PupilDetector(object):

    def __init__(self, originalImg, processedImg, params = None, eyeball=None):
        self.originalImg = originalImg
        self.processedImg = processedImg
        self.params = params
        self.eyeBall = eyeball

        if FeatureDebug.DEBUG_PUPIL_DETECTOR:
            from debug.AdjustableImage import AdjustableImage
            self.debug = AdjustableImage()
            self.debug.doIt(self.originalImg, self.updateHoughCallback, self.params)

        if FeatureDebug.DEBUG_DRAW_TRUTH:
            from db import Database as db
            self.db = db
            self.__drawTruth__()

    def doHoughTransform(self, param1=None, param2 = None, minRadius = None, maxRadius = None):

        # houghTransformed = self.processedImg.copy()
        result = self.originalImg.copy()

        if param1 is None or param2 is None or minRadius is None or maxRadius is None:
            (param1, param2, minRadius, maxRadius) = self.params.hough.getParams()
            # houghMinDistance = HOUGH_MIN_DIST

        houghCircles = CV_.HoughCirclesWithDefaultGradient(self.processedImg, DP, HOUGH_MIN_DIST,
                                   None, param1, param2, minRadius, maxRadius)

        if houghCircles is not None:
            # self.saveInfo({('Hough Circle', True)})
            circles = np.round(houghCircles[0, :]).astype("int")
            for (x,y,r) in circles:
                cv2.circle(result, (x,y), r, GREEN, 1)
                cv2.line(result,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS), RED, 1)
                cv2.line(result,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS), RED, 1)

                self.eyeBall.addHoughCircle(x,y,r)

                ImageHelper.showImage('Hough Circle', result)
            return result
        else:
            # self.saveInfo({('Hough Circle', False)})
            pass

    def findPupilCircle(self):

        pupilStats = {}

        circleDetectedImage = self.processedImg.copy()
        result = self.originalImg.copy()

        #Fill in contours
        contours, hierachy = CV_.findContours(circleDetectedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(circleDetectedImage, contours, -1, (255,255,255), -1)
        # Imager.showImage("Fill in contours", srcImage)


        for contour in contours:
            area = cv2.contourArea(contour)
            x,y,width,height = cv2.boundingRect(contour)
            radius = width/2

            #DEBUGGING
            # if area > 0:
            #     print "Area: " + str(area)
            # if width != 0 and height != 0 and radius != 0:
            #     print "Diff1: " + str(abs(1 - width/height))
            #     print "Diff2: " + str(abs(1 - area/(math.pi * math.pow(radius, 2))))


            if  (   area >= MIN_AREA and
                    abs(1 - width/height) <= DIFF_VALUES and
                    abs(1 - area/(math.pi * math.pow(radius, 2))) < DIFF_VALUES):

                # print "Diff1: " + str(abs(1 - width/height))
                # print "Diff2: " + str(abs(1 - area/(math.pi * math.pow(radius, 2))))

                center = (x + radius, y + radius)
                cv2.line(result,(x, y + radius),(x + radius*2, y + radius),(0,0,255),1)
                cv2.line(result,(x + radius, y + radius *2),(x + radius, y),(0,0,255),1)
                cv2.circle(result, center, radius, RED, 1)

                ImageHelper.showImage('Pupil Circle', result)

                # self.callback({('DEBUG_RADIUS', radius), ('DEBUG_CENTER', center), ('DEBUG_RECT', (x,y,width,height))})
                self.eyeBall.addContourCircle(x, y, radius)

                # self.saveInfo({(DEBUG_RADIUS, radius), (DEBUG_CENTER, center), (DEBUG_RECT, (x,y,width,height))})

    def __drawTruth__(self):
        fileName = self.eyeBall.getFileName()

        if 'img1398289259' in fileName:
            print 'FUCK'


        annotated, (x,y) = self.db.getTruth(self.eyeBall.getFileName())
        if annotated:
            cv2.circle(self.originalImg, (x,y), 5, YELLOW, -1)

    #deprecated
    def updateHoughCallback(self, param1=None, param2=None, minRad=None, maxRad=None):
        self.debug.updateImage(self.doHoughTransform(param1, param2, minRad, maxRad))
        print 'updateHough'

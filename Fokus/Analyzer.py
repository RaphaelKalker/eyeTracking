import cv2
import math
import time as time
import numpy as np

class Analyzer:

    global THRESH, MAXVAL, MIN_AREA, RED, DIFF_VALUES

    THRESH = 200 #the threshold value
    MAXVAL = 255 #the maximum value
    MIN_AREA = 30
    RED = (255,255, 0)
    DIFF_VALUES = 1

    def __init__(self):
        print 'init'

    def loadImage(self, src):

        image = cv2.imread('testimages/' + src)

        if image == None:
            raise NameError('Image not found!')

        cv2.imshow('Original Image', image)

        #Invert image with ~ and convert to grayscale
        imageGray = cv2.cvtColor(~image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grey Image', imageGray)

        #Threshold the image
        cv2.threshold(imageGray, THRESH, MAXVAL, cv2.THRESH_BINARY, imageGray)
        cv2.imshow('Threshold Image', imageGray)

        #Fill in contours
        image2, contours, heirachy = cv2.findContours(imageGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imageGray, contours, -1, (255,255,255), -1)
        cv2.imshow("Fill in contours", image2)

        for contour in contours:
            area = cv2.contourArea(contour)
            x,y,width,height = cv2.boundingRect(contour)
            radius = width/2

            #DEBUGGING
            if area > 0:
                print "Area: " + str(area)
            if width != 0 and height != 0 and radius != 0:
                print "Diff1: " + str(abs(1 - width/height))
                print "Diff2: " + str(abs(1 - area/(math.pi * math.pow(radius, 2))))


            if  (   area >= MIN_AREA and
                    abs(1 - width/height) <= DIFF_VALUES and
                    abs(1 - area/(math.pi * math.pow(radius, 2))) < DIFF_VALUES):

                print "Diff1: " + str(abs(1 - width/height))
                print "Diff2: " + str(abs(1 - area/(math.pi * math.pow(radius, 2))))

                center = (x + radius, y + radius)
                cv2.circle(image, center, radius, (0, 255,0), 1)

                cv2.imshow("Final Result " + str(time.time()), image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()




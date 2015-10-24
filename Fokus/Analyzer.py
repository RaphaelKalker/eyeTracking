import cv2
import math
import copy
import time as time
import numpy as np

class Analyzer:

    global THRESH, MAXVAL, MIN_AREA, RED, DIFF_VALUES, DP, MIN_DIST, MAX_HOUGH_ATTEMPTS, CROSSHAIRS, PRINTDEBUG

    THRESH = 220 #the threshold value
    MAXVAL = 255 #the maximum value
    MIN_AREA = 30 #the min value for creating circles
    RED = (255,255, 0)
    DIFF_VALUES = 1
    DP = 10 #Dimension in circle space (lower is faster to compute)
    MIN_DIST = 20 # the minimum distance two detected circles can be from one another
    MAX_HOUGH_ATTEMPTS = 100 #define the number of attempts to find at least one circle
    CROSSHAIRS = 5
    PRINTDEBUG = True

    def __init__(self):
        print 'init'

    def loadImage(self, src):

        originalImage = cv2.imread('image/' + src)

        if originalImage == None:
            raise NameError('Image not found!')

        houghTransformed = copy.deepcopy(originalImage)
        Analyzer.showImage(self, 'Original Image', originalImage, 0)

        #Invert image with ~ and convert to grayscale
        imageGray = cv2.cvtColor(~originalImage, cv2.COLOR_BGR2GRAY)
        Analyzer.showImage(self, 'Grey Image', imageGray, 1)

        #Threshold the image
        imageThreshold = copy.deepcopy(imageGray)
        cv2.threshold(imageThreshold, THRESH, MAXVAL, cv2.THRESH_BINARY, imageThreshold)
        Analyzer.showImage(self, 'Threshold Image', imageThreshold, 2)

        #Fill in contours
        contours, heirachy = cv2.findContours(imageThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imageThreshold, contours, -1, (255,255,255), -1)
        Analyzer.showImage(self, "Fill in contours", imageThreshold, 3)

        #Hough Circles

        circles = None
        param1 = 1
        param2 = 300
        minRadius = 0
        maxRadius = 40

        houghCircles = cv2.HoughCircles(imageThreshold, cv2.cv.CV_HOUGH_GRADIENT, DP, MIN_DIST,
                                   circles, param1, param2, minRadius, maxRadius)

        while(houghCircles is None):

            print 'Could not find circles with param2: ' + str(param2)

            # if houghCircles is not None:
            #     print 'test'
            #     if len(houghCircles) is 1:
            #         print 'After adjusting found more than one'
            #         break

            if (param2 is 1):
                print 'Failed!!!!'
                width, height, blah = originalImage.shape
                cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
                Analyzer.showImage(self, 'Hough Circle', houghTransformed, 6)

                break



            param2 -= 1
            houghCircles = cv2.HoughCircles(imageThreshold, cv2.cv.CV_HOUGH_GRADIENT, DP, MIN_DIST,
                                   circles, param1, param2, minRadius, maxRadius)

            if houghCircles is not None:
                circles = np.round(houghCircles[0, :]).astype("int")
                for (x,y,r) in circles:
                    cv2.circle(houghTransformed, (x,y), r, RED, 1)
                    lineLength = 2
                    cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
                    cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)


                    Analyzer.showImage(self, 'Hough Circle', houghTransformed, 6)


        #OLD STUFF

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
                cv2.line(originalImage,(x, y + radius),(x + radius*2, y + radius),(0,0,255),1)
                cv2.line(originalImage,(x + radius, y + radius *2),(x + radius, y),(0,0,255),1)
                cv2.circle(originalImage, center, radius, RED, 1)

                Analyzer.showImage(self, 'Final Result', originalImage, 4)


        if PRINTDEBUG:
            self.printDebugInfo()




        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def getWindowPosition(self, imageNr, imageWidth):
        return (imageNr * imageWidth, 0)


    def showImage(self, title, image, imageNr):
        cv2.imshow(title, image)
        shape = image.shape
        posX, posY = Analyzer.getWindowPosition(self, imageNr, shape[1])
        cv2.moveWindow(title, posX, posY)

    def printDebugInfo(self):
        background = np.zeros((512,512,3), np.uint8)
        win = cv2.namedWindow('Debug Infromation', flags=cv2.WINDOW_NORMAL)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(background,'Debug Info coming soon',(10,100), font, 1,(255,255,255),1)
        cv2.imshow('Debug Information', background)

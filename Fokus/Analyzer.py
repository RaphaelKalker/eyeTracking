import cv2
import math
import copy
import time as time
import numpy as np
import math

class Analyzer:

    global THRESH, MAXVAL, MIN_AREA, RED, GREEN, BLUE, DIFF_VALUES, DP, MIN_DIST, MAX_HOUGH_ATTEMPTS, CROSSHAIRS, PRINTDEBUG

    THRESH = 220 #the threshold value
    MAXVAL = 255 #the maximum value
    MIN_AREA = 30 #the min value for creating circles
    RED = (0,0,255)
    GREEN = (0,255,0)
    BLUE = (255,0,0)
    DIFF_VALUES = 1
    DP = 10 #Dimension in circle space (lower is faster to compute)
    MIN_DIST = 20 # the minimum distance two detected circles can be from one another
    MAX_HOUGH_ATTEMPTS = 100 #define the number of attempts to find at least one circle
    CROSSHAIRS = 5
    PRINTDEBUG = False 

    def __init__(self):
        print 'init'

    def loadImage(self, src):

        originalImage = cv2.imread('image/' + src)

        imgWidth,imgHeight,rgb = np.shape(originalImage)

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

#        houghCircles = cv2.HoughCircles(imageThreshold, cv2.cv.CV_HOUGH_GRADIENT, DP, MIN_DIST,
#                                   circles, param1, param2, minRadius, maxRadius)
#
#        while(houghCircles is None):
#
#            print 'Could not find circles with param2: ' + str(param2)
#
#            # if houghCircles is not None:
#            #     print 'test'
#            #     if len(houghCircles) is 1:
#            #         print 'After adjusting found more than one'
#            #         break
#
#            if (param2 is 1):
#                print 'Failed!!!!'
#                width, height, blah = originalImage.shape
#                cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
#                Analyzer.showImage(self, 'Hough Circle', houghTransformed, 6)
#
#                break
#
#
#
#            param2 -= 1
#            houghCircles = cv2.HoughCircles(imageThreshold, cv2.cv.CV_HOUGH_GRADIENT, DP, MIN_DIST,
#                                   circles, param1, param2, minRadius, maxRadius)
#
#            if houghCircles is not None:
#                circles = np.round(houghCircles[0, :]).astype("int")
#                for (x,y,r) in circles:
#                    cv2.circle(houghTransformed, (x,y), r, RED, 1)
#                    lineLength = 2
#                    cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
#                    cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
#
#
#                    Analyzer.showImage(self, 'Hough Circle', houghTransformed, 6)


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
#                cv2.line(originalImage,(x, y + radius),(x + radius*2, y + radius),(0,0,255),1)
#                cv2.line(originalImage,(x + radius, y + radius *2),(x + radius, y),(0,0,255),1)

                cv2.circle(originalImage, center, radius, RED, 1)
                cv2.circle(originalImage, center, 1, RED, 1)

                # cropping to find ir led reflection
                xBoundLow = max(0, x - 20)
                xBoundHigh = min(imgWidth, x + width + 40)
                yBoundLow = max(0, y - 20)
                yBoundHigh = min(imgHeight, y + height + 30)
                cv2.rectangle(originalImage, (yBoundHigh, xBoundHigh), (yBoundLow,xBoundLow), GREEN, 1)
                imgGrayCropped = ~imageGray[xBoundLow:xBoundHigh, yBoundLow:yBoundHigh]
                imgGrayBin = copy.deepcopy(imgGrayCropped)
                cv2.threshold(imgGrayBin, 200, MAXVAL, cv2.THRESH_BINARY, imgGrayBin)
                
                Analyzer.showImage(self, 'cropped', imgGrayCropped, 5)
                Analyzer.showImage(self, 'cropped thresholding', imgGrayBin, 6)

                # get ir led reflection contour
                irContours, hier = cv2.findContours(imgGrayBin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                # take the first found contour
                if irContours:
                    cnt = irContours[0]

                    # calculate centroid of ir contour
                    M = cv2.moments(cnt)
                    if M['m00'] == 0:
                        break
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    
                    # transform centroid back to original image coordinates
                    irX = yBoundLow + cx
                    irY = xBoundLow + cy
                    cv2.circle(originalImage, (irX,irY), 1, RED, 1)

                    # calculate distance between pupil and contour
                    lenIrPupil = math.sqrt((irX-center[0])**2 + (irY-center[1])**2 )
                    print lenIrPupil

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

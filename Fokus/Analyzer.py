import cv2
import CV_
import math
import copy
import time as time
import numpy as np

THRESH = 220 #the threshold value
MAXVAL = 255 #the maximum value
MIN_AREA = 30 #the min value for creating circles
RED = (0,0,255)
GREEN = (0,255,0)
BLUE = (255,0,0)
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

def close():
    cv2.destroyAllWindows()

def exit():
    cv2.destroyAllWindows()
    exit()


class Analyzer:

    def __init__(self, src):
        self.originalImage = cv2.imread('image/' + src)
        self.imgWidth, self.imgHeight, self.imgChannel = self.originalImage.shape
        self.imgIndex = 0
        self.debugStats = dict({('filename', src)})
        print 'Starting Analyzer for ' + src

    def loadImage(self):

        # originalImage = cv2.imread('image/' + src)
        originalImage = self.originalImage

        if originalImage is None:
            raise NameError('Image not found!')

        Analyzer.showImage(self, 'Original Image', originalImage)

        #Invert image with ~ and convert to grayscale
        imageGray = cv2.cvtColor(~originalImage, cv2.COLOR_BGR2GRAY)
        Analyzer.showImage(self, 'Grey Image', imageGray)

        #Threshold the image
        imageThreshold = copy.deepcopy(imageGray)
        cv2.threshold(imageThreshold, THRESH, MAXVAL, cv2.THRESH_BINARY, imageThreshold)
        Analyzer.showImage(self, 'Threshold Image', imageThreshold)


        #Hough Circles
        self.doHoughTransform(imageThreshold)

        #Simple Circle Math
        self.findPupilCircle(imageThreshold)

        #IR LED
        #self.findIrReflection(imageGray)


        if PRINTDEBUG:
            self.printDebugInfo()

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def doHoughTransform(self, srcImage):

        houghTransformed = copy.deepcopy(self.originalImage)
        param2 = HOUGH_MAX_PARAM2


        houghCircles = cv2.HoughCircles(srcImage, cv2.HOUGH_GRADIENT, DP, HOUGH_MIN_DIST,
                                   None, HOUGH_PARAM1, HOUGH_MAX_PARAM2, HOUGH_MIN_RADIUS, HOUGH_MAX_RADIUS)

        while(houghCircles is None):

            # print 'Could not find circles with param2: ' + str(param2)

            if (param2 is 1):
                print 'Failed!!!!'
                width, height = srcImage.shape
                cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
                Analyzer.showImage(self, 'Hough Circle', houghTransformed)

                break



            param2 -= 1
            houghCircles = cv2.HoughCircles(srcImage, cv2.HOUGH_GRADIENT, DP, HOUGH_MIN_DIST,
                                   None, HOUGH_PARAM1, param2, HOUGH_MIN_RADIUS, HOUGH_MAX_RADIUS)

            if houghCircles is not None:
                circles = np.round(houghCircles[0, :]).astype("int")
                for (x,y,r) in circles:
                    cv2.circle(houghTransformed, (x,y), r, RED, 1)
                    lineLength = 2
                    cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
                    cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)

                    Analyzer.showImage(self, 'Hough Circle', houghTransformed)

    def findPupilCircle(self, srcImage):

        pupilStats = {}

        circleDetectedImage = copy.deepcopy(self.originalImage)

        #Fill in contours
        contours, hierachy = CV_.findContours(srcImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(srcImage, contours, -1, (255,255,255), -1)
        Analyzer.showImage(self, "Fill in contours", srcImage)


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
                cv2.line(circleDetectedImage,(x, y + radius),(x + radius*2, y + radius),(0,0,255),1)
                cv2.line(circleDetectedImage,(x + radius, y + radius *2),(x + radius, y),(0,0,255),1)
                cv2.circle(circleDetectedImage, center, radius, RED, 1)

                Analyzer.showImage(self, 'Pupil Circle', circleDetectedImage)

                self.saveInfo({('radius', radius), ('center', center), ('rect', (x,y,width,height))})

    def findIrReflection(self, imageGray):

        irImage = copy.deepcopy(self.originalImage)

        center = self.debugStats.get('center')
        radius = self.debugStats.get('radius')
        xPupil, yPupil, widthPupil, heightPupil = self.debugStats.get('rect')

        # cropping to find ir led reflection
        xBoundLow = max(0, xPupil - 20)
        xBoundHigh = min(self.imgWidth, xPupil + radius*2 + 40)
        yBoundLow = max(0, yPupil - 20)
        yBoundHigh = min(self.imgHeight, yPupil + radius*2 + 30)
        cv2.rectangle(irImage, (yBoundHigh, xBoundHigh), (yBoundLow,xBoundLow), GREEN, 1)
        imgGrayCropped = ~imageGray[xBoundLow:xBoundHigh, yBoundLow:yBoundHigh]
        imgGrayBin = copy.deepcopy(imgGrayCropped)
        cv2.threshold(imgGrayBin, 200, MAXVAL, cv2.THRESH_BINARY, imgGrayBin)

        Analyzer.showImage(self, 'cropped', imgGrayCropped)
        Analyzer.showImage(self, 'cropped thresholding', imgGrayBin)

        # get ir led reflection contour
        irContours, hier = CV_.findContours(imgGrayBin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # take the first found contour
        if irContours:
            cnt = irContours[0]

            # calculate centroid of ir contour
            M = cv2.moments(cnt)
            if M['m00'] == 0:
                pass

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            # transform centroid back to original image coordinates
            irX = yBoundLow + cx
            irY = xBoundLow + cy
            cv2.circle(irImage, (irX,irY), 1, RED, 1)

            # calculate distance between pupil and contour
            lenIrPupil = math.sqrt((irX-center[0])**2 + (irY-center[1])**2 )
            print lenIrPupil

        Analyzer.showImage(self, 'IR Reflection', irImage)

    def saveInfo(self, info):
        self.debugStats.update(info)


    def getWindowPosition(self, imageNr, imageWidth):
        return (imageNr * imageWidth, 0)

    def showImage(self, title, image):
        cv2.imshow(title, image)
        shape = image.shape
        posX, posY = self.getWindowPosition(self.imgIndex, shape[1])
        cv2.moveWindow(title, posX, posY)
        self.imgIndex += 1


    def printDebugInfo(self):

        for k, v in self.debugStats.iteritems():
            print k + ': ' + str(v)
        # cv2.putText(background,'Debug Info coming soon',(10,100), font, 1,(255,255,255),1)
        # cv2.imshow(q'Debug Information', background)
import string
import cv2
import CV_
import math
import copy
import Const
import DebugOptions as tb
import time as time
import numpy as np
import platform

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

PARAM1 = 'param1'
PARAM2 = 'param2'
MIN_RAD = 'minRadius'
MAX_RAD = 'maxRadius'

#Values
DEBUG_RECT = 'Rect'
DEBUG_CENTER = 'Center'
DEBUG_RADIUS = 'Radius'
DEBUG_CANDIDATE_CORNER = 'CandidateCorner'

FORMAT_JPG = '.jpg'

selecting = False
startX = -1
startY = -1

INVALID = -1

COLOR_WHITE_LB = np.array([0,0,0])
COLOR_WHITE_UB = np.array([151,35,95])

def close():
    cv2.destroyAllWindows()

def exit():
    cv2.destroyAllWindows()
    exit()


class Analyzer2:

    #global variables

    startX = 0
    startY = 0

    #src is either a file name, or an image buffer
    def __init__(self, src, cameraType):

        if isinstance(src, basestring):
            self.debugStats = dict({('Filename', src), ('CameraType', cameraType)})
            self.cameraType = cameraType
            self.originalImage = cv2.imread(src)

        elif type(src).__module__ == 'numpy':
            self.debugStats = dict({('Buffer', True)})
            self.originalImage = cv2.imdecode(src, 1)

        else:
            raise AssertionError('Source input is invalid')

        if  self.originalImage is None:
            raise ValueError('Original Image was null')

        self.imgWidth, self.imgHeight = self.originalImage.shape[:2]
        self.imgIndex = 0


    def loadImage(self):

        originalImage = self.originalImage.copy()
        self.imageCanny = self.originalImage.copy()

        if originalImage is None:
            raise NameError('Image not found!')

        self.showImage('Original Image', originalImage)

        #Invert image with ~ and convert to grayscale
        self.imageGray = cv2.cvtColor(~originalImage, cv2.COLOR_BGR2GRAY)
        Analyzer2.showImage(self, 'Grey Image', self.imageGray)

        #Create a region of interest by selection
        # self.roi = Analyzer2.findRegionOfInterest(originalImage)
        # self.roi = originalImage.copy()
        # selectableWindow = 'Grey Image'
        # # self.showImage('ROI', self.roi)
        # cv2.setMouseCallback(selectableWindow, self.onPointSelected)

        #Convert to HSV
        self.imageHSV = cv2.cvtColor(originalImage, cv2.COLOR_BGR2HSV_FULL)
        # self.showImage('Yolo', self.imageHSV)

        #Threshold the image
        self.doThreshold()

        kernel = np.ones((3,3),np.uint8)
        iter = 1
        dilation = cv2.dilate(self.imageThreshold, kernel, iterations = iter)
        self.showImage('Dilated', dilation)

        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

        self.showImage('Closing', closing)

        self.imageThreshold = dilation




        #Hough Circles
        self.doHoughTransform(self.imageThreshold)

        #Simple Circle Math
        self.findPupilCircle(self.imageThreshold)

        #IR LED
        # self.findIrReflection(imageGray)


        if PRINTDEBUG:
            self.printDebugInfo()

        tb.initHoughOptions(self.cameraType, self.updateParams)

        cv2.waitKey(1)
        # k = cv2.waitKey() & 0xFF
        # if k == 27:
        #     cv2.destroyAllWindows()

    def updateSelector(self, img, topRight, bottomLeft):
        pass

        cv2.rectangle(img, topRight, bottomLeft, BLUE, 2)
        # self.showImage('Yoloy', img)

    def onPointSelected(self, event,x,y,flags,param):

        # print 'onPointSelected -> x: {} y: {}'.format(x,y)
        regionSelected, x1,x2, y1, y2 = Analyzer2.drawRectSelection(self, self.imageGray, event, x, y)

        if regionSelected:
            print 'region selected true'
            window = self.roi[y1+1:y2-1, x1+1:x2-1]
            hsvWindow = cv2.cvtColor(window, cv2.COLOR_BGR2HSV)
            hsvImage = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2HSV)
            self.showImage('HSV Image', hsvImage[:,:,0])
            self.showImage('HSV Image2', hsvImage[:,:,1])
            self.showImage('HSV Image3e', hsvImage[:,:,2])
            hVals = hsvWindow[:, :, 0]
            sVals = hsvWindow[:, :, 1]
            vVals = hsvWindow[:, :, 2]

            avgH = np.mean(hVals)
            avgS = np.mean(sVals)
            avgV = np.mean(vVals)

            lb = np.array([avgH - 10, avgS - 10, avgV - 10], dtype=np.uint8, ndmin=1)
            up = np.array([avgH + 10, avgV + 10, avgV + 10], dtype=np.uint8, ndmin=1)

            mask = cv2.inRange(hsvImage, lb, up)

            # self.showImage('MASKKK', mask)

            result = cv2.bitwise_and(self.originalImage, self.originalImage, mask=mask)

            self.showImage('HSV Selection', self.roi)
            self.showImage('Result', result)

            print 'region selected'



        # print window

    def drawRectSelection(self, img, event, x, y):

        global selecting, startX, startY

        if event == cv2.EVENT_LBUTTONDOWN:
            selecting = True
            startX = x
            startY = y

        elif event == cv2.EVENT_MOUSEMOVE:
            #GrayScale Image
            if len(img.shape) == 2:
                print 'Pointer Stats, x,y: {},{} - Value: [{}]'.format(x,y,img[x,y])
            else:
                print 'Pointer Stats, x,y: {},{} - Value: [{}] '.format(x,y,img[x,y,:] )
            # if selecting:
            #     pass
            #     cv2.rectangle(self.roi, (startX,startY), (x,y), GREEN, 1)

        elif event == cv2.EVENT_LBUTTONUP:
            print 'Final: ' + str(x) + ', ' + str(y)
            selecting = False
            done = True
            cv2.rectangle(img, (startX,startY), (x,y), GREEN, 1)

        if not selecting and startY is not INVALID:
            Analyzer2.showImage(self, 'ROI', self.roi)
            done = True
            x0 = startX
            y0 = startY
            startX = INVALID
            startY = INVALID
            return True, x0, x, y0, y


        else:
            return False, 0, 0, 0, 0

    def updateParams(self, type, **kwargs):
        print 'Updated Params ' + kwargs.__str__()
        self.saveInfo(kwargs)

        if type is Const.Trackbar.Canny:
            cannyLb = kwargs.get('cannyLb')
            cannyUp = kwargs.get('cannyUb')
            self.findCornerCandidate(self.imageCanny, cannyLb, cannyUp)

        elif type is Const.Trackbar.Hough:
            param1 = kwargs.get(PARAM1)
            param2 = kwargs.get(PARAM2)
            minRad = kwargs.get(MIN_RAD)
            maxRad = kwargs.get(MAX_RAD)
            self.doSelectiveHoughTransform(self.imageThreshold, param1, param2, minRad, maxRad)

    def doThreshold(self):
        self.imageThreshold = self.imageGray.copy()
        minThresh = Const.Threshold.getMin(self.cameraType)
        cv2.threshold(self.imageThreshold, minThresh, MAXVAL, cv2.THRESH_BINARY, self.imageThreshold)
        self.showImage('Threshold Image', self.imageThreshold)

    def findCornerCandidate(self, img, lowerBound, upperBound):
        blur = cv2.GaussianBlur(img, (9, 9), 0)
        self.showImage('Blurred', blur)

        edges = cv2.Canny(blur, lowerBound, upperBound)
        dst = cv2.cornerHarris(edges, 3, 21, 0.2)
        dst = cv2.dilate(dst, None)

        candidatesYX =  (dst > 0.01 * dst.max()).nonzero()

        if not candidatesYX or len(candidatesYX[0]) != 0 or len(candidatesYX[1]) != 0:
            print 'Failed to find corners!'
        else:
            ind = candidatesYX[1].argmax(axis=0)

            (mostLikelyX, mostLikelyY) = (candidatesYX[0][ind], candidatesYX[1][ind])

            self.saveInfo({(DEBUG_CANDIDATE_CORNER, (mostLikelyX, mostLikelyY))})

            corners = self.originalImage.copy()
            corners[candidatesYX[0], candidatesYX[1]] = [0,0,255]
            offset = 3
            corners[mostLikelyX -offset : mostLikelyX + offset, mostLikelyY - offset: mostLikelyY + offset] = [0,255,255]

            self.showImage('Corners', corners)
            self.showImage('Canny', edges)

        #x,y are switched





    def doSelectiveHoughTransform(self, srcImage, param1=None, param2 = None, minRadius = None, maxRadius = None):

        houghTransformed = copy.deepcopy(self.originalImage)

        houghCircles = CV_.HoughCirclesWithDefaultGradient(srcImage, DP, HOUGH_MIN_DIST,
                                   None, param1, param2, minRadius, maxRadius)

        #reset Image
        self.imgIndex = 0

        if houghCircles is not None:
            circles = np.round(houghCircles[0, :]).astype("int")
            for (x,y,r) in circles:
                cv2.circle(houghTransformed, (x,y), r, RED, 1)
                lineLength = 2
                cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
                cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)

            self.showImage('Hough Circle', houghTransformed)

        else:
            width, height = srcImage.shape
            cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
            self.showImage('Hough Circle', houghTransformed)


    def doHoughTransform(self, srcImage, param1=None, param2 = None, minRadius = None, maxRadius = None):

        houghTransformed = copy.deepcopy(self.originalImage)

        if param1 is None or param2 is None or minRadius is None or maxRadius is None:
            (param1, param2, minRadius, maxRadius) = Const.HoughParamaters.getParams(self.cameraType)
            houghMinDistance = HOUGH_MIN_DIST

        houghCircles = CV_.HoughCirclesWithDefaultGradient(srcImage, DP, houghMinDistance,
                                   None, param1, param2, minRadius, maxRadius)

        if houghCircles is not None:
            self.saveInfo({('Hough Circle', True)})
            circles = np.round(houghCircles[0, :]).astype("int")
            for (x,y,r) in circles:
                cv2.circle(houghTransformed, (x,y), r, RED, 1)
                cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS), RED, 1)
                cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS), RED, 1)

                self.showImage('Hough Circle', houghTransformed)
        else:
            self.saveInfo({('Hough Circle', False)})





        #use selective for iteration instead
        # while(houghCircles is None):
        #
        #     if (param2 is 1):
        #         print 'Failed!!!!'
        #         width, height = srcImage.shape
        #         cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
        #         self.showImage('Hough Circle', houghTransformed)
        #
        #         break
        #
        #     param2 -= 1
        #     houghCircles = CV_.HoughCirclesWithDefaultGradient(srcImage, DP, houghMinDistance,
        #                            None, param1, param2, minRadius, maxRadius)
        #
        #     if houghCircles is not None:
        #         circles = np.round(houghCircles[0, :]).astype("int")
        #         for (x,y,r) in circles:
        #             cv2.circle(houghTransformed, (x,y), r, RED, 1)
        #             cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS), RED, 1)
        #             cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS), RED, 1)
        #
        #             self.showImage('Hough Circle', houghTransformed)

    def findPupilCircle(self, srcImage):

        pupilStats = {}

        circleDetectedImage = copy.deepcopy(self.originalImage)

        #Fill in contours
        contours, hierachy = CV_.findContours(srcImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(srcImage, contours, -1, (255,255,255), -1)
        # self.showImage("Fill in contours", srcImage)


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

                self.showImage('Pupil Circle', circleDetectedImage)

                self.saveInfo({(DEBUG_RADIUS, radius), (DEBUG_CENTER, center), (DEBUG_RECT, (x,y,width,height))})

    def findIrReflection(self, imageGray):

        irImage = copy.deepcopy(self.originalImage)

        center = self.debugStats.get(DEBUG_CENTER)
        radius = self.debugStats.get(DEBUG_RADIUS)
        xPupil, yPupil, widthPupil, heightPupil = self.debugStats.get(DEBUG_RECT)

        # cropping to find ir led reflection
        xBoundLow = max(0, xPupil - 20)
        xBoundHigh = min(self.imgWidth, xPupil + radius*2 + 40)
        yBoundLow = max(0, yPupil - 20)
        yBoundHigh = min(self.imgHeight, yPupil + radius*2 + 30)
        cv2.rectangle(irImage, (yBoundHigh, xBoundHigh), (yBoundLow,xBoundLow), GREEN, 1)
        imgGrayCropped = ~imageGray[xBoundLow:xBoundHigh, yBoundLow:yBoundHigh]
        imgGrayBin = copy.deepcopy(imgGrayCropped)
        cv2.threshold(imgGrayBin, 200, MAXVAL, cv2.THRESH_BINARY, imgGrayBin)

        # Analyzer.showImage(self, 'cropped', imgGrayCropped)
        # Analyzer.showImage(self, 'cropped thresholding', imgGrayBin)

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

        # Analyzer.showImage(self, 'IR Reflection', irImage)

    def saveInfo(self, info):
        self.debugStats.update(info)


    def getWindowPosition(self, imageNr, imageWidth):
        return (imageNr * imageWidth, 0)

    def showImage(self, title, image):
        if platform.system() == Const.MAC:
            cv2.imshow(title, image)
            shape = image.shape
            posX, posY = self.getWindowPosition(self.imgIndex, shape[1])
            cv2.moveWindow(title, posX, posY)
            self.imgIndex += 1


    def printDebugInfo(self):

        print '\n'

        for k, v in self.debugStats.iteritems():
            print k + ':\t\t' + str(v)

        print '\n'
        # cv2.putText(background,'Debug Info coming soon',(10,100), font, 1,(255,255,255),1)
        # cv2.imshow(q'Debug Information', background)


    @staticmethod
    def findRegionOfInterest(image):

        #top vertex
        x1 = 40
        y1 = 40

        #bottom vertex
        x2 = 250
        y2 = 150

        roiFrame = image[y1:y2, x1:x2]

        return roiFrame
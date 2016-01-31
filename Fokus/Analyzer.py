import cv2
import sys
import CV_
import math
import copy
import Parameters
from CornerDetection import CornerDetection
import DebugOptions as tb
import numpy as np
import FeatureDebug
from ImageHelper import ImageHelper
from Morphology import Morphology
from PupilDetector import PupilDetector
from Threshold import Threshold
import Utils

selecting = False
startX = -1
startY = -1

INVALID = -1

COLOR_WHITE_LB = np.array([0,0,0])
COLOR_WHITE_UB = np.array([151,35,95])

def close():
    cv2.destroyAllWindows()

def forceExit():
    cv2.destroyAllWindows()
    sys.exit()


class Analyzer:

    #global variables

    startX = 0
    startY = 0

    #src is either a file name, or an image buffer
    def __init__(self, src, cameraType, params=None):

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
        self.params = Parameters.Parameters if params is None else params


    def loadImage(self):

        originalImage = self.originalImage.copy()
        self.imageCanny = self.originalImage.copy()

        if originalImage is None:
            raise NameError('Image not found!')

        ImageHelper.showImage('Original Image', originalImage)

        #Invert image with ~ and convert to grayscale
        self.imageGray = cv2.cvtColor(~originalImage, cv2.COLOR_BGR2GRAY)
        ImageHelper.showImage('Grey Image', self.imageGray)

        #Threshold image -> req. new Threshold obj

        self.thresholder = Threshold(self.imageGray, self.cameraType, self.params)
        self.imageThreshold = self.thresholder.getBinaryThreshold()
        self.thresholder.getAdaptiveThreshold(150, 3, -5)

        #Clean up the binary threshold image to get a better pupil representation
        morpher = Morphology(self.imageThreshold)
        processedImage = morpher.cleanImage()

        ####TEMP
        blur = cv2.GaussianBlur(self.imageCanny, (9, 9), 0)
        ImageHelper.showImage('Blurred', blur)
        lB, uB = self.params.Canny.getParams(self.cameraType)
        canny = cv2.Canny(blur, lB, uB)

        self.pupilDetector = PupilDetector(originalImage, processedImage, self.cameraType, self.saveInfo, self.params)
        self.pupilDetector.doHoughTransform()
        self.pupilDetector.findPupilCircle()

        #IR LED
        # self.findIrReflection(imageGray)

        if FeatureDebug.PRINT:
            self.printDebugInfo()

        #Parameter Tuner
        if Utils.isMac():
            tb.initHoughOptions(self.cameraType, self.updateParams)
            cv2.waitKey(1)

        else:
            print 'WARNING! Disabled parameter tuner, must test on BB'

        if Utils.isMac():
            keyPressed = cv2.waitKey()
            if keyPressed == ord('n'):
                cv2.destroyAllWindows()
            elif keyPressed == ord('e'):
                forceExit()

    def updateStats(self, info):
        self.saveInfo(info)

    def updateSelector(self, img, topRight, bottomLeft):
        pass

        cv2.rectangle(img, topRight, bottomLeft, BLUE, 2)
        # Imager.showImage('Yoloy', img)

    def onPointSelected(self, event,x,y,flags,param):

        # print 'onPointSelected -> x: {} y: {}'.format(x,y)
        regionSelected, x1,x2, y1, y2 = Analyzer.drawRectSelection(self, self.imageGray, event, x, y)

        if regionSelected:
            print 'region selected true'
            window = self.roi[y1+1:y2-1, x1+1:x2-1]
            hsvWindow = cv2.cvtColor(window, cv2.COLOR_BGR2HSV)
            hsvImage = cv2.cvtColor(self.originalImage, cv2.COLOR_BGR2HSV)
            ImageHelper.showImage('HSV Image', hsvImage[:,:,0])
            ImageHelper.showImage('HSV Image2', hsvImage[:,:,1])
            ImageHelper.showImage('HSV Image3e', hsvImage[:,:,2])
            hVals = hsvWindow[:, :, 0]
            sVals = hsvWindow[:, :, 1]
            vVals = hsvWindow[:, :, 2]

            avgH = np.mean(hVals)
            avgS = np.mean(sVals)
            avgV = np.mean(vVals)

            lb = np.array([avgH - 10, avgS - 10, avgV - 10], dtype=np.uint8, ndmin=1)
            up = np.array([avgH + 10, avgV + 10, avgV + 10], dtype=np.uint8, ndmin=1)

            mask = cv2.inRange(hsvImage, lb, up)

            # Imager.showImage('MASKKK', mask)

            result = cv2.bitwise_and(self.originalImage, self.originalImage, mask=mask)

            ImageHelper.showImage('HSV Selection', self.roi)
            ImageHelper.showImage('Result', result)

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
            ImageHelper.showImage('ROI', self.roi)
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

        if type is Parameters.Const.Trackbar.Canny:
            cannyLb = kwargs.get('cannyLb')
            cannyUp = kwargs.get('cannyUb')
            CornerDetection.findCornerCandidate(self.imageCanny, cannyLb, cannyUp)

        elif type is Parameters.Const.Trackbar.Hough:
            param1 = kwargs.get(Parameters.Const.PARAM_1)
            param2 = kwargs.get(Parameters.Const.PARAM_2)
            minRad = kwargs.get(Parameters.Const.MIN_RAD)
            maxRad = kwargs.get(Parameters.Const.MAX_RAD)
            self.pupilDetector.doHoughTransform(param1, param2, minRad, maxRad)

        elif type is Parameters.Const.Trackbar.AdaptiveThreshold:
            blockSize = kwargs.get(Parameters.Const.BLOCKSIZE)
            self.thresholder.getAdaptiveThreshold(blockSize)

    # def doSelectiveHoughTransform(self, srcImage, param1=None, param2 = None, minRadius = None, maxRadius = None):
    #
    #     houghTransformed = copy.deepcopy(self.originalImage)
    #
    #     houghCircles = CV_.HoughCirclesWithDefaultGradient(srcImage, DP, HOUGH_MIN_DIST,
    #                                None, param1, param2, minRadius, maxRadius)
    #
    #     #reset Image
    #     self.imgIndex = 0
    #
    #     if houghCircles is not None:
    #         circles = np.round(houghCircles[0, :]).astype("int")
    #         for (x,y,r) in circles:
    #             cv2.circle(houghTransformed, (x,y), r, RED, 1)
    #             lineLength = 2
    #             cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
    #             cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS),(0,0,255),1)
    #
    #         ImageHelper.showImage('Hough Circle', houghTransformed)
    #
    #     else:
    #         width, height = srcImage.shape
    #         cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
    #         ImageHelper.showImage('Hough Circle', houghTransformed)
    #
    #
    #
    #
    #
    #
    #
    #
    #     #use selective for iteration instead
    #     # while(houghCircles is None):
    #     #
    #     #     if (param2 is 1):
    #     #         print 'Failed!!!!'
    #     #         width, height = srcImage.shape
    #     #         cv2.putText(houghTransformed,"FAILED", (width/2, height/2), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))
    #     #         Imager.showImage('Hough Circle', houghTransformed)
    #     #
    #     #         break
    #     #
    #     #     param2 -= 1
    #     #     houghCircles = CV_.HoughCirclesWithDefaultGradient(srcImage, DP, houghMinDistance,
    #     #                            None, param1, param2, minRadius, maxRadius)
    #     #
    #     #     if houghCircles is not None:
    #     #         circles = np.round(houghCircles[0, :]).astype("int")
    #     #         for (x,y,r) in circles:
    #     #             cv2.circle(houghTransformed, (x,y), r, RED, 1)
    #     #             cv2.line(houghTransformed,(x - CROSSHAIRS, y - CROSSHAIRS),(x + CROSSHAIRS, y + CROSSHAIRS), RED, 1)
    #     #             cv2.line(houghTransformed,(x + CROSSHAIRS, y - CROSSHAIRS),(x - CROSSHAIRS, y + CROSSHAIRS), RED, 1)
    #     #
    #     #             Imager.showImage('Hough Circle', houghTransformed)

    # def findIrReflection(self, imageGray):
    #
    #     irImage = copy.deepcopy(self.originalImage)
    #
    #     center = self.debugStats.get(DEBUG_CENTER)
    #     radius = self.debugStats.get(DEBUG_RADIUS)
    #     xPupil, yPupil, widthPupil, heightPupil = self.debugStats.get(DEBUG_RECT)
    #
    #     # cropping to find ir led reflection
    #     xBoundLow = max(0, xPupil - 20)
    #     xBoundHigh = min(self.imgWidth, xPupil + radius*2 + 40)
    #     yBoundLow = max(0, yPupil - 20)
    #     yBoundHigh = min(self.imgHeight, yPupil + radius*2 + 30)
    #     cv2.rectangle(irImage, (yBoundHigh, xBoundHigh), (yBoundLow,xBoundLow), GREEN, 1)
    #     imgGrayCropped = ~imageGray[xBoundLow:xBoundHigh, yBoundLow:yBoundHigh]
    #     imgGrayBin = copy.deepcopy(imgGrayCropped)
    #     cv2.threshold(imgGrayBin, 200, MAXVAL, cv2.THRESH_BINARY, imgGrayBin)
    #
    #
    #     # get ir led reflection contour
    #     irContours, hier = CV_.findContours(imgGrayBin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #
    #     # take the first found contour
    #     if irContours:
    #         cnt = irContours[0]
    #
    #         # calculate centroid of ir contour
    #         M = cv2.moments(cnt)
    #         if M['m00'] == 0:
    #             pass
    #
    #         cx = int(M['m10']/M['m00'])
    #         cy = int(M['m01']/M['m00'])
    #
    #         # transform centroid back to original image coordinates
    #         irX = yBoundLow + cx
    #         irY = xBoundLow + cy
    #         cv2.circle(irImage, (irX,irY), 1, RED, 1)
    #
    #         # calculate distance between pupil and contour
    #         lenIrPupil = math.sqrt((irX-center[0])**2 + (irY-center[1])**2 )
    #         print lenIrPupil
    #
    #     # Analyzer.showImage(self, 'IR Reflection', irImage)

    def saveInfo(self, info):
        self.debugStats.update(info)

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
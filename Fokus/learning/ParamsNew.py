# from cv2 import SimpleBlobDetector_Params
import cv2

__author__ = 'Raphael'

MAC = 'Darwin'


#Responsible for holding all the parameters using by the Analyzer object




class ParamsNew(object):

    def __init__(self):
        pass
        self.thresh = Threshold()
        self.hough = Hough()
        self.canny = Canny()
        self.blob = SimpleBlobDetector()
        # self.TrackBar = Trackbar()


    def setHoughParams(self, param1=None, param2=None, minRadius=None, maxRadius=None):
        self.hough.param1 = param1
        self.hough.param2 = param2
        self.hough.minRadius = minRadius
        self.hough.maxRadius = maxRadius
        pass

    def setThresholdParams(self, minThresh=None, maxThresh=None, isNormalized=None):
        self.thresh.minThresh = minThresh
        self.thresh.maxThresh = maxThresh
        self.thresh.isNormalized = isNormalized
        pass

    def setCannyParams(self, lowerBound = None, upperBound = None):
        self.canny.lowerBound = lowerBound
        self.canny.upperBound = upperBound

    #Note this follows the Params structure from the SimpleBlobDetector params
    def setSimpleDetectorParams(self, maxArea = None, maxInertiaRatio = None, minInertiaRatio = None, filterByInertia = None, maxCircularity = None, minCircularity = None, maxConvexity = None, thresholdStep = None, minRepeatability = None, minDistBetweenBlobs = None, filterByColor = None, blobColor = None, filterByCircularity = None,  filterByConvexity = None , minConvexity = None, useNormalized = None, minThreshold = None, maxThreshold = None, filterByArea = None, minArea = None):
        self.blob.useNormalized = useNormalized
        self.blob.minThreshold = minThreshold
        self.blob.maxThreshold = maxThreshold
        self.blob.filterByArea = filterByArea
        self.blob.minArea = minArea
        self.blob.thresholdStep = thresholdStep
        self.blob.minRepeatability = minRepeatability
        self.blob.minDistBetweenBlobs = minDistBetweenBlobs
        self.blob.filterByColor = filterByColor
        self.blob.blobColor = blobColor
        self.blob.maxArea = maxArea
        self.blob.filterByCircularity = filterByCircularity
        self.blob.filterByConvexity = filterByConvexity
        self.blob.minConvexity = minConvexity
        self.blob.maxConvexity = maxConvexity
        self.blob.maxInertiaRatio = maxInertiaRatio
        self.blob.minInertiaRatio = minInertiaRatio
        self.blob.filterByInertia = filterByInertia
        self.blob.maxCircularity = maxCircularity
        self.blob.minCircularity = minCircularity

class Threshold():

    # _minThresh, _maxThresh = 0

    @property
    def minThresh(self):
        return self.minThresh

    @minThresh.setter
    def minThresh(self, val):
        self.minThresh = val

    @property
    def maxThresh(self):
        return self.maxThresh

    @maxThresh.setter
    def maxThresh(self, val):
        self.maxThresh = val

    # @property
    # def minNormalizedThresh(self):
    #     return self.minNormalizedThresh
    #
    # @minNormalizedThresh.setter
    # def minNormalizedThresh(self, value):
    #     self.minNormalizedThresh = value

    @property
    def isNormalized(self):
        return self.isNormalized

    @isNormalized.setter
    def isNormalized(self, value):
        self.isNormalized = value
        pass


    def __str__(self):
        return "Threshold -> min: %d | max: %d | normalizedMin: %d" % (self.minThresh, self.maxThresh, self.minNormalizedThresh)

class Hough():

    @property
    def minRadius(self):
        return self.minRadius

    @minRadius.setter
    def minRadius(self, value):
        self.minRadius = value

    @property
    def maxRadius(self):
        return self.maxRadius

    @maxRadius.setter
    def maxRadius(self, value):
        self.maxRadius = value

    @property
    def param1(self):
        return self.param1

    @param1.setter
    def param1(self, value):
        self.param1 = value

    @property
    def param2(self):
        return self.param2

    @param2.setter
    def param2(self, value):
        self.param2 = value

    def getParams(self):
        return (self.param1, self.param2, self.minRadius, self.maxRadius)

    def __str__(self):
        return "Hough -> minRadius: %d | maxRadius: %d | param1: %d | param2: %d" % (self.minRadius, self.maxRadius, self.param1, self.param2)

class Canny():

    @property
    def lowerBound(self):
        return self.lowerBound

    @lowerBound.setter
    def lowerBound(self, value):
        self.lowerBound = value


    @property
    def upperBound(self):
        return self.upperBound

    @upperBound.setter
    def upperBound(self, value):
        self.upperBound = value
        pass

class SimpleBlobDetector():

    @property
    def useNormalized(self):
        return self.useNormalized

    @useNormalized.setter
    def useNormalized(self, value):
        self.useNormalized = value
        pass

    @property
    def thresholdStep(self):
        return self.thresholdStep

    @thresholdStep.setter
    def thresholdStep(self, value):
        self.thresholdStep = value

    @property
    def minRepeatability(self):
        return self.minRepeatability

    @minRepeatability.setter
    def minRepeatability(self, value):
        self.minRepeatability = value

    @property
    def minDistBetweenBlobs(self):
        return self.minDistBetweenBlobs

    @minDistBetweenBlobs.setter
    def minDistBetweenBlobs(self, value):
        self.minDistBetweenBlobs = value

    @property
    def filterByColor(self):
        return self.filterByColor

    @filterByColor.setter
    def filterByColor(self, value):
        self.filterByColor = value

    @property
    def blobColor(self):
        return self.blobColor

    @blobColor.setter
    def blobColor(self, value):
        self.blobColor = value
        pass

    @property
    def maxInertiaRatio(self):
        return self.maxInertiaRatio

    @maxInertiaRatio.setter
    def maxInertiaRatio(self, value):
        self.maxInertiaRatio = value



    @property
    def minThreshold(self):
        return self.minThreshold

    @minThreshold.setter
    def minThreshold(self, value):
        self.minThreshold = value

    @property
    def maxThreshold(self):
        return self.maxThreshold

    @maxThreshold.setter
    def maxThreshold(self, value):
        self.maxThreshold = value

    @property
    def filterByArea(self):
        return self.filterByArea

    @filterByArea.setter
    def filterByArea(self, value):
        self.filterByArea = value
        pass

    @property
    def minArea(self):
        return self.minArea

    @minArea.setter
    def minArea(self, value):
        self.minArea = value

    @property
    def maxArea(self):
        return self.maxArea

    @maxArea.setter
    def maxArea(self, value):
        self.maxArea = value
        pass

    @property
    def filterByCircularity(self):
        return self.filterByCircularity

    @filterByCircularity.setter
    def filterByCircularity(self, value):
        self.filterByCircularity = value

    @property
    def minCircularity(self):
        return self.minCircularity

    @minCircularity.setter
    def minCircularity(self, value):
        self.minCircularity

    @property
    def maxCircularity(self):
        self.maxCircularity

    @maxCircularity.setter
    def maxCircularity(self, value):
        self.maxCircularity = value

    @property
    def filterByInertia(self):
        return self.filterByInertia

    @filterByInertia.setter
    def filterByInertia(self, value):
        self.filterByInertia = value

    @property
    def minInertiaRatio(self):
        return self.minInertiaRatio

    @minInertiaRatio.setter
    def minInertiaRatio(self, value):
        self.minInertiaRatio = value

    @property
    def minInertiaRatio(self):
        return self.minInertiaRatio

    @minInertiaRatio.setter
    def minInertiaRatio(self, value):
        self.minInertiaRatio = value

    @property
    def filterByConvexity(self):
        return self.filterByConvexity

    @filterByConvexity.setter
    def filterByConvexity(self, value):
        self.filterByConvexity = value

    @property
    def minConvexity(self):
        return self.minConvexity

    @minConvexity.setter
    def minConvexity(self, value):
        self.minConvexity = value

    @property
    def maxConvexity(self):
        return self.maxConvexity

    @maxConvexity.setter
    def maxConvexity(self, value):
        self.maxConvexity = value
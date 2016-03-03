__author__ = 'Raphael'

MAC = 'Darwin'


#Responsible for holding all the parameters using by the Analyzer object




class ParamsNew(object):

    def __init__(self):
        pass
        self.thresh = Threshold()
        self.hough = Hough()
        self.canny = Canny()
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

#
#     class Camera():
#         LEFT    = 0
#         RIGHT   = 1
#

#
#     class Canny():
#
#         LEFT_LOW_BOUND = 35
#         LEFT_UPPER_BOUND = 141
#
#         RIGHT_LOW_BOUND = 40
#         RIGHT_UPPER_BOUND = 167
#
#         @classmethod
#         def getParams(cls, cameraType):
#             if cameraType == Parameters.Camera.LEFT:
#                 return (cls.LEFT_LOW_BOUND, cls.LEFT_UPPER_BOUND)
#             else:
#                 return (cls.RIGHT_LOW_BOUND, cls.RIGHT_UPPER_BOUND)
#
#
#
# class Const():
#     PARAM_1 = 'param1'
#     PARAM_2 = 'param2'
#     MIN_RAD = 'minRadius'
#     MAX_RAD = 'maxRadius'
#
#     BLOCKSIZE = 'blockSize'
#
#
#     class Trackbar(Enum):
#         Hough = 1
#         Canny = 2
#         AdaptiveThreshold = 3
#
#
#
#
#
#
#
#
#
#

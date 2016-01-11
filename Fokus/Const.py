from enum import Enum
import Const

MAC = 'Darwin'


class Trackbar(Enum):
    Hough = 1
    Canny = 2
    AdaptiveThreshold = 3

class Camera():
    LEFT    = 0
    RIGHT   = 1

class Threshold():

    BLOCKSIZE = 'blockSize'

    LEFT    = 190
    RIGHT   = 205

    @classmethod
    def getMin(cls, cameraType):
        if cameraType == Const.Camera.LEFT:
            return cls.LEFT
        else:
            return cls.RIGHT


class HoughParamaters():

    PARAM_1 = 'param1'
    PARAM_2 = 'param2'
    MIN_RAD = 'minRadius'
    MAX_RAD = 'maxRadius'

    LEFT_MAX_RADIUS     = 40
    LEFT_MIN_RADIUS     = 5
    LEFT_PARAM_1        = 1
    LEFT_PARAM_2        = 40

    RIGHT_MAX_RADIUS    = 35
    RIGHT_MIN_RADIUS    = 8
    RIGHT_PARAM_1       = 1
    RIGHT_PARAM_2       = 46


    @classmethod
    def getParams(cls, cameraType):
        if cameraType == Const.Camera.LEFT:
            return (cls.LEFT_PARAM_1, cls.LEFT_PARAM_2, cls.LEFT_MIN_RADIUS, cls.LEFT_MAX_RADIUS)
        else:
            return (cls.RIGHT_PARAM_1, cls.RIGHT_PARAM_2, cls.RIGHT_MIN_RADIUS, cls.RIGHT_MAX_RADIUS)

class Canny():

    LEFT_LOW_BOUND = 35
    LEFT_UPPER_BOUND = 141

    RIGHT_LOW_BOUND = 40
    RIGHT_UPPER_BOUND = 167

    @classmethod
    def getParams(cls, cameraType):
        if cameraType == Const.Camera.LEFT:
            return (cls.LEFT_LOW_BOUND, cls.LEFT_UPPER_BOUND)
        else:
            return (cls.RIGHT_LOW_BOUND, cls.RIGHT_UPPER_BOUND)







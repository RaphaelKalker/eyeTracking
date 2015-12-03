from enum import Enum
import Const

MAC = 'Darwin'


class Trackbar(Enum):
    Hough = 1
    Canny = 2

class Camera():
    LEFT    = 0
    RIGHT   = 1

class Threshold():
    LEFT    = 190
    RIGHT   = 200

    @classmethod
    def getMin(cls, cameraType):
        if cameraType == Const.Camera.LEFT:
            return cls.LEFT
        else:
            return cls.RIGHT


class HoughParamaters():
    LEFT_MAX_RADIUS     = 40
    LEFT_MIN_RADIUS     = 0
    LEFT_PARAM_1        = 1
    LEFT_PARAM_2        = 40

    RIGHT_MAX_RADIUS    = 20
    RIGHT_MIN_RADIUS = 8
    RIGHT_PARAM_1       = 1
    RIGHT_PARAM_2       = 40


    @classmethod
    def getParams(cls, cameraType):
        if cameraType == Const.Camera.LEFT:
            return (cls.LEFT_PARAM_1, cls.LEFT_PARAM_2, cls.LEFT_MIN_RADIUS, cls.LEFT_MAX_RADIUS)
        else:
            return (cls.RIGHT_PARAM_1, cls.RIGHT_PARAM_2, cls.RIGHT_MIN_RADIUS, cls.RIGHT_MAX_RADIUS)




class RightHough():
    MAX_RADIUS      = 20
    MIN_MINRADIUS   = 8
    PARAM_1         = 1
    PARAM_2         = 40






import sys
from debug import FeatureDebug
from learning.ParamsNew import ParamsNew

__author__ = 'Raphael'

FUCKING_HUGE_NUMBER = sys.maxint

#Responsible for settings default values for Parameters object

class ParamsConstructor():

    def constructDefaultParams(self):

        params = ParamsNew()

        params.setThresholdParams(
            minThresh=180 if not FeatureDebug.NORMALIZE_GRAYSCALE else 230,
            maxThresh=255,
            isNormalized=FeatureDebug.NORMALIZE_GRAYSCALE
        )

        params.setHoughParams(
            param1=1,
            param2=40,
            minRadius=5,
            maxRadius=20
        )

        params.setCannyParams(
            lowerBound = 80,
            upperBound = 255
        )

        params.setSimpleDetectorParams(
            #default ones
            thresholdStep = 10,
            minRepeatability = 2,
            minDistBetweenBlobs = 10,
            filterByColor = True,
            blobColor = 0,
            maxArea = 5000,
            filterByCircularity = False,
            minCircularity = 0.8,
            maxCircularity = FUCKING_HUGE_NUMBER,
            filterByInertia = True,
            minInertiaRatio = 0.1,
            maxInertiaRatio = FUCKING_HUGE_NUMBER,
            filterByConvexity = True,
            minConvexity = .95,
            maxConvexity = FUCKING_HUGE_NUMBER,

            #We set these ones
            useNormalized = True,
            minThreshold = 1,
            maxThreshold = 50,
            filterByArea = True,
            minArea = 1
        )

        return params

# constructDefaultParams()

# def constructShit():
#
#     for i in range(1,100,1):
#         params.thresh.minThresh =i

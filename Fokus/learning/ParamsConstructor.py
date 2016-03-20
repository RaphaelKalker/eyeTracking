from debug import FeatureDebug
from learning.ParamsNew import ParamsNew

__author__ = 'Raphael'


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
            maxRadius=40
        )

        params.setCannyParams(
            lowerBound = 80,
            upperBound = 255
        )

        params.setSimpleDetectorParams(
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

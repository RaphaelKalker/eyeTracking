import FeatureDebug
from Parameters import Parameters
from learning.ParamsNew import ParamsNew

__author__ = 'Raphael'


#Responsible for settings default values for Parameters object

class ParamsConstructor():

    def constructDefaultParams(self):

        params = ParamsNew()

        params.setThresholdParams(
            minThresh=180 if not FeatureDebug.NORMALIZE_GRAYSCALE else 250,
            maxThresh=255,
            isNormalized=FeatureDebug.NORMALIZE_GRAYSCALE
        )

        params.setHoughParams(
            param1=1,
            param2=40,
            minRadius=5,
            maxRadius=40
        )

        print params.thresh.minThresh
        print params.thresh.maxThresh

        print params.hough.maxRadius


        return params


# constructDefaultParams()

# def constructShit():
#
#     for i in range(1,100,1):
#         params.thresh.minThresh =i

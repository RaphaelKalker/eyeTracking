from Parameters import Parameters
from learning.ParamsNew import ParamsNew

__author__ = 'Raphael'


#Responsible for settings default values for Parameters object

def constructDefaultParams():

    params = ParamsNew()

    params.setThresholdParams(
        minThresh=10,
        maxThresh=255,
        minNormalizedThresh=240
    )

    params.setHoughParams(
        param1=1,
        param2=40,
        minRadius=8,
        maxRadius=35
    )

    print params.thresh.minThresh
    print params.thresh.maxThresh

    print params.hough.maxRadius


    return params


constructDefaultParams()

# def constructShit():
#
#     for i in range(1,100,1):
#         params.thresh.minThresh =i

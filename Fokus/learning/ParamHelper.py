from learning.ParamsNew import ParamsNew

__author__ = 'Raphael'

MAX = 200

class ParamHelper():

    @property
    def sweeping(self):
        return self.sweeping

    @sweeping.setter
    def sweeping(self, value):
        self.sweeping = value


    def __init__(self):
        pass

    def __str__(self):
        return self.params.thresh.__str__() + "\t" + self.params.hough.__str__()

    def constructDefaultParams(self):

        self.params = ParamsNew()

        self.params.setThresholdParams(
            minThresh=10,
            maxThresh=255,
            minNormalizedThresh=240
        )

        self.params.setHoughParams(
            param1=1,
            param2=40,
            minRadius=8,
            maxRadius=35
        )

        return self.params


# constructDefaultParams()

    def constructNext(self):

        if self.params.thresh.minThresh < MAX:
            self.params.thresh.minThresh += 1

        elif self.params.thresh.maxThresh < MAX:
            self.params.thresh.maxThresh += 1

        elif self.params.hough.minRadius < MAX:
            self.params.hough.minRadius += 1

        else:
            #we are done
            return None

        print self
        return self.params



paramHelper = ParamHelper()
params = paramHelper.constructDefaultParams()

while (params is not None):
    params = paramHelper.constructNext()

# for i in range(1,100,1):
#     params.thresh.minThresh = i
#
#     for a in range(1,20,1):
#         params.thresh
from learning.ParamsNew import ParamsNew

SCHEMA = {"fileName":"","cameraType":"","color":"","verified":{"x":"","y":"","radius":""},"imageProperties":{"mean":"","variance":""},"heuristics":[{"histogramNormalized":"","threshold":"","hough":{"param1":"","param2":"","minRadius":"","maxRadius":"","x":"","y":"","radius":""},"contour":{"minRadius":"","x":"","y":"","radius":""},}]}

VERIFIED = 'verified'
X = 'x'
Y = 'y'
HEURISTICS = 'heuristics'

class EyeDict(object):

    def __init__(self, fileName = None):
        self.dict = SCHEMA
        self.dict['fileName'] = fileName


    def useParams(self, params):
        if isinstance(params, ParamsNew):
            print 'build eye from params'
            pass
        else:
            print 'Parameters instance is incorrect.'
            # raise ValueError('Parameters instance is incorrect.')

    def getDict(self):
        return self.dict

    def getFileName(self):
        return self.dict['fileName']

    def addPupilTruth(self, x, y):
        self.dict[VERIFIED][X] = x
        self.dict[VERIFIED][Y] = y
        pass

    def addThreshold(self, min, max, isNormalized):
        self.dict[HEURISTICS]
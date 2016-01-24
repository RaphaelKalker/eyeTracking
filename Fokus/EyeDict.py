

SCHEMA = {"fileName":"","cameraType":"","color":"","verified":{"x":"","y":"","radius":""},"imageProperties":{"mean":"","variance":""},"heuristics":[{"histogramNormalized":"","threshold":"","hough":{"param1":"","param2":"","minRadius":"","maxRadius":"","x":"","y":"","radius":""},"contour":{"minRadius":"","x":"","y":"","radius":""},}]}

class EyeDict(object):

    def __init__(self, fileName = None):
        self.dict = SCHEMA
        self.dict['fileName'] = fileName

    def getDict(self):
        return self.dict

    def getFileName(self):
        return self.dict['fileName']

    def addPupilTruth(self, x, y):
        self.dict['verified']['x'] = x
        self.dict['verified']['y'] = y
        pass
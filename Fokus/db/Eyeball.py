import datetime
import math
import Utils
from learning.ParamsNew import ParamsNew
import copy
import pprint

#Always make a deep copy when using these to create new dicts
# SCHEMA = {"fileName":"","cameraType":"","color":"","verified":{"x":"","y":"","isReading":"True","radius":""},"imageProperties":{"mean":"","variance":""},"heuristics":[]}
# SCHEMA_HEURISTICS = {"histogramNormalized":"","threshold":"","param1":"","param2":"","minRadius":"","maxRadius":"","minContourRadius":"","hough":{"x":"","y":"","radius":""},"contour":{"x":"","y":"","radius":""}}



RELFECTION_BLOB = 'reflection'
TRUTH = 'truth'
X = 'x'
Y = 'y'
SIZE = 'size'
RADIUS = 'radius'
HEURISTICS = 'heuristics'
HOUGH = "hough"
CONTOUR = "contour"
UPDATED_AT = "updated_at"
CAMERA = "camera"
FILENAME = "fileName"
CREATED_AT = "created_at"
PRESCRIPTION_TYPE = "prescription_type"
PERSON = "person"

CENTRE = 60



class Eyeball():

    class PrescriptionType():
        READING = 'reading'
        NON_READING = 'non_reading'
        UNKNOWN = '-1'

    class Person():
        TIM = 'tim'
        ANNI = 'anni'
        RAPH = 'raph'
        RYAN = 'ryan'

    class Camera():
        LEFT = 'left'
        RIGHT = 'right'
        UNKNOWN = '-1'

    class FilterOptions():
        REFLECTION = 'reflection'


    def __init__(self, fileName = None):
        self.dict = Utils.newDict({"fileName":"","camera":"","created_at":"","prescription_type":"","person":"","truth":{"x":"","y":""},"heuristics":[], "reflection":[]})
        self.dict['fileName'] = fileName

    def getDict(self):
        return self.dict

    def getHeuristics(self):
        return self.getDict()[HEURISTICS]

    def getFileName(self):
        return self.dict[FILENAME]

    def getCreatedAt(self):
        return self.dict[CREATED_AT]

    def getPrescriptionType(self):
        return self.dict[PRESCRIPTION_TYPE]

    def getPerson(self):
        return self.dict[PERSON]

    def getCameraType(self):
        return self.dict[CAMERA]

    def getRandomPupilTruth(self):
        heuristics = self.getDict()[HEURISTICS]

        x = -1
        y = -1

        for h in heuristics:

            if 'contour' in h:
                xNew = h['contour']['x']
                yNew = h['contour']['y']

                if abs(xNew - CENTRE) < abs(x - CENTRE):
                    x = xNew
                    y = yNew

        return (x, y)

    def getPupilCentreCandidate(self, filterOptions = None):

        minDistance = -1
        xLikely,yLikely = 0, 0

        if filterOptions == self.FilterOptions.REFLECTION:
            heuristics = self.getDict()[HEURISTICS]
            referencePoints = self.getDict()[RELFECTION_BLOB]

            if not referencePoints:
                return self.getRandomPupilTruth()


            for h in heuristics:
                if HOUGH in h:
                    xHough = h[HOUGH][X]
                    yHough = h[HOUGH][Y]

                    for ref in referencePoints:
                        xRef = ref[Y] #yes this is flipped, probably because of the way the mask was created
                        yRef = ref[X]

                        newDist = math.sqrt((xRef - xHough)**2 + (yRef - yHough)**2)

                        if newDist < minDistance or minDistance == -1:
                            minDistance = newDist
                            xLikely, yLikely = xHough, yHough

            return xLikely, yLikely

        else:
            return self.getRandomPupilTruth()
    def addPupilTruth(self, x, y):
        self.dict[TRUTH][X] = x
        self.dict[TRUTH][Y] = y
        self.setTimeStamp()
        pass

    def addThreshold(self, min, max, isNormalized):
        raise NotImplementedError('threshold not implemented')

    #warning immuatable errors here
    def addHoughCircle(self, x, y, r):
        heuristics = {}
        hough = {}
        heuristics[HOUGH] = hough

        heuristics[HOUGH][X] = x
        heuristics[HOUGH][Y] = y
        heuristics[HOUGH][RADIUS] = r

        self.dict[HEURISTICS].append(heuristics)
        self.setTimeStamp()


    def addContourCircle(self, x, y, r):
        heuristics = {}
        contour = {}
        heuristics[CONTOUR] = contour

        heuristics[CONTOUR][X] = x
        heuristics[CONTOUR][Y] = y
        heuristics[CONTOUR][RADIUS] = r

        self.dict[HEURISTICS].append(heuristics)
        self.setTimeStamp()

    def addReflection(self, x, y, size):
        reflection = {}
        self.dict[RELFECTION_BLOB]
        reflection[X] = x
        reflection[Y] = y
        reflection[SIZE] = size
        self.dict[RELFECTION_BLOB].append(reflection)
        self.setTimeStamp()

    def getReflection(self):
        return self.getDict()[RELFECTION_BLOB]


    def setTimeStamp(self):
        self.dict[CREATED_AT] = datetime.datetime.now().isoformat()

    def setPerson(self, personName):
        self.dict[PERSON] = personName

    def setCamera(self, cameraType):
        self.dict[CAMERA] = cameraType

    def setPrescriptionType(self, prescriptionType):
        self.dict[PRESCRIPTION_TYPE] = prescriptionType



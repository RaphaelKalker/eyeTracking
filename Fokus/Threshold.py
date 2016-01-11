import cv2
import Const
import FeatureDebug
from ImageHelper import ImageHelper

__author__ = 'Raphael'


THRESH = 220 #the threshold value
MAXVAL = 255 #the maximum value


class Threshold(object):

    def __init__(self, image, cameraType):
        self.image = image
        self.cameraType = cameraType

    def preProcessGrayScale(self):
        cv2.equalizeHist(self.image, self.image)
        ImageHelper.showImage('Normalized', self.image)
        pass

    def getBinaryThreshold(self):
        minThresh = Const.Threshold.getMin(self.cameraType)
        # maxThresh = Const.Threshold.getMax(self.cameraType)

        if FeatureDebug.NORMALIZE_GRAYSCALE:
            self.preProcessGrayScale()
            minThresh = Const.Threshold.getNormalizedMin(self.cameraType)

        _, output = cv2.threshold(self.image, minThresh, MAXVAL, cv2.THRESH_BINARY)
        _, output2 = cv2.threshold(self.image, minThresh, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


        ImageHelper.showImage('Threshold Image', output)
        ImageHelper.showImage('Otsu Image', output2)

        return output

    def getAdaptiveThreshold(self, maxVal, blockSize, c):
        outputAdaptive = cv2.adaptiveThreshold(self.image, maxVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, c)
        ImageHelper.showImage('Adaptive Thresh', outputAdaptive)




    def getOtsuBinaryThreshold(self):
        raise NotImplementedError()
        pass
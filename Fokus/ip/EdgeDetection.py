import cv2
import numpy as np

__author__ = 'Raphael'


class EdgeDetection():

    def __init__(self, image, params):
        self.image = image
        self.params = params

    def doCanny(self, lB=None, uB=None):

        if lB is None:
            lB = self.params.canny.lowerBound

        if uB is None:
            uB = self.params.canny.upperBound

        edgeMap = cv2.Canny(self.image, lB, uB)

        return edgeMap

    def doAutoCanny(self):
        v = np.median(self.image)
        sigma=0.33

        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        return self.doCanny(lower, upper)



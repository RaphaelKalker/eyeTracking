import cv2
import numpy as np
import FeatureDebug
from ImageHelper import ImageHelper

__author__ = 'Raphael'

class Morphology(object):

    def __init__(self, img):
        self.img = img

    def cleanImage(self):

        kernel = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(self.img, kernel, iterations = 1)
        if FeatureDebug.MORPHOLOGY_IMAGES: ImageHelper.showImage('1. Dilated', dilation)

        erosion = cv2.erode(dilation, kernel, iterations = 3)
        if FeatureDebug.MORPHOLOGY_IMAGES: ImageHelper.showImage('2. Erosion', erosion)

        opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel, iterations=3)
        if FeatureDebug.MORPHOLOGY_IMAGES: ImageHelper.showImage('3. Opening', opening)

        dilation = cv2.dilate(opening, kernel, iterations = 3)
        if FeatureDebug.MORPHOLOGY_IMAGES: ImageHelper.showImage('4. Dilated', dilation)

        result = dilation

        return result


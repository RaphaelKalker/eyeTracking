import cv2

from debug import FeatureDebug
from ImageHelper import ImageHelper
from ip.PupilDetector import YELLOW

__author__ = 'Raphael'


class ReflectionReduction:
    def __init__(self, image):
        self.image = image
        pass

    def doStuff(self, fileName):
        pass
        hsvImg = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        h,s,v = cv2.split(hsvImg)

        if FeatureDebug.DEBUG_DRAW_TRUTH:
            from db import Database as db
            self.db = db
            self.image = self.__drawTruth__(self.image, fileName)

        processedH = self.image.copy()
        processedS = self.image.copy()

        _, h_thresh = cv2.threshold(h, 60, 255, cv2.THRESH_BINARY_INV)
        _, s_threshed = cv2.threshold(s, 50, 60, cv2.THRESH_BINARY)

        #apply mask to image
        processedH = cv2.bitwise_and(self.image,self.image, mask = h_thresh)
        processedS = cv2.bitwise_and(self.image,self.image, mask = s_threshed)


        ImageHelper.showImage('Original', self.image)
        # ImageHelper.showImage('HSV', hsvImg)
        ImageHelper.showImage('H', h)
        ImageHelper.showImage('S', s)
        ImageHelper.showImage('V', v)
        ImageHelper.showImage('h_threshed',h_thresh)
        # ImageHelper.showImage('h_mask_threshed', self.__drawTruth__(processedH, fileName))
        ImageHelper.showImage('s_threshed', s_threshed)
        # ImageHelper.showImage('s_mask_threshed', self.__drawTruth__(processedS, fileName))

        return processedH



    def __drawTruth__(self, image, fileName):
        annotated, (x,y) = self.db.getTruth(fileName)
        if annotated:
            cv2.circle(image, (x,y), 5, YELLOW, -1)
            return image





import cv2
import numpy as np
from ImageHelper import ImageHelper

__author__ = 'Raphael'

DEBUG_IMAGES = True

class Segmentation():

    def __init__(self, image):
        self.image = image

    def getMask(self):
        pass


        height, width, channels = self.image.shape

        #create a mask to remove some of the image which is irrelevant
        mask = np.zeros((height,width,channels), np.uint8)

        mask[0:0.66*height,:] = (255,255,255)
        #mask[0:1*height,:] = (255,255,255)

        img = cv2.cvtColor(cv2.bitwise_and(mask, self.image), cv2.COLOR_BGR2HSV)

        #first scale up the values
        minH, maxH, _, _ = cv2.minMaxLoc(img[:,:,0])
        minS, maxS, _, _ = cv2.minMaxLoc(img[:,:,1])

        Hchannel = (img[:,:,0]*255.0/float(maxH)).astype(np.uint8)
        Schannel = (img[:,:,1]*255.0/float(maxS)).astype(np.uint8)

        #for the fuzzy type AND do MIN. Fuzzy type OR do MAX

        minImage = cv2.min(Hchannel, Schannel)
        minI, maxI, _, _ = cv2.minMaxLoc(minImage)
        _, minImg = cv2.threshold(cv2.blur((minImage[:,:]*255.0/float(maxI)).astype(np.uint8), (10,10)), 110, 255, cv2.THRESH_BINARY)

        if  DEBUG_IMAGES:
            # ImageHelper.showImage('H', Hchannel)
            # ImageHelper.showImage('S', Schannel)
            # ImageHelper.showImage('V', self.image)
            ImageHelper.showImage('Mask', minImg)

        return minImg

    def getSegmentedImage(self):
        mask = self.getMask()
        segmentedImage = cv2.bitwise_and(self.image[:,:,2], mask)
        return segmentedImage
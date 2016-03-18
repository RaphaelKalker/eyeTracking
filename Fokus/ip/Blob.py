import logging
import cv2
import numpy as np
import sys
from ImageHelper import ImageHelper
from debug import FeatureDebug

__author__ = 'Raphael'

USE_MASK = True
WHITE = 255
INVALID = 0

logger = logging.getLogger('Blob')


class Blob(object):

    def __init__(self, grayscaleImage, eyeBall, mask, params):
        self.image = grayscaleImage
        self.eyeBall = eyeBall
        self.mask = mask
        self.params = params

    def findReflectionPoints(self):

        detector = cv2.SimpleBlobDetector_create(self.params.blob)

        keypoints = detector.detect(self.image)
        validKP = []

        for point in keypoints:
            x = int(point.pt[0])
            y = int(point.pt[1])
            size = '%.2f' % point.size


            # Filter out key points according to mask
            # We do this because the mask passed into the Simple Blob Detector doesn't work
            # WARNING orientation is reverse so use y, x coordinates
            if  self.mask[y,x] == WHITE:
                logging.debug('REFLECTION: x={} y={} size={}'.format(x,y, size))
                self.eyeBall.addReflection(y,x, size)
                validKP.append(point)
            else:
                # logger.debug('IGNORED: x={} y={} size={}'.format(x,y, size))
                pass

        if  FeatureDebug.SHOW_CV2_IMAGES and FeatureDebug.DEBUG_BLOB_DETECTOR:
            mask_with_keypoints = cv2.drawKeypoints(self.mask, keypoints, None, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            im_with_keypoints = cv2.drawKeypoints(self.image, validKP, None, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            ImageHelper.showImage('Blob Starting Image', self.image)
            ImageHelper.showImage('Mask with Points', mask_with_keypoints)
            ImageHelper.showImage('Mask applied', cv2.bitwise_and(im_with_keypoints,im_with_keypoints, mask=self.mask))

        return validKP
import cv2
import numpy as np

__author__ = 'Raphael'

class Blob(object):

    def __init__(self, grayscaleImage):
        self.image = grayscaleImage

    def detect(self):

        params = cv2.SimpleBlobDetector_Params()

        params.minThreshold = 1
        params.maxThreshold = 255

        params.filterByArea = True
        params.minArea = 1

        params.filterByCircularity = True
        params.minCircularity = 1

        params.filterByConvexity = True
        params.minConvexity = 1

        params.filterByInertia = True
        params.minInertiaRatio = 1

        detector = cv2.SimpleBlobDetector_create(params)

        keypoints = detector.detect(self.image)
        im_with_keypoints = cv2.drawKeypoints(self.image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return im_with_keypoints



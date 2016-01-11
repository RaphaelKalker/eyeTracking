import cv2
import Analyzer
import Const
from ImageHelper import ImageHelper

__author__ = 'Raphael'

class CornerDetection(object):

    @classmethod
    def findCornerCandidate(cls, img, lowerBound, upperBound):
        pass
        # blur = cv2.GaussianBlur(img, (9, 9), 0)
        # ImageHelper.showImage('Blurred', blur)
        #
        # edges = cv2.Canny(blur, lowerBound, upperBound)
        # ImageHelper.showImage('Canny', edges)
        # dst = cv2.cornerHarris(edges, 3, 21, 0.2)
        # dst = cv2.dilate(dst, None)
        #
        # candidatesYX =  (dst > 0.01 * dst.max()).nonzero()
        #
        # if not candidatesYX or len(candidatesYX[0]) == 0 or len(candidatesYX[1]) == 0:
        #     print 'Failed to find corners!'
        # else:
        #     ind = candidatesYX[1].argmax(axis=0)
        #
        #     (mostLikelyX, mostLikelyY) = (candidatesYX[0][ind], candidatesYX[1][ind])
        #
        #     self.saveInfo({(Analyzer2.DEBUG_CANDIDATE_CORNER, (mostLikelyX, mostLikelyY))})
        #
        #     corners = self.originalImage.copy()
        #     corners[candidatesYX[0], candidatesYX[1]] = [0,0,255]
        #     offset = 3
        #     corners[mostLikelyX -offset : mostLikelyX + offset, mostLikelyY - offset: mostLikelyY + offset] = [0,255,255]
        #
        #     ImageHelper.showImage('Corners', corners)

        #x,y are switched

import cv2
import numpy as np
import Analyzer
import sys

WINDOW = 'Options'

PARAM1 = 'Param 1'
PARAM2 = 'Param 2'
MIN_RAD = 'Minimum Radius'
MAX_RAD = 'Maximum Radius'


def nothing(x):
    pass

def initHoughOptions():

    # Create a black image, a window
    img = np.zeros((1,300,3), np.uint8)
    cv2.namedWindow(WINDOW)

    cv2.createTrackbar(PARAM1, WINDOW, 0, Analyzer.HOUGH_PARAM1, nothing)
    cv2.createTrackbar(PARAM2, WINDOW, 0, Analyzer.HOUGH_MAX_PARAM2, nothing)
    cv2.createTrackbar(MIN_RAD, WINDOW, 0, 255, nothing)
    cv2.createTrackbar(MAX_RAD, WINDOW, 0, Analyzer.HOUGH_MAX_RADIUS, nothing)

    # Switch to default -
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, WINDOW, 0, 1, nothing)

    while(1):
        cv2.imshow(WINDOW,img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            Analyzer.close()
            break
        elif k == ord('e'):
            sys.exit('Force Close')

        # get current positions of four trackbars
        p1 = cv2.getTrackbarPos(PARAM1, WINDOW)
        p2 = cv2.getTrackbarPos(PARAM2, WINDOW)
        minR = cv2.getTrackbarPos(MIN_RAD, WINDOW)
        maxR = cv2.getTrackbarPos(MAX_RAD, WINDOW)

        #todo if vals change then update analyzer

    cv2.destroyWindow(WINDOW)






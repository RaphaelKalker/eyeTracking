import cv2
import numpy as np
import Analyzer
import sys
import Const

WINDOW = 'Options'

PARAM1 = '1) Param 1'
PARAM2 = '2) Param 2'
MIN_RAD = '3) Minimum Radius'
MAX_RAD = '4) Maximum Radius'
WINDOW_BOUND = '5) Top Left Window Px'
WINDOW_BOUND2 = '6) Top Right Window px'

HOUGH_PARAM1 = 1
HOUGH_MAX_PARAM2 = 300
HOUGH_MIN_RADIUS = 0
HOUGH_MAX_RADIUS = 40
HOUGH_MIN_DIST = 20 # the minimum distance two detected circles can be from one another
HOUGH_MAX_ATTEMPTS = 100 #define the number of attempts to find at least one circle

CANNY_LOW = '7) Canny LB'
CANNY_HIGH = '8) Canny UP'

p1 = 0
p2 = 0
minR = 0
maxR = 0
cannyLb = 0
cannyUb = 0


def nothing(dummyVar = None):
    pass

def initHoughOptions(callback):

    global p1, p2, minR, maxR, cannyUb, cannyLb

    # Create a black image, a window
    img = np.zeros((200,300,3), np.uint8)
    cv2.namedWindow(WINDOW)
    cv2.createTrackbar(PARAM1, WINDOW, 0, Analyzer.HOUGH_PARAM1, nothing)
    cv2.createTrackbar(MIN_RAD, WINDOW, 0, 255, nothing)
    cv2.createTrackbar(PARAM2, WINDOW, 0, Analyzer.HOUGH_MAX_PARAM2, nothing)
    cv2.createTrackbar(MAX_RAD, WINDOW, 0, Analyzer.HOUGH_MAX_RADIUS, nothing)
    cv2.createTrackbar(WINDOW_BOUND, WINDOW, 0, 100, nothing)
    cv2.createTrackbar(CANNY_LOW, WINDOW, 0, 255, nothing)
    cv2.createTrackbar(CANNY_HIGH, WINDOW, 0, 255, nothing)

    cv2.setTrackbarPos(PARAM1, WINDOW, HOUGH_PARAM1)
    cv2.setTrackbarPos(PARAM2, WINDOW, 40)
    cv2.setTrackbarPos(MIN_RAD, WINDOW, HOUGH_MIN_RADIUS)
    cv2.setTrackbarPos(MAX_RAD, WINDOW, HOUGH_MAX_RADIUS)

    cv2.setTrackbarPos(CANNY_LOW, WINDOW, 35)
    cv2.setTrackbarPos(CANNY_HIGH, WINDOW, 150)

    while(1):
        cv2.imshow(WINDOW,img)
        cv2.moveWindow(WINDOW, 0, 500)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            Analyzer.close()
            break
        elif k == ord('e'):
            sys.exit('Force Close')

        p1Temp = cv2.getTrackbarPos(PARAM1, WINDOW)
        p2Temp = cv2.getTrackbarPos(PARAM2, WINDOW)
        minRTemp = cv2.getTrackbarPos(MIN_RAD, WINDOW)
        maxRTemp = cv2.getTrackbarPos(MAX_RAD, WINDOW)
        cannyLbTemp = cv2.getTrackbarPos(CANNY_LOW, WINDOW)
        cannyUbTemp = cv2.getTrackbarPos(CANNY_HIGH, WINDOW)

        updated = False

        if p1Temp != p1:
            p1 = p1Temp
            updated = True

        if p2Temp != p2:
            p2 = p2Temp
            updated = True

        if minRTemp != minR:
            minR = minRTemp
            updated = True

        if maxRTemp != maxR:
            maxR = maxRTemp
            updated = True

        if cannyLbTemp != cannyLb:
            cannyLb = cannyLbTemp
            updated = True

        if cannyUbTemp != cannyUb:
            cannyUb = cannyUbTemp
            updated = True

        if updated:
            # callback(param1 = p1, param2 = p2, minRadius = minR, maxRadius = maxR)
            callback(Const.Trackbar.Canny, cannyLb = cannyLb, cannyUb = cannyUb)

    cv2.destroyWindow(WINDOW)






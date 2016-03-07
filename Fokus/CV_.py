import cv2



def findContours(image, mode, method, contours=None, hierarchy=None, offset=None):

    if  cv2.__version__ == '3.0.0':
        i, c, h = cv2.findContours(image, mode, method, contours, hierarchy, offset)
    else:
        c, h = cv2.findContours(image, mode, method, contours, hierarchy, offset)

    return c,h


def HoughCirclesWithDefaultGradient(image, dp, minDist, circles=None, param1=None, param2=None, minRadius=None, maxRadius=None):

    if cv2.__version__ == '3.0.0':
        return cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, minDist,
                                   circles, param1, param2, minRadius, maxRadius)

    else:
        return cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, dp, minDist,
                                   circles, param1, param2, minRadius, maxRadius)
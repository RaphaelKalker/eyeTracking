import cv2



def findContours(image, mode, method, contours=None, hierarchy=None, offset=None):

    if  cv2.__version__ == '3.0.0':
        i, c, h = cv2.findContours(image, mode, method, contours, hierarchy, offset)
    else:
        c, h = cv2.findContours(image, mode, method, contours, hierarchy, offset)

    return c,h




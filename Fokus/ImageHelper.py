import time
import platform
import cv2
import Const

import FeatureDebug

#
if FeatureDebug.MATLABLIB:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg


__author__ = 'Raphael'

FEATURE_ENABLED = True

class ImageHelper(object):

    newestIndex = 0
    imageDict = {}
    my_dict = {'cheese': 'cake'} #class variable - shared

    @classmethod
    def showImage(cls, title, image):

        if platform.system() == Const.MAC and FeatureDebug.IMAGES:

            cv2.imshow(title, image)
            timestamp = int(round(time.time() * 1000))
            cv2.imwrite('../results/' + title + str(timestamp) + '.jpg', image)
            shape = image.shape

            if title not in cls.imageDict:
                cls.imageDict.update({title : cls.newestIndex})
                cls.newestIndex = cls.newestIndex + 1

            posX, posY = cls.getWindowPosition(cls.imageDict.get(title), shape[1])
            cv2.moveWindow(title, posX, posY)


    @classmethod
    def histogram(cls, img):
        plt.hist(img.ravel(),256,[0,256])
        plt.show()

    @classmethod
    def getWindowPosition(cls, imageNr, imageWidth):
        return (imageNr * imageWidth, 0)



import time

import cv2

import FeatureDebug


#
import Utils

if FeatureDebug.MATLABLIB:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider



__author__ = 'Raphael'

FEATURE_ENABLED = True

class ImageHelper(object):

    newestIndex = 0
    imageDict = {}
    my_dict = {'cheese': 'cake'} #class variable - shared

    @classmethod
    def showImage(cls, title, image):

        if Utils.isMac() and FeatureDebug.MATLABLIB:
            cls.invokeMatplotLib(title, image)
            pass


        elif Utils.isMac() and FeatureDebug.IMAGES:

            cv2.imshow(title, image)
            shape = image.shape

            if FeatureDebug.SAVE_IMAGES:
                timestamp = int(round(time.time() * 1000))
                cv2.imwrite('../results/' + title + str(timestamp) + '.jpg', image)

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


    @classmethod
    def invokeMatplotLib(cls, title, image):
            fig, axis = plt.subplots()

            #Create sliders
            axcolor = 'lightgoldenrodyellow'

            axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
            axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
            raAmp = plt.axes([0.25, 0.2, 0.65, 0.03], axisbg=axcolor)

            sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=3)
            samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=5)
            slider = Slider(raAmp, 'Raph', 2, 40, valinit=1)

            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.get_current_fig_manager().window.wm_geometry("+0+0")
            # fig.canvas.mpl_connect('button_press_event', self.onPointSelected)
            # fig.canvas.mpl_connect('key_press_event', self.onKeyPressed)
            plt.waitforbuttonpress()
            plt.close(fig)

    @classmethod
    def update(val):
        print



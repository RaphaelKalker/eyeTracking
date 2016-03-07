import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


class AdjustableImage():

    def __init__(self):
        pass

    def updateHough(self, ignoreThisVal):
            print self.slider_houghparam1.val

            self.callback(
                param1 = self.slider_houghparam1.val,
                param2 = self.slider_houghparam2.val,
                minRad = self.slider_houghminRad.val,
                maxRad = self.slider_houghmaxRad.val
            )



    def doIt(self, image, callback, params):

        # global slider_houghparam1
        self.callback = callback



        fig = plt.figure(figsize=(10,15))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # params.hough.minRadius
        # params.hough.param1
        # params.hough.param2
        # params.hough.maxRadius

        # for axis in params:
        #     minVal = 1
        #     maxVal = 30
        #     initVal = 10
        #     left = 0.1
        #     bottom = 0.1
        #     width = .65
        #     height = .03
        #     ax = plt.axes([left, bottom, width, height])
        #     slider = Slider(ax, 'title', )


        axis_houghparam1 = plt.axes([0.1, 0.2, 0.65, 0.03], axisbg='lightgoldenrodyellow')
        self.slider_houghparam1 = Slider(axis_houghparam1, 'Param1', 1, 30, valinit=params.hough.param1, valfmt='%0.0f')
        self.slider_houghparam1.on_changed(self.updateHough)

        axis_houghparam2 = plt.axes([0.1, 0.16, 0.65, 0.03], axisbg='lightgoldenrodyellow')
        self.slider_houghparam2 = Slider(axis_houghparam2, 'Param2', 1, 30, valinit=params.hough.param2, valfmt='%0.0f')
        self.slider_houghparam2.on_changed(self.updateHough)

        axis_houghminRad = plt.axes([0.1, 0.12, 0.65, 0.03], axisbg='lightgoldenrodyellow')
        self.slider_houghminRad = Slider(axis_houghminRad, 'Param2', 1, 30, valinit=params.hough.minRadius, valfmt='%0.0f')
        self.slider_houghparam2.on_changed(self.updateHough)

        axis_houghmaxRad = plt.axes([0.1, 0.08, 0.65, 0.03], axisbg='lightgoldenrodyellow')
        self.slider_houghmaxRad = Slider(axis_houghmaxRad, 'Param2', 1, 30, valinit=params.hough.maxRadius, valfmt='%0.0f')
        self.slider_houghmaxRad.on_changed(self.updateHough)

        plt.show()

    def updateImage(self, newImage):
        if newImage is not None:
            plt.imshow(cv2.cvtColor(newImage, cv2.COLOR_BGR2RGB))
            # plt.show()
        pass

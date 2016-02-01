import os
import cv2
import database
from EyeDict import EyeDict

if True:
    cv2.destroyAllWindows() #avoids crash
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import pylab
    import matplotlib.image as mpimg

RED = (0,0,255)

class TruthSet(object):

    def __init__(self, filePath):
        pass

        self.dbHelper = database.Database()
        self.cycle(filePath)

    def onPointSelected(self, event):

        if event.xdata is None or event.ydata is None:
            #wasn't a valid click, don't close the window yet!
            plt.waitforbuttonpress()
            return

        print ' x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.x, event.y, event.xdata, event.ydata)

        eyeball = EyeDict(self.fileName)
        eyeball.addPupilTruth(int(event.xdata), int(event.ydata))

        self.dbHelper.addEyeball(eyeball)


    def cycle(self, filePath):
        os.chdir(filePath)
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.jpeg') or f.endswith('.jpg')]

        for file in files:
            self.image = cv2.imread(file.__str__(), 0)
            self.annotated = self.image.copy()
            self.fileName = file.__str__()

            print '\nLoading ' + self.fileName

            fig = plt.figure()
            plt.imshow(self.image, cmap='magma')
            plt.get_current_fig_manager().window.wm_geometry("+0+0")
            fig.canvas.mpl_connect('button_press_event', self.onPointSelected)
            plt.waitforbuttonpress()
            plt.close(fig)

    def initMouseCallback(self, fileName):
        cv2.namedWindow(fileName)
        cv2.setMouseCallback(fileName, self.onPointSelected)
        pass


#run your stuff here
ts = TruthSet('image/tim_jan13')




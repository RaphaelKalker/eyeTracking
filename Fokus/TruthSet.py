import os
import cv2
from Database import Database
from Eyeball import Eyeball
import FeatureDebug

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

        self.dbHelper = Database()
        self.cycle(filePath)


    def onKeyPressed(self, event):

        if event.key == 'n':
            print 'Pressed: ' + event.key + ': Skip this eyeball'
            self.addEyeBall(self.fileName, -1, -1)

        else:
            plt.waitforbuttonpress()






    def onPointSelected(self, event):

        if event.xdata is None or event.ydata is None:
            #wasn't a valid click, don't close the window yet!
            plt.waitforbuttonpress()
            return

        print ' x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.x, event.y, event.xdata, event.ydata)

        self.addEyeBall(self.fileName, event.xdata, event.ydata)


    def cycle(self, filePath):
        os.chdir(filePath)
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.jpeg') or f.endswith('.jpg')]

        for file in files:

            self.fileName = file.__str__()

            if FeatureDebug.START_TRUTH_FROM_PREV:
                if self.dbHelper.eyeBallExists(self.fileName):
                    print 'Skipped filename'
                    continue

            self.image = cv2.imread(file.__str__(), 1)
            self.annotated = self.image.copy()

            print '\nLoading ' + self.fileName

            fig = plt.figure()
            plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            plt.get_current_fig_manager().window.wm_geometry("+0+0")
            fig.canvas.mpl_connect('button_press_event', self.onPointSelected)
            fig.canvas.mpl_connect('key_press_event', self.onKeyPressed)
            plt.waitforbuttonpress()
            plt.close(fig)

    def initMouseCallback(self, fileName):
        cv2.namedWindow(fileName)
        cv2.setMouseCallback(fileName, self.onPointSelected)
        pass

    def addEyeBall(self, fileName, x, y):
        eyeball = Eyeball(fileName)
        eyeball.addPupilTruth(str(int(x)), str(int(y)))
        self.dbHelper.addEyeball(eyeball)

        pass


#run your stuff here
ts = TruthSet('image/tim_jan13')




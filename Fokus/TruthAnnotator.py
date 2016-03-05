import pprint
import os
import cv2
import time

from db.Database import Database
from Eyeball import Eyeball
import FeatureDebug

if True:
    cv2.destroyAllWindows() #avoids crash
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

RED = (0,0,255)

class AnnotationSession():
    def __init__(self, dbName, person, prescriptionType, imagePath, cameraType):
        self.dbName = dbName
        self.person = person
        self.prescriptionType = prescriptionType
        self.filePath = imagePath
        self.cameraType = cameraType

class TruthAnnotator(object):

    def __init__(self, session):

        if not isinstance(session, AnnotationSession):
            raise AssertionError('Use the DatabaseConstructor to build params for annotation')

        self.dbHelper = Database(session.dbName)
        self.session = session
        self.cycle(session.filePath)


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


    def cycle(self):
        os.chdir(self.session.filePath)
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
        eyeball.setTimeStamp()
        eyeball.setPerson(self.session.person)
        eyeball.setCamera(self.session.cameraType)
        eyeball.setPrescriptionType(self.session.prescriptionType)
        self.dbHelper.addEyeball(eyeball) #change this
        pprint.pprint(eyeball.getDict())

        pass

#run your stuff here
annotator = TruthAnnotator(
    AnnotationSession(
        dbName= 'db-{}'.format(int(round(time.time() * 1000))),
        person = Eyeball.Person.TIM,
        prescriptionType = Eyeball.PrescriptionType.READING,
        imagePath= 'image/tim_jan13',
        cameraType = Eyeball.Camera.LEFT
    )
)

annotator.cycle()






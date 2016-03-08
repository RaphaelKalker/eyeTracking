import pprint
import time
import argparse

import os
import cv2

from db.Database import Database
from db.Eyeball import Eyeball
from debug import FeatureDebug

if True:
    cv2.destroyAllWindows()  # avoids crash
    import matplotlib

    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

RED = (0, 0, 255)


class AnnotationSession():
    def __init__(self, dbName, person, prescriptionType, imagePath):
        self.dbName = dbName
        self.person = person
        self.prescriptionType = prescriptionType
        self.filePath = imagePath


class TruthAnnotator(object):
    def __init__(self, session):

        if not isinstance(session, AnnotationSession):
            raise AssertionError('Use the DatabaseConstructor to build params for annotation')

        self.dbHelper = Database(session.dbName)
        self.session = session

    def onKeyPressed(self, event):

        if event.key == 'n':
            print 'Pressed: ' + event.key + ': Skip this eyeball'
            self.addEyeBall(self.fileName, -1, -1)

        else:
            plt.waitforbuttonpress()

    def onPointSelected(self, event):

        if event.xdata is None or event.ydata is None:
            # wasn't a valid click, don't close the window yet!
            plt.waitforbuttonpress()
            return

        print ' x=%d, y=%d, xdata=%f, ydata=%f' % (
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
        # first character of file name indicates left or right side camera
        cameraSide = "left" if fileName[0] == "L" else "right" if fileName[0] == "R" else "none"  
        eyeball.setCamera(cameraSide)
        eyeball.setPrescriptionType(self.session.prescriptionType)
        self.dbHelper.addEyeball(eyeball)  # change this
        pprint.pprint(eyeball.getDict())

        pass

parser = argparse.ArgumentParser()
parser.add_argument("person", type=str, help="whose eyeballs? tim, raph, ryan, or anni")
parser.add_argument("image_path", type=str, help="image directory")
parser.add_argument("prescriptionType", type=str, help="r for reading or d for distance")
parser.add_argument("database_name", type=str, help="existing or new database name")
args = parser.parse_args()

prescription="reading" if args.prescriptionType == "r" else "distance" if args.prescriptionType == "d" else "unknown"

# run your stuff here
annotator = TruthAnnotator(
    AnnotationSession(
        dbName="db-" + args.database_name,
        person=args.person.lower(),
        prescriptionType=prescription,
        imagePath=args.image_path
    )
)

annotator.cycle()

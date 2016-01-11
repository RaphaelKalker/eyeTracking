import os
from Analyzer import Analyzer
import Const
import Utils
import time

if Utils.isBeagalBone():
    import sys
    import Cam2
    import Cam1
    sys.path.insert(0, '../pyCam/')

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'


def processImages():
    os.chdir(PROCESSING_DIR)

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for image in files:

        if image.startswith('L'):
            left = Analyzer(image, Const.Camera.LEFT)
            left.loadImage()
            pass
        elif image.startswith('R'):
            # right = Analyzer2(image, Const.Camera.RIGHT)
            # right.loadImage()
            pass

        else:
            pass

if  __name__ == '__main__':

    if Utils.isBeagalBone():
        print 'Init BB System'
        # initialize cameras
        camRight = Cam1.Cam1(IMAGE_DIRECTORY)
        camLeft = Cam2.Cam2(IMAGE_DIRECTORY)

        # looping to capture and process images
        for i in range(1,100):
            timestamp = int(time.time())
            camRight.takeImg()
            camLeft.takeImg()

            rightImg = camRight.getImg(timestamp)
            leftImg = camLeft.getImg(timestamp)

            print "process image in Analyzer2"

            time.sleep(1)

        # close connections to cameras
        cam1.closeConn()
        cam2.closeConn()

        print "process image in Analyzer2"
    else:
        print 'Init Mac System'
        processImages()

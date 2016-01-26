import os
from Analyzer import Analyzer
import Const
import Utils
import time
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if Utils.isBeagalBone():
    sys.path.insert(0, '../pyCam/')
    import Cam1
    import Cam2

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'
PROCESSING_DIR = 'processing/'
PROCESSING_DIR_JAN_11 = 'image/Jan11'


def processImages():
    os.chdir(PROCESSING_DIR_JAN_11)

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for image in files:

        if not image.endswith('.jpg'):
            continue #skip 

        if image.startswith('L'):
            left = Analyzer(image, Const.Camera.LEFT)
            left.loadImage()
            pass
        elif image.startswith('R'):
            # right = Analyzer2(image, Const.Camera.RIGHT)
            # right.loadImage()
            pass

        else:
            left = Analyzer(image, Const.Camera.LEFT)
            left.loadImage()
            pass

if  __name__ == '__main__':

    if Utils.isBeagalBone():
        logger.info('Init BB System')

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

#            print "process image in Analyzer2"
            time.sleep(1)

        # close connections to cameras
        cam1.closeConn()
        cam2.closeConn()

    else:
        logger.info('Init Mac System')
        processImages()

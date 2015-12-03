import cv2
#from Analyzer import Analyzer
from Analyzer2 import Analyzer2
#from redis import Redis
#from rq import Queue

import sys
sys.path.insert(0, '../pyCam/')
import Cam2
import Cam1
import time

import os


# class Start(object):

DEFAULT_DIRECTORY = 'imageLeftCam'
IMAGE_DIRECTORY = './processing/'

def analyzeImages():


    rootDir = '.'

    for dirName, subDirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.__contains__('jpg') and dirName.__contains__(DEFAULT_DIRECTORY):
                a = Analyzer2(DEFAULT_DIRECTORY + '/' + fname)
                a.loadImage()


def analyzeSimulatedBuffer(src):

    originalImage = cv2.imread(DEFAULT_DIRECTORY + '/' + src)
    success,imageBuf = cv2.imencode('.jpg', originalImage)

    a = Analyzer2(imageBuf)
    a.loadImage()

if  __name__ == '__main__':

    # q = Queue(connection=Redis())


    # resultLeft = q.enqueue(takeLeftPicture())
    # resultRight = q.enqueue(takeRightPicture())
    #
    # analyzeImages()
#    analyzeSimulatedBuffer('image1398285888.jpg')

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

import cv2
#from Analyzer import Analyzer
from Analyzer2 import Analyzer2
#from redis import Redis
#from rq import Queue

import sys
sys.path.insert(0, '../pyCam/')
import Cam2
import Cam1

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

def takeLeftPicture():
    print 'takeLeftPicutre'
    cam2 = Cam2.Cam2(IMAGE_DIRECTORY)
    cam2.takeImg()
    leftImgDir = cam2.getImg()
    cam2.closeConn()
    print leftImgDir
    return leftImgDir

def takeRightPicture():
    print 'takeRightPicture'
    cam1 = Cam1.Cam1(IMAGE_DIRECTORY)
    cam1.takeImg()
    rightImgDir = cam1.getImg()
    cam1.closeConn()
    print rightImgDir
    return rightImgDir

if  __name__ == '__main__':

    # q = Queue(connection=Redis())


    # resultLeft = q.enqueue(takeLeftPicture())
    # resultRight = q.enqueue(takeRightPicture())
    #
    # analyzeImages()
#    analyzeSimulatedBuffer('image1398285888.jpg')
    leftImg = takeLeftPicture()
    rightImg = takeRightPicture()
    print "process image in Analyzer2"
#    a = Analyzer2(leftImg)
#    a.loadImage()

import cv2
from Analyzer import Analyzer
from Analyzer2 import Analyzer2
from redis import Redis
from rq import Queue

import os


# class Start(object):

DEFAULT_DIRECTORY = 'imageLeftCam'

def analyzeImages():


    rootDir = '.'

    for dirName, subDirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.__contains__('jpg') and dirName.__contains__(DEFAULT_DIRECTORY):
                a = Analyzer2(DEFAULT_DIRECTORY + '/' + fname)
                a.loadImage()


def analyzeSimulatedBuffer(src):

    originalImage = cv2.imread('image/' + src)
    success,imageBuf = cv2.imencode('.jpg', originalImage)

    a = Analyzer(imageBuf)
    a.loadImage()

def takeLeftPicture():
    print 'takeLeftPicutre'
    ##analyze

def takeRightPicture():
    print 'takeRightPicture'

if  __name__ == '__main__':

    q = Queue(connection=Redis())


    resultLeft = q.enqueue(takeLeftPicture())
    resultRight = q.enqueue(takeRightPicture())
    
    analyzeImages()
    # analyzeSimulatedBuffer('aa2.jpg')





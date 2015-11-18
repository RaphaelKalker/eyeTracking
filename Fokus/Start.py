import cv2
from Analyzer import Analyzer
import os


# class Start(object):

def analyzeImages():

    rootDir = '.'

    for dirName, subDirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.__contains__('jpg') and dirName.__contains__('image'):
                # print fname
                a = Analyzer(fname)
                a.loadImage()


def analyzeSimulatedBuffer(src):

    originalImage = cv2.imread('image/' + src)
    success,imageBuf = cv2.imencode('.jpg', originalImage)

    a = Analyzer(imageBuf)
    a.loadImage()

if  __name__ == '__main__':
    analyzeImages()
    # analyzeSimulatedBuffer('aa2.jpg')





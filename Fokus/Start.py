from Analyzer import Analyzer
import PupilDetection as PD
import os


class Start(object):

    if  __name__ == '__main__':
        # PD.PupilDetection.doItqLive()
        a = Analyzer()
        a.loadImage('pupil-detect-src-img.jpg')


        rootDir = '.'

        for dirName, subDirList, fileList in os.walk(rootDir):
            print 'found'
            for fname in fileList:
                if fname.__contains__('bmp'):
                    a.loadImage(fname)
                    print 'fname'

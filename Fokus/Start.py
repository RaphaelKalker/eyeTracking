from Analyzer import Analyzer
import os


class Start(object):

    if  __name__ == '__main__':
        # a = Analyzer()

        rootDir = '.'

        for dirName, subDirList, fileList in os.walk(rootDir):
            for fname in fileList:
                if fname.__contains__('jpg') and dirName.__contains__('image'):
                    print fname
                    a = Analyzer(fname)
                    a.loadImage()

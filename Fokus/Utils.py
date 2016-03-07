import copy
import platform

def isBeagalBone():
    return platform.system() != 'Darwin'

def isMac():
    return platform.system() == 'Darwin'

def newDict(item):
    return dict(copy.deepcopy(item))
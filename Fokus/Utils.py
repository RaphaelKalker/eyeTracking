import platform

def isBeagalBone():
    return platform.system() != 'Darwin'

def isMac():
    return platform.system() == 'Darwin'

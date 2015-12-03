import platform

def isBeagalBone():
    return platform.system() != 'Darwin'

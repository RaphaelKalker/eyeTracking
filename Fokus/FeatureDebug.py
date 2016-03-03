import Utils

__author__ = 'Raphael'

SHOW_CV2_IMAGES = True

SAVE_IMAGES = False
TRACKBAR = False
MORPHOLOGY_IMAGES = False
MORPHOLOGY = False
BLUR = True
THRESHOLD = True
MATLABLIB = False #This causes crashes, probably because opencv has some matplotlib stuff
NORMALIZE_GRAYSCALE = True
START_TRUTH_FROM_PREV = True
VERIFY_TRUTH = True

#DEBUG WINDOW
DEBUG_PUPIL_DETECTOR = False

#PRINT DEBUG
PRINT_HEURISTICS = True
DEBUG_DRAW_TRUTH = False if Utils.isBeagalBone() else False
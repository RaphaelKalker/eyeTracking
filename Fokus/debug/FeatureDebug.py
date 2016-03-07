import Utils

__author__ = 'Raphael'

SHOW_CV2_IMAGES = True

SAVE_IMAGES = False
TRACKBAR = False
MORPHOLOGY_IMAGES = False
MORPHOLOGY = False
BLUR = True
THRESHOLD = True
MATLABLIB = False if Utils.isMac() else False
NORMALIZE_GRAYSCALE = True
START_TRUTH_FROM_PREV = False
VERIFY_TRUTH = True

#DEBUG WINDOW
DEBUG_PUPIL_DETECTOR = False if Utils.isMac() else False

#PRINT DEBUG
PRINT_HEURISTICS = True
DEBUG_DRAW_TRUTH = False if Utils.isMac() else False
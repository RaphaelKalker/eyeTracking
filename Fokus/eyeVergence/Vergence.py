import logging
import math

logger = logging.getLogger(__name__)

class Vergence():
    def __init__(self, leftImg_f, rightImg_f):

        self.refPt = [0.0, 0.0]
 
        self.l_id = leftImg_f
        self.r_id = rightImg_f

    def detectVergence(self, l_pupil, r_pupil):
        reading = False
        
        l_deltaX = l_pupil[0] - self.refPt[0]
        l_deltaY = l_pupil[1] - self.refPt[1]
        r_deltaX = r_pupil[0] - self.refPt[0]
        r_deltaY = r_pupil[1] - self.refPt[1]

        l_vec = math.sqrt(l_deltaX**2 + l_deltaY**2)
        r_vec = math.sqrt(r_deltaX**2 + r_deltaY**2)

        # logic to compare the vector lengths with some threshold
        logger.info("left %.2f", l_vec)
        logger.info("right %.2f", r_vec)

        # need more logic here to decide near or far

        res = "NEAR" if reading else "FAR"
        return res 

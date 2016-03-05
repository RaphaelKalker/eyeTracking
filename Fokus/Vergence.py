import sys
import time
import serial
import copy
import logging
import math
from db import Database
from tinydb import TinyDB, Query

logger = logging.getLogger(__name__)

class Vergence():
    def __init__(self, leftImg_f, rightImg_f):

        self.refPt = [0.0, 0.0]
 
        self.l_id = leftImg_f
        self.r_id = rightImg_f
        
        valid, self.l_pupil = Database.getTruth(self.l_id)
        valid, self.r_pupil = Database.getTruth(self.r_id)

    def detectVergence(self, ):
        reading = False
        
        l_deltaX = self.l_pupil[0] - self.refPt[0]
        l_deltaY = self.l_pupil[1] - self.refPt[1]
        r_deltaX = self.r_pupil[0] - self.refPt[0]
        r_deltaY = self.r_pupil[1] - self.refPt[1]

        l_vec = math.sqrt(l_deltaX**2 + l_deltaY**2)
        r_vec = math.sqrt(r_deltaX**2 + r_deltaY**2)

        # logic to compare the vector lengths with some threshold
        logger.info("left %.2f", l_vec)
        logger.info("right %.2f", r_vec)

        # need more logic here to decide near or far

        res = "NEAR" if reading else "FAR"
        return res 

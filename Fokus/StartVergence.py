import sys
import time
import Utils
import logging
import argparse
from eyeVergence import Vergence
from db import Database

parser = argparse.ArgumentParser()
parser.add_argument("database_path", type=str, help="database path")
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

db_handle = Database.Database(args.database_path)

def computeVergence(timestamp):
    leftImg = "L" + timestamp
    rightImg = "R" + timestamp
    
    frame_vergence = Vergence.Vergence(leftImg, rightImg)
    l_valid, l_pupil = db_handle.getTruth(leftImg)
    r_valid, r_pupil = db_handle.getTruth(rightImg)
    if l_valid and r_valid:
        res = frame_vergence.detectVergence(l_pupil,r_pupil)
        logger.info("%s\t%s", timestamp, res)

if  __name__ == '__main__':
    if Utils.isBeagalBone():
        raise AssertionError('The system was not meant for the beaglebone! Use StartBB.py')

    frames_list = db_handle.getSearchFileMatch('^L')
    for frame in frames_list:
        timestamp = frame['fileName'][1:]
        computeVergence(timestamp)

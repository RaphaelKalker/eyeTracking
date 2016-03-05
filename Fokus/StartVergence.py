import sys
import time
import Utils
import logging
import argparse
import Vergence
from tinydb import TinyDB, Query

parser = argparse.ArgumentParser()
parser.add_argument("database_path", type=str, help="database path")
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

def computeVergence(timestamp):
    leftImg = "L" + timestamp
    rightImg = "R" + timestamp
    
    frame_vergence = Vergence.Vergence(leftImg, rightImg)
    res = frame_vergence.detectVergence()
    logger.info("%s\t%s", timestamp, res)

if  __name__ == '__main__':
    if Utils.isBeagalBone():
        raise AssertionError('The system was not meant for the beaglebone! Use StartBB.py')

    db_obj = TinyDB(args.database_path)
    frames_list = db_obj.search(Query().fileName.matches('^L'))
    for frame in frames_list:
        timestamp = frame['fileName'][1:]
        computeVergence(timestamp)

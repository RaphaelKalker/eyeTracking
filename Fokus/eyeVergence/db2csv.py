import sys
import csv
from db import Database

def getPupils(dh, timestamp):
    leftImg = "L" + timestamp
    rightImg = "R" + timestamp
    
    l_valid, l_pupil = dh.getTruth(leftImg)
    r_valid, r_pupil = dh.getTruth(rightImg)
    if l_valid and r_valid:
        return (l_pupil, r_pupil)

with open(sys.argv[3], 'w') as f:
    writer = csv.writer(f)
    writer.writerow( ("r_x", "r_y", "l_x", "l_y", 'prescription') )

    db_reading = Database.Database(sys.argv[1])
    r_list = db_reading.getSearchFileMatch('^L')
    for frame in r_list:
        ret = getPupils(db_reading, frame['fileName'][1:])
        if ret:
            writer.writerow( (ret[0][0], ret[0][1], ret[1][0], ret[1][1], 0) )

    db_distance = Database.Database(sys.argv[2])
    d_list = db_distance.getSearchFileMatch('^L')
    for frame in d_list:
        ret = getPupils(db_distance, frame['fileName'][1:])
        if ret:
            writer.writerow( (ret[0][0], ret[0][1], ret[1][0], ret[1][1], 1) )
    
    print "number of reading frames: %i" % (len(r_list))
    print "number of distance frames: %i" % (len(d_list))

import sys
import csv
from db import Database

#USAGE: python db2csv.py <DB1 path> <DB2 path> <csv name>

#def getPupilsDISTANCE(dh, timestamp):
#    leftImg = "L" + timestamp
#    rightImg = "R" + timestamp
#    
#    l_valid, l_pupil = dh.getTruth(leftImg)
#    r_valid, r_pupil = dh.getTruth(rightImg)
#    if l_valid and r_valid:
#        return (l_pupil, r_pupil)
#
#def getPupilsREADING(dh, timestamp):
#    leftImg = "R" + timestamp
#    rightImg = "L" + timestamp
#    
#    l_valid, l_pupil = dh.getTruth(leftImg)
#    r_valid, r_pupil = dh.getTruth(rightImg)
#    if l_valid and r_valid:
#        return (l_pupil, r_pupil)

def getPupils(dh, timestamp):
    leftImg = "R" + timestamp
    rightImg = "L" + timestamp
    
    l_valid, l_pupil = dh.getTruth(leftImg)
    r_valid, r_pupil = dh.getTruth(rightImg)
    if l_valid and r_valid:
        img = dh.getImage(leftImg)
        p_type = img[0]['prescription_type']
        return [l_pupil, r_pupil, p_type]

#with open(sys.argv[3], 'w') as f:
with open(sys.argv[2], 'w') as f:
    writer = csv.writer(f)
    writer.writerow( ("r_x", "r_y", "l_x", "l_y", 'prescription') )

    db_reading = Database.Database(sys.argv[1])
    r_list = db_reading.getSearchFileMatch('^L')
    for frame in r_list:
        ret = getPupils(db_reading, frame['fileName'][1:])
        if ret:
            pres = 0 if ret == 'reading' else 1
            writer.writerow( (ret[0][0], ret[0][1], ret[1][0], ret[1][1], pres) )
#
#    db_distance = Database.Database(sys.argv[2])
#    d_list = db_distance.getSearchFileMatch('^L')
#    for frame in d_list:
#        ret = getPupilsDISTANCE(db_distance, frame['fileName'][1:])
#        if ret:
#            writer.writerow( (ret[0][0], ret[0][1], ret[1][0], ret[1][1], 1) )
    
    print "number of reading frames: %i" % (len(r_list))
    print "number of distance frames: %i" % (len(d_list))

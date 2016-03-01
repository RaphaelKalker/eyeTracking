import os
import Utils
if Utils.isMac():
    from tinydb import TinyDB, Query

__author__ = 'Raphael'

SUBPATH = 'database'
DB = SUBPATH + '/imgDB-2.json'


###

global helper

databasePath = DB
if not os.path.exists(SUBPATH):
    os.makedirs(SUBPATH)

helper = TinyDB(databasePath)

def getImage(identifier):
    return helper.get(Query().fileName == identifier)

def getTruth(identifier):
    entry = getImage(identifier)

    x = entry['truth']['x']
    y = entry['truth']['y']

    #some times the value is stored as a unicode string, we need an int
    if isinstance(x, basestring):
        x = int(x)
        y = int(y)

    validEntry =  False if entry is None or x == -1 or y == -1 else True

    # if (entry is None or
    #     x == -1 or
    #     y == -1):
    #     return False, (x, x)


    return validEntry, (x, y)

###


class Database(object):

    def __init__(self, databasePath=None):

        if databasePath is None:
            databasePath = DB
            if not os.path.exists(SUBPATH):
                os.makedirs(SUBPATH)

        self.db = TinyDB(databasePath)
        self.Eyeball = Query()

    def getImage(self, identifier):
        return self.db.search(self.Eyeball.fileName == identifier)
        item = self.db.get(eid =3)

    def cycleThroughImages(self, path):

        self.db.update(EXAMPLE_JSON2, self.Eyeball.fileName == '1234567899.jpg')
        self.getImage('')

        os.chdir(path)

        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.jpg')]

        for image in files:
            self.db.insert(self.constructFields(image.__str__()))

    def addEyeball(self, eyeBallObj):

        condition = self.Eyeball.fileName == eyeBallObj.getFileName()

        if self.db.contains(condition):
            el = self.db.get(condition)
            self.db.update(eyeBallObj.getDict(), eids=[el.eid])
            print 'Edited existing item with eid: ' + str(el.eid)

        else:
            retVal = self.db.insert(eyeBallObj.getDict())
            print 'Added new item with eid: ' + str(retVal)


    def eyeBallExists(self, fileName):
        return self.db.contains(self.Eyeball.fileName == fileName)










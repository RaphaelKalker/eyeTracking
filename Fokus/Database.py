import os
from tinydb import TinyDB, Query

__author__ = 'Raphael'

SUBPATH = 'database'
DB = SUBPATH + '/imgDB-2.json'

class Database(object):

    def __init__(self, databasePath=None):

        if databasePath is None:
            databasePath = DB
            if not os.path.exists(SUBPATH):
                os.makedirs(SUBPATH)

        self.db = TinyDB(databasePath)
        self.Eyeball = Query()
        self.getImage('')

    def getImage(self, identifier):
        print self.db.search(self.Eyeball.fileName == '1234567899.jpg')

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










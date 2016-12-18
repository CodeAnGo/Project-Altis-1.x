from libpandadna import *

class DNABulkLoader:
    def __init__(self, storage, files):
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print 'Load Files:Reading DNA file...', file
            loadDNABulk(self.dnaStorage, file)
        del self.dnaStorage
        del self.dnaFiles

def loadDNABulk(dnaStorage, file):
    dnaLoader = DNALoader()
    if __dev__:
        file = 'resources/' + file
    dnaLoader.loadDNAFile(dnaStorage, file)

def loadDNAFile(dnaStorage, dnafile):
    print 'LoadFile: Reading DNA file...', dnafile
    dnaLoader = DNALoader()
    if __dev__:
        dnafile = 'resources/' + dnafile
    node = dnaLoader.loadDNAFile(dnaStorage, dnafile)
    try:
        if node.node().getNumChildren() > 0:
            return node.node()
    except:
        pass

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    if __dev__:
        file = 'resources/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, file)
    return data
    print 'Loading DNA File: ', file

def setupDoor(a, b, c, d, e, f):
    try:
        e = int(str(e).split('_')[0])
    except:
        print 'setupDoor: error parsing', e
        e = 9999

    DNADoor.setupDoor(a, b, c, d, e, f)


from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase import Loader
from toontown.dna.DNAParser import *
from direct.stdpy.file import open
from direct.stdpy import threading

class ToontownAsyncLoader(Loader.Loader):

    def __init__(self, base):
        Loader.Loader.__init__(self, base)
        return
        
    def loadModel(self, *args, **kw):
        ret = Loader.Loader.loadModel(self, *args, **kw)
        return ret
        
    def destroy(self):
        Loader.Loader.destroy(self)

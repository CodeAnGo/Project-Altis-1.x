from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
import DistributedGagTreeAI, DistributedFlowerAI, GardenGlobals

class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenPlotAI")

    def __init__(self, air, ownerId):
        DistributedLawnDecorAI.__init__(self, air, ownerId)
        
        self.plot = GardenGlobals.EmptyPlot

    def plantFlower(self, todo0, todo1):
        pass

    def plantGagTree(self, todo0, todo1):
        pass

    def plantStatuary(self, todo0):
        pass

    def plantToonStatuary(self, todo0, todo1):
        pass

    def plantNothing(self, todo0):
        pass

    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)
        
        self.plot = gardenData.getUint8()
        
    def pack(self, gardenData):
        DistributedLawnDecorAI.pack(self, gardenData)
        gardenData.addUint8(self.plot)

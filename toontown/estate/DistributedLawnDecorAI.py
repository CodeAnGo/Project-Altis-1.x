from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI
import GardenGlobals

class DistributedLawnDecorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawnDecorAI")

    def __init__(self, air, ownerId):
        DistributedNodeAI.__init__(self, air)

        self.ownerId = ownerId

        self.plotIndex = None
        self.plotType = None

        self.pos = None
        self.heading = None

    def getPlot(self):
        return self.plotIndex

    def getHeading(self):
        return self.heading

    def getPosition(self):
        return self.pos

    def getOwnerIndex(self):
        return self.ownerIndex

    def plotEntered(self):
        pass

    def removeItem(self):
        pass

    def setMovie(self, todo0, todo1):
        pass

    def movieDone(self):
        pass

    def interactionDenied(self, todo0):
        pass

    def construct(self, gardenData):
        self.plotIndex = gardenData.getUint8()

        self.plotType = GardenGlobals.getPlotType(self.ownerIndex, self.plotIndex)
        self.pos = GardenGlobals.getPlotPos(self.ownerIndex, self.plotIndex)
        self.heading = GardenGlobals.getPlotHeading(self.ownerIndex, self.plotIndex)

    def pack(self, gardenData):
        gardenData.addUint8(self.plotIndex)

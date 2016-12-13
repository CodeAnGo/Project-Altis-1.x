from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedDGFlowerAI
import HoodAI
from toontown.toon import NPCToons
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.safezone import DistributedTrolleyAI

class DGHoodAI(HoodAI.HoodAI):
    __slots__ = ('air', 'zoneId', 'canonicalHoodId', 'fishingPonds', 'partyGates', 'treasurePlanner', 'buildingManagers', 
		 'suitPlanners', 'trolley', 'butterflies', 'flower', 'classicChar')

    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.DaisyGardens,
                               ToontownGlobals.DaisyGardens)

        self.trolley = None
        self.butterflies = []
        self.flower = None
        self.classicChar = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        self.createFlower()
        if simbase.config.GetBool('want-butterflies', True):
            self.createButterflies()
        
        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(5620)

    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)

        ButterflyGlobals.clearIndexes(self.zoneId)

    def createButterflies(self):
        playground = ButterflyGlobals.DG
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.zoneId)
                self.butterflies.append(butterfly)
				
    def createFlower(self):
        self.flower = DistributedDGFlowerAI.DistributedDGFlowerAI(self.air)
        self.flower.generateWithRequired(self.zoneId)
        self.flower.start()
		
    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

from toontown.classicchars import DistributedMickeyAI
from toontown.hood import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI

class TTHoodAI(HoodAI.HoodAI):
    __slots__ = ('air', 'zoneId', 'canonicalHoodId', 'fishingPonds', 'partyGates', 'treasurePlanner', 
                 'buildingManagers', 'suitPlanners', 'trolley', 'butterflies')

    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.ToontownCentral,
                               ToontownGlobals.ToontownCentral)

        self.trolley = None
        self.butterflies = []

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-butterflies', True):
            self.createButterflies()

        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(2649)

        if simbase.air.wantChristmas:
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(2649)

    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)

        ButterflyGlobals.clearIndexes(self.zoneId)


    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.zoneId)
                self.butterflies.append(butterfly)
				
    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

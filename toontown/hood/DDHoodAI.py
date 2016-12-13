from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toon import NPCToons
import HoodAI

class DDHoodAI(HoodAI.HoodAI):
    __slots__ = ('air', 'zoneId', 'canonicalHoodId', 'fishingPonds', 'partyGates', 'treasurePlanner', 
                 'buildingManagers', 'suitPlanners', 'trolley', 'boat')
	
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.DonaldsDock,
                               ToontownGlobals.DonaldsDock)

        self.trolley = None
        self.boat = None

        self.startup()
		
    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        self.createBoat()
                
        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(1834)

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

    def createBoat(self):
        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.zoneId)
        self.boat.start()

from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.building.DistributedBuildingMgrAI import DistributedBuildingMgrAI
from toontown.safezone.DistributedTrolleyAI import DistributedTrolleyAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.safezone import TreasureGlobals
from toontown.town.StreetAI import StreetAI
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.dna.DNAParser import DNAStorage, DNAGroup, DNAVisGroup
from toontown.toon import NPCToons
from toontown.environment import DistributedDayTimeManagerAI
from toontown.environment import DistributedRainManagerAI

class SZHoodAI(HoodAI):
    """
    AI-side representation of everything in a single safezone neighborhood.

    One subclass of this class exists for every neighborhood in the game.
    HoodAIs are responsible for spawning all TreasurePlanners, ponds, 
    and other hood objects, etc.
    """

    def __init__(self, air):
        HoodAI.__init__(self, air)

        self.safezone = self.HOOD
        self.streets = {}

        self.trolley = None
        self.pond = None
        self.buildingMgr = None
        
        # If it is a time where we want snow
        self.wantSnow = True

        self.createZone()
        self.createStreets()
        #self.createTime()
        self.createRain()

    def createZone(self, genTrolley = True):
        HoodAI.createZone(self)
        dnaStore = DNAStorage()
        self.air.dnaStoreMap[self.HOOD] = dnaStore
        if genTrolley:
            self.createTrolley()
        self.createTreasurePlanner()
        self.buildingMgr = DistributedBuildingMgrAI(self.air, self.HOOD, self.air.dnaStoreMap[self.HOOD], self.air.trophyMgr)
        NPCToons.createNpcsInZone(self.air, self.HOOD)

    def createStreets(self):
        branchIds = ToontownGlobals.HoodHierarchy.get(self.HOOD, [])
        for branch in branchIds:
            street = StreetAI(self.air, branch)
            self.streets[branch] = street

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.safezone)

    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[self.HOOD]
        self.treasurePlanner = SZTreasurePlannerAI(self.safezone, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def spawnObjects(self):
        filename = self.air.genDNAFileName(self.safezone)
        self.air.dnaSpawner.spawnObjects(filename, self.safezone)
        
    def createTime(self):
        if self.HOOD != 9000:
            self.dayTimeMgr = DistributedDayTimeManagerAI.DistributedDayTimeManagerAI(self.air)
            self.dayTimeMgr.generateWithRequired(self.HOOD)  
            self.dayTimeMgr.start()
            self.notify.info('Day Time Manager turned on for zone ' + str(self.HOOD))
            
    def createRain(self):
        self.rainMgr = DistributedRainManagerAI.DistributedRainManagerAI(self.air)
        self.rainMgr.generateWithRequired(self.HOOD)  
        if self.HOOD == 1000 or self.wantSnow:
            self.rainMgr.start(True) # We want it to always rain in donalds dock
        else:
            self.rainMgr.start(False)
        self.notify.info('Rain Manager turned on for zone ' + str(self.HOOD))

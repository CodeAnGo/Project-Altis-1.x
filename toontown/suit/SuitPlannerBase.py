from panda3d.core import *
from panda3d.direct import *
import random
import string
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals
from toontown.hood import ZoneUtil, HoodUtil
from toontown.building import SuitBuildingGlobals
from toontown.dna.DNAParser import DNASuitPoint, DNAStorage, loadDNAFileAI
from direct.stdpy.file import open

class SuitPlannerBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('SuitPlannerBase')
    SuitHoodInfo = [[2100, #Silly Street
      5,
      15,
      0,
      5,
      20,
      3,
      (1,
       5,
       10,
       40,
       60,
       80),
      (20,
       20,
       20,
       20,
       20),
      (2, 3, 4),
      []],
     [2200, #Loopy Lane
      3,
      10,
      0,
      5,
      15,
      3,
      (1,
       5,
       10,
       40,
       60,
       80),
      (10,
       60,
       10,
       10,
       10),
      (1, 2, 3),
      []],
     [2300, #Punchline Place
      3,
      10,
      0,
      5,
      15,
      3,
      (1,
       5,
       10,
       40,
       60,
       80),
      (10,
       10,
       30,
       40,
       10),
      (1, 2, 3),
      []],
     [1100, #Barnacle Boulevard 
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (80,
       10,
       0,
       0,
       10),
      (2, 3, 4),
      []],
     [1200, #Seaweed Street
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       0,
       90,
       10,
       0),
      (2,
       3,
       4,
       5),
      []],
     [1300, #Lighthouse Lane
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (40,
       10,
       10,
       10,
       30),
      (3,
       4,
       5,
       6),
      []],
     [3100, #Walrus Way
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (80,
       10,
       0,
       0,
       10),
      (5, 6, 7, 8),
      []],
     [3200, #Sleet Street
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (10,
       10,
       10,
       60,
       10),
      (5, 6, 7, 8),
      []],
     [3300, #Polar Place
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (5,
       80,
       5,
       5,
       5),
      (7, 8, 9),
      []],
     [4100, #Alto Avenue
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       0,
       50,
       50,
       0),
      (2, 3, 4),
      []],
     [4200, #Baritone Boulevard
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       0,
       90,
       10,
       0),
      (4,
       5,
       6,
       7),
      []],
     [4300, #Tenor Terrance
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (15,
       10,
       0,
       0,
       75),
      (5,
       6,
       7,
       8),
      []],
     [5100, #Elm Street
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (10,
       10,
       10,
       60,
       10),
      (2, 3, 4),
      []],
     [5200, #Maple Street
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (10,
       60,
       0,
       20,
       10),
      (3,
       4,
       5,
       6),
      []],
     [5300, #Oak Street
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80,
       0),
      (5,
       5,
       5,
       80,
       5),
      (3,
       4,
       5,
       6),
      []],
     [5400, #Rose Valley
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80,
       0),
      (5,
       5,
       5,
       80,
       5),
      (4,
       5,
       6,
       7),
      []],
     [9100, #Lullaby Lane
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (20,
       20,
       20,
       20,
       20),
      (6,
       7,
       8,
       9),
      []],
     [9200, #Pajama Place
      1,
      5,
      0,
      99,
      100,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (5,
       5,
       80,
       5,
       5),
      (6,
       7,
       8,
       9),
      []],
    [10000, #Bossbot Country Club 
      10,
      20,
      0,
      0,
      0,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (100,
       0,
       0,
       0,
       0),
      (8, 9, 10),
      []],  
     [11000, #Sellbot Junkyard
      3,
      15,
      0,
      0,
      0,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       0,
       0,
       100,
       0),
      (3, 4, 5, 6),
      []],
     [11200, #Sellbot Factory Exterior
      10,
      20,
      0,
      0,
      0,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       0,
       0,
       100,
       0),
      (4, 5, 6),
      []],
     [12000, #Cashbot Trainyard
      10,
      20,
      0,
      0,
      0,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       0,
       100,
       0,
       0),
      (6, 7, 8, 9),
      []],
     [13000, #Lawbot Courtyard
      10,
      20,
      0,
      0,
      0,
      4,
      (1,
       5,
       10,
       40,
       60,
       80),
      (0,
       100,
       0,
       0,
       0),
      (7, 8, 9, 10),
      []]]
    SUIT_HOOD_INFO_ZONE = 0
    SUIT_HOOD_INFO_MIN = 1
    SUIT_HOOD_INFO_MAX = 2
    SUIT_HOOD_INFO_BMIN = 3
    SUIT_HOOD_INFO_BMAX = 4
    SUIT_HOOD_INFO_BWEIGHT = 5
    SUIT_HOOD_INFO_SMAX = 6
    SUIT_HOOD_INFO_JCHANCE = 7
    SUIT_HOOD_INFO_TRACK = 8
    SUIT_HOOD_INFO_LVL = 9
    SUIT_HOOD_INFO_HEIGHTS = 10
    TOTAL_BWEIGHT = 0
    TOTAL_BWEIGHT_PER_TRACK = [0,
     0,
     0,
     0]
    TOTAL_BWEIGHT_PER_HEIGHT = [0,
     0,
     0,
     0,
     0,
     0]
    for currHoodInfo in SuitHoodInfo:
        weight = currHoodInfo[SUIT_HOOD_INFO_BWEIGHT]
        tracks = currHoodInfo[SUIT_HOOD_INFO_TRACK]
        levels = currHoodInfo[SUIT_HOOD_INFO_LVL]
        heights = [0,
         0,
         0,
         0,
         0,
         0]
        for level in levels:
            minFloors, maxFloors = SuitBuildingGlobals.SuitBuildingInfo[level - 1][0]
            for i in range(minFloors - 1, maxFloors):
                heights[i] += 1

        currHoodInfo[SUIT_HOOD_INFO_HEIGHTS] = heights
        TOTAL_BWEIGHT += weight
        TOTAL_BWEIGHT_PER_TRACK[0] += weight * tracks[0]
        TOTAL_BWEIGHT_PER_TRACK[1] += weight * tracks[1]
        TOTAL_BWEIGHT_PER_TRACK[2] += weight * tracks[2]
        TOTAL_BWEIGHT_PER_TRACK[3] += weight * tracks[3]
        TOTAL_BWEIGHT_PER_HEIGHT[0] += weight * heights[0]
        TOTAL_BWEIGHT_PER_HEIGHT[1] += weight * heights[1]
        TOTAL_BWEIGHT_PER_HEIGHT[2] += weight * heights[2]
        TOTAL_BWEIGHT_PER_HEIGHT[3] += weight * heights[3]
        TOTAL_BWEIGHT_PER_HEIGHT[4] += weight * heights[4]
        TOTAL_BWEIGHT_PER_HEIGHT[5] += weight * heights[5]

    def __init__(self):
        self.suitWalkSpeed = ToontownGlobals.SuitWalkSpeed
        self.dnaStore = None
        self.pointIndexes = {}
        return

    def delete(self):
        del self.dnaStore
        if hasattr(self, 'dnaData'):
            del self.dnaData

    def setupDNA(self):
        if self.dnaStore:
            return None
        self.dnaStore = DNAStorage()
        dnaFileName = self.genDNAFileName()
        loadDNAFileAI(self.dnaStore, dnaFileName)
        self.initDNAInfo()

    def genDNAFileName(self):
        zoneId = ZoneUtil.getCanonicalZoneId(self.getZoneId())
        hoodId = ZoneUtil.getCanonicalHoodId(zoneId)
        hood = ToontownGlobals.dnaMap.get(hoodId)
        phase = ToontownGlobals.streetPhaseMap.get(hoodId, 4)
        if zoneId == 2000:
            phase = 4
        if hoodId == zoneId:
            zoneId = 'sz'
        if not hood:
            hood = 'toontown_central'
            zoneId = 'sz'
        return 'phase_%s/dna/%s_%s.pdna' % (phase, hood, zoneId)

    def getZoneId(self):
        return self.zoneId

    def setZoneId(self, zoneId):
        self.notify.debug('setting zone id for suit planner')
        self.zoneId = zoneId
        self.setupDNA()

    def extractGroupName(self, groupFullName):
        return groupFullName.split(':', 1)[0]

    def initDNAInfo(self):
        numGraphs = self.dnaStore.discoverContinuity()
        if numGraphs != 1:
            self.notify.info('zone %s has %s disconnected suit paths.' % (self.zoneId, numGraphs))
        self.battlePosDict = {}
        self.cellToGagBonusDict = {}
        for i in xrange(self.dnaStore.getNumDNAVisGroupsAI()):
            vg = self.dnaStore.getDNAVisGroupAI(i)
            zoneId = int(self.extractGroupName(vg.getName()))
            if vg.getNumBattleCells() == 1:
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
            elif vg.getNumBattleCells() > 1:
                self.notify.warning('multiple battle cells for zone: %d' % zoneId)
                self.battlePosDict[zoneId] = vg.getBattleCell(0).getPos()
        self.dnaStore.resetDNAGroups()
        self.dnaStore.resetDNAVisGroups()
        self.dnaStore.resetDNAVisGroupsAI()
        self.streetPointList = []
        self.frontdoorPointList = []
        self.sidedoorPointList = []
        self.cogHQDoorPointList = []
        numPoints = self.dnaStore.getNumSuitPoints()
        for i in xrange(numPoints):
            point = self.dnaStore.getSuitPointAtIndex(i)
            if point.getPointType() == DNASuitPoint.FRONT_DOOR_POINT:
                self.frontdoorPointList.append(point)
            elif point.getPointType() == DNASuitPoint.SIDE_DOOR_POINT:
                self.sidedoorPointList.append(point)
            elif (point.getPointType() == DNASuitPoint.COGHQ_IN_POINT) or (point.getPointType() == DNASuitPoint.COGHQ_OUT_POINT):
                self.cogHQDoorPointList.append(point)
            else:
                self.streetPointList.append(point)
            self.pointIndexes[point.getIndex()] = point

    def performPathTest(self):
        if not self.notify.getDebug():
            return None
        startAndEnd = self.pickPath()
        if not startAndEnd:
            return None
        startPoint = startAndEnd[0]
        endPoint = startAndEnd[1]
        path = self.dnaStore.getSuitPath(startPoint, endPoint)
        numPathPoints = path.getNumPoints()
        for i in xrange(numPathPoints - 1):
            zone = self.dnaStore.getSuitEdgeZone(path.getPointIndex(i), path.getPointIndex(i + 1))
            travelTime = self.dnaStore.getSuitEdgeTravelTime(path.getPointIndex(i), path.getPointIndex(i + 1), self.suitWalkSpeed)
            self.notify.debug('edge from point ' + `i` + ' to point ' + `(i + 1)` + ' is in zone: ' + `zone` + ' and will take ' + `travelTime` + ' seconds to walk.')

    def genPath(self, startPoint, endPoint, minPathLen, maxPathLen):
        return self.dnaStore.getSuitPath(startPoint, endPoint, minPathLen, maxPathLen)

    def getDnaStore(self):
        return self.dnaStore

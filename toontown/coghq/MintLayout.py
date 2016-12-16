from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import MintRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllCashbotInfo():
    print 'roomId: roomName'
    for roomId, roomName in MintRoomSpecs.CashbotMintRoomId2RoomName.items():
        print '%s: %s' % (roomId, roomName)

    print '\nroomId: numBattles'
    for roomId, numBattles in MintRoomSpecs.roomId2numBattles.items():
        print '%s: %s' % (roomId, numBattles)

    print '\nmintId floor roomIds'
    printMintRoomIds()
    print '\nmintId floor numRooms'
    printNumRooms()
    print '\nmintId floor numForcedBattles'
    printNumBattles()


def iterateCashbotMints(func):
    from toontown.toonbase import ToontownGlobals
    for mintId in [ToontownGlobals.CashbotMintIntA, ToontownGlobals.CashbotMintIntB, ToontownGlobals.CashbotMintIntC]:
        for floorNum in xrange(ToontownGlobals.MintNumFloors[mintId]):
            func(MintLayout(mintId, floorNum))


def printMintInfo():

    def func(ml):
        print ml

    iterateCashbotMints(func)


def printMintRoomIds():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getRoomIds()

    iterateCashbotMints(func)


def printMintRoomNames():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getRoomNames()

    iterateCashbotMints(func)


def printNumRooms():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getNumRooms()

    iterateCashbotMints(func)


def printNumBattles():

    def func(ml):
        print ml.getMintId(), ml.getFloorNum(), ml.getNumBattles()

    iterateCashbotMints(func)


BakedFloorLayouts = {12500: {0: (0,
             4,
             9,
             6,
             5,
             8,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         1: (0,
             15,
             13,
             16,
             18,
             6,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         2: (0,
             4,
             11,
             3,
             9,
             6,
             14,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         3: (0,
             17,
             3,
             4,
             16,
             14,
             15,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         4: (0,
             15,
             5,
             8,
             9,
             11,
             10,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         5: (0,
             13,
             12,
             8,
             18,
             16,
             10,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         6: (0,
             16,
             13,
             5,
             12,
             18,
             17,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         7: (0,
             10,
             12,
             18,
             3,
             13,
             16,
             8,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         8: (0,
             3,
             5,
             18,
             6,
             17,
             4,
             9,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         9: (0,
             6,
             9,
             10,
             13,
             16,
             8,
             4,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         10: (0,
              13,
              17,
              18,
              2,
              16,
              11,
              3,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         11: (0,
              3,
              17,
              6,
              4,
              14,
              8,
              9,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         12: (0,
              18,
              14,
              2,
              17,
              8,
              5,
              10,
              11,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         13: (0,
              13,
              6,
              4,
              11,
              3,
              9,
              10,
              8,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         14: (0,
              15,
              5,
              17,
              14,
              10,
              4,
              18,
              16,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         15: (0,
              16,
              10,
              11,
              2,
              17,
              3,
              14,
              5,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         16: (0,
              5,
              8,
              10,
              6,
              3,
              15,
              14,
              18,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         17: (0,
              12,
              13,
              5,
              8,
              14,
              11,
              18,
              16,
              10,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         18: (0,
              11,
              3,
              15,
              18,
              16,
              14,
              6,
              17,
              5,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         19: (0,
              10,
              16,
              11,
              3,
              5,
              12,
              13,
              18,
              14,
              24)},
 12600: {0: (0,
             8,
             17,
             6,
             14,
             2,
             5,
             9,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         1: (0,
             4,
             14,
             18,
             2,
             13,
             8,
             9,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         2: (0,
             18,
             9,
             6,
             5,
             14,
             12,
             3,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         3: (0,
             6,
             2,
             13,
             16,
             18,
             5,
             3,
             9,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         4: (0,
             15,
             4,
             9,
             8,
             6,
             13,
             5,
             11,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         5: (0,
             13,
             18,
             14,
             15,
             11,
             3,
             2,
             8,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         6: (0,
             5,
             14,
             2,
             11,
             18,
             16,
             10,
             15,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         7: (0,
             10,
             9,
             5,
             4,
             2,
             18,
             13,
             11,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         8: (0,
             11,
             4,
             12,
             6,
             17,
             13,
             18,
             3,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         9: (0,
             15,
             16,
             5,
             13,
             9,
             14,
             4,
             6,
             3,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         10: (0,
              16,
              15,
              18,
              6,
              8,
              3,
              4,
              9,
              10,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         11: (0,
              5,
              8,
              4,
              12,
              13,
              9,
              11,
              16,
              3,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         12: (0,
              13,
              16,
              18,
              4,
              12,
              3,
              6,
              5,
              17,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         13: (0,
              14,
              6,
              12,
              13,
              18,
              10,
              3,
              16,
              9,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         14: (0,
              9,
              15,
              13,
              5,
              6,
              3,
              14,
              11,
              4,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         15: (0,
              13,
              14,
              3,
              12,
              16,
              11,
              9,
              4,
              5,
              18,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         16: (0,
              3,
              6,
              17,
              18,
              5,
              10,
              9,
              4,
              13,
              15,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         17: (0,
              3,
              6,
              14,
              4,
              13,
              16,
              12,
              8,
              5,
              18,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         18: (0,
              11,
              13,
              4,
              17,
              15,
              6,
              3,
              8,
              9,
              16,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         19: (0,
              11,
              5,
              8,
              18,
              2,
              6,
              13,
              3,
              14,
              9,
              21)},
 12700: {0: (0,
             16,
             14,
             6,
             17,
             5,
             9,
             2,
             15,
             8,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         1: (0,
             3,
             2,
             12,
             14,
             8,
             13,
             6,
             10,
             18,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         2: (0,
             15,
             9,
             5,
             12,
             18,
             4,
             11,
             14,
             16,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         3: (0,
             2,
             13,
             18,
             6,
             8,
             15,
             4,
             17,
             11,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         4: (0,
             12,
             18,
             4,
             6,
             10,
             14,
             13,
             16,
             15,
             11,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         5: (0,
             10,
             2,
             9,
             13,
             4,
             8,
             17,
             15,
             14,
             11,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         6: (0,
             2,
             14,
             4,
             10,
             16,
             15,
             17,
             3,
             8,
             6,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         7: (0,
             14,
             11,
             17,
             18,
             9,
             10,
             12,
             8,
             5,
             2,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         8: (0,
             9,
             11,
             8,
             5,
             17,
             4,
             3,
             18,
             15,
             2,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         9: (0,
             2,
             9,
             18,
             11,
             16,
             10,
             15,
             3,
             8,
             6,
             random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         10: (0,
              4,
              10,
              6,
              8,
              18,
              15,
              2,
              17,
              3,
              13,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         11: (0,
              10,
              14,
              8,
              6,
              9,
              15,
              5,
              17,
              2,
              13,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         12: (0,
              16,
              5,
              12,
              10,
              6,
              9,
              11,
              3,
              15,
              13,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         13: (0,
              17,
              3,
              6,
              14,
              4,
              10,
              12,
              15,
              13,
              16,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         14: (0,
              8,
              18,
              14,
              9,
              17,
              2,
              6,
              16,
              10,
              15,
              13,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         15: (0,
              4,
              17,
              8,
              11,
              12,
              3,
              10,
              16,
              13,
              6,
              15,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         16: (0,
              6,
              3,
              10,
              4,
              17,
              2,
              13,
              11,
              5,
              15,
              16,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         17: (0,
              6,
              16,
              5,
              12,
              11,
              17,
              8,
              14,
              15,
              9,
              10,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         18: (0,
              15,
              8,
              12,
              10,
              17,
              18,
              11,
              9,
              16,
              4,
              5,
              random.choice([19, 20, 21, 22, 23, 24, 25, 26, 27])),
         19: (0,
              10,
              2,
              16,
              5,
              6,
              11,
              13,
              18,
              12,
              17,
              3,
              19)}}

class MintLayout:
    notify = DirectNotifyGlobal.directNotify.newCategory('MintLayout')

    def __init__(self, mintId, floorNum):
        self.mintId = mintId
        self.floorNum = floorNum
        self.roomIds = []
        self.hallways = []
        self.numRooms = 1 + ToontownGlobals.MintNumRooms[self.mintId][self.floorNum]
        self.numHallways = self.numRooms - 1
        if self.mintId in BakedFloorLayouts and self.floorNum in BakedFloorLayouts[self.mintId]:
            self.roomIds = list(BakedFloorLayouts[self.mintId][self.floorNum])
        else:
            self.roomIds = self._genFloorLayout()
        hallwayRng = self.getRng()
        connectorRoomNames = MintRoomSpecs.CashbotMintConnectorRooms
        for i in xrange(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))

    def _genFloorLayout(self):
        rng = self.getRng()
        startingRoomIDs = MintRoomSpecs.CashbotMintEntranceIDs
        middleRoomIDs = MintRoomSpecs.CashbotMintMiddleRoomIDs
        finalRoomIDs = MintRoomSpecs.CashbotMintFinalRoomIDs

        numBattlesLeft = ToontownGlobals.MintNumBattles[self.mintId]

        finalRoomId = rng.choice(finalRoomIDs)
        numBattlesLeft -= MintRoomSpecs.getNumBattles(finalRoomId)

        middleRoomIds = []
        middleRoomsLeft = self.numRooms - 2

        numBattles2middleRoomIds = invertDictLossless(MintRoomSpecs.middleRoomId2numBattles)

        allBattleRooms = []
        for num, roomIds in numBattles2middleRoomIds.items():
            if num > 0:
                allBattleRooms.extend(roomIds)
        while 1:
            allBattleRoomIds = list(allBattleRooms)
            rng.shuffle(allBattleRoomIds)
            battleRoomIds = self._chooseBattleRooms(numBattlesLeft,
                                                    allBattleRoomIds)
            if battleRoomIds is not None:
                break

            MintLayout.notify.info('could not find a valid set of battle rooms, trying again')

        middleRoomIds.extend(battleRoomIds)
        middleRoomsLeft -= len(battleRoomIds)

        if middleRoomsLeft > 0:
            actionRoomIds = numBattles2middleRoomIds[0]
            for i in xrange(middleRoomsLeft):
                roomId = rng.choice(actionRoomIds)
                actionRoomIds.remove(roomId)
                middleRoomIds.append(roomId)

        roomIds = []

        roomIds.append(rng.choice(startingRoomIDs))

        rng.shuffle(middleRoomIds)
        roomIds.extend(middleRoomIds)

        roomIds.append(finalRoomId)

        return roomIds

    def getNumRooms(self):
        return len(self.roomIds)

    def getRoomId(self, n):
        return self.roomIds[n]

    def getRoomIds(self):
        return self.roomIds[:]

    def getRoomNames(self):
        names = []
        for roomId in self.roomIds:
            names.append(MintRoomSpecs.CashbotMintRoomId2RoomName[roomId])

        return names

    def getNumHallways(self):
        return len(self.hallways)

    def getHallwayModel(self, n):
        return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += MintRoomSpecs.roomId2numBattles[roomId]

        return numBattles

    def getMintId(self):
        return self.mintId

    def getFloorNum(self):
        return self.floorNum

    def getRng(self):
        return random.Random(self.mintId * self.floorNum)

    def _chooseBattleRooms(self, numBattlesLeft, allBattleRoomIds, baseIndex = 0, chosenBattleRooms = None):
        if chosenBattleRooms is None:
            chosenBattleRooms = []
        while baseIndex < len(allBattleRoomIds):
            nextRoomId = allBattleRoomIds[baseIndex]
            baseIndex += 1
            newNumBattlesLeft = numBattlesLeft - MintRoomSpecs.middleRoomId2numBattles[nextRoomId]
            if newNumBattlesLeft < 0:
                continue
            elif newNumBattlesLeft == 0:
                chosenBattleRooms.append(nextRoomId)
                return chosenBattleRooms
            chosenBattleRooms.append(nextRoomId)
            result = self._chooseBattleRooms(newNumBattlesLeft, allBattleRoomIds, baseIndex, chosenBattleRooms)
            if result is not None:
                return result
            else:
                del chosenBattleRooms[-1:]
        else:
            return

        return

    def __str__(self):
        return 'MintLayout: id=%s, floor=%s, numRooms=%s, numBattles=%s' % (self.mintId,
         self.floorNum,
         self.getNumRooms(),
         self.getNumBattles())

    def __repr__(self):
        return str(self)

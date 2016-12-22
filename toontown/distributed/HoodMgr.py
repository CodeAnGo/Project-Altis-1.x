from panda3d.core import *
from panda3d.direct import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.launcher import DownloadForceAcknowledge
import string
import random
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil

class HoodMgr(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('HoodMgr')
    ToontownCentralInitialDropPoints = (
        [65.860, 142.571, 2.526, 790.259, 0, 0],
        [57.473, 125.268, 2.526, 756.419, 0, 0],
        [45.851, 119.799, 2.526, 752.187, 0, 0],
        [32.971, 116.496, 2.526, 735.172, 0, 0],
        [22.488, 116.245, 2.526, 719.057, 0, 0],
        [35.136, 132.832, 2.526, 746.570, 0, 0]
    )
    ToontownCentralHQDropPoints = (
        [12.915, -24.938, 4.025, 256.087, 0, 0],
        [19.111, -16.684, 4.025, 230.295, 0, 0],
        [44.362, -5.827, 4.025, 183.660, 0, 0],
        [75.218, -62.574, 4.025, 69.765, 0, 0],
        [64.095, -98.374, 2.525, 8.584, 0, 0]
    )
    ToontownCentralTunnelDropPoints = (
        [43.086, -134.343, 2.525, 153.905, 0, 0],
        [30.529, -132.724, 2.525, 174.786, 0, 0],
        [-112.550, -16.980, -0.539, 55.739, 0, 0],
        [-113.516, 5.141, -0.332, 86.807, 0, 0],
        [-127.868, 19.685, 0.025, 124.113, 0, 0],
        [51.805, 1.551, 4.025, -94.668, 0, 0]
    )
    dropPoints = {
        ToontownGlobals.DonaldsDock: (
            [-28.0, -2.5, 5.8, 120.0, 0.0, 0.0],
            [-22, 13, 5.8, 155.6, 0.0, 0.0],
            [67, 47, 5.7, 134.7, 0.0, 0.0],
            [62, 19, 5.7, 97.0, 0.0, 0.0],
            [66, -27, 5.7, 80.5, 0.0, 0.0],
            [-114, -7, 5.7, -97.0, -0.0, 0.0],
            [-108, 36, 5.7, -153.8, -0.0, 0.0],
            [-116, -46, 5.7, -70.1, -0.0, 0.0],
            [-63, -79, 5.7, -41.2, -0.0, 0.0],
            [-2, -79, 5.7, 57.4, -0.0, 0.0],
            [-38, -78, 5.7, 9.1, -0.0, 0.0]
        ),
        ToontownGlobals.ToontownCentral: (
            [29.852, -24.213, 4.025, -144.876, 0, 0],
            [47.767, 8.561, 4.025, 84.711, 0, 0],
            [15.510, 0.600, 4.025, 95.333, 0, 0],
            [47.125, 131.393, 2.525, 45.557, 0, 0],
            [-36.086, 72.705, 0.025, 89.292, 0, 0],
            [-121.765, 3.269, 0.025, 253.862, 0, 0],
            [-93.421, -5.947, -0.998, 259.667, 0, 0],
            [-62.664, -10.416, 1.227, 259.667, 0, 0],
            [-67.422, -89.830, 0.525, 2.817, 0, 0],
            [24.879, -136.027, 2.525, -119.153, 0, 0],
            [105.006, -128.606, 4.051, 39.054, 0, 0],
            [85.233, -59.504, 4.025, 48.868, 0, 0],
            [63.280, -34.097, 4.025, 47.924, 0, 0],
            [80.324, 23.511, 4.025, 132.485, 0, 0],
            [103.581, 39.608, 4.025, 464.251, 0, 0],
            [10.075, 75.395, 2.525, 499.846, 0, 0]
        ),
        ToontownGlobals.TheBrrrgh: (
            [35, -32, 6.2, 138, 0.0, 0.0],
            [26, -105, 6.2, -339, 0.0, 0.0],
            [-29, -139, 6.2, -385, 0.0, 0.0],
            [-79, -123, 6.2, -369, 0.0, 0.0],
            [-114, -86, 3, -54, 0.0, 0.0],
            [-136, 9, 6.2, -125, 0.0, 0.0],
            [-75, 92, 6.2, -187, 0.0, 0.0],
            [-7, 75, 6.2, -187, 0.0, 0.0],
            [-106, -42, 8.6, -111, 0.0, 0.0],
            [-116, -44, 8.3, -20, 0.0, 0.0]
        ),
        ToontownGlobals.MinniesMelodyland: (
            [86, 44, -13.5, 121.1, 0.0, 0.0],
            [88, -8, -13.5, 91, 0, 0],
            [92, -76, -13.5, 62.5, 0.0, 0.0],
            [53, -112, 6.5, 65.8, 0.0, 0.0],
            [-69, -71, 6.5, -67.2, 0.0, 0.0],
            [-75, 21, 6.5, -100.9, 0.0, 0.0],
            [-21, 72, 6.5, -129.5, 0.0, 0.0],
            [56, 72, 6.5, 138.2, 0.0, 0.0],
            [-41, 47, 6.5, -98.9, 0.0, 0.0]
        ),
        ToontownGlobals.DaisyGardens: (
            [-0.998, 9.147, 0.025, -5.663, 0, 0],
            [47.207, 51.395, 0.025, -77.411, 0.0, 0.0],
            [113.105, 120.739, 0.025, -33.388, 0.0, 0.0],
            [119.150, 187.219, 0.025, 28.910, 0.0, 0.0],
            [93.115, 240.878, 14.016, -38.148, 0.0, 0.0],
            [71.400, 288.892, 14.025, 44.651, 0.0, 0.0],
            [39.726, 329.260, 13.925, 125.246, 0.0, 0.0],
            [-24.758, 307.053, 14.025, 119.294, 0.0, 0.0],
            [-74.713, 273.668, 14.026, 133.668, 0.0, 0.0],
            [-81.067, 229.671, 14.025, 181.866, 0.0, 0.0],
            [-117.230, 185.184, 0.025, 163.659, 0.0, 0.0]
        ),
        ToontownGlobals.DonaldsDreamland: (
            [77, 91, 0.0, 124.4, 0.0, 0.0],
            [29, 92, 0.0, -154.5, 0.0, 0.0],
            [-28, 49, -16.4, -142.0, 0.0, 0.0],
            [21, 40, -16.0, -65.1, 0.0, 0.0],
            [48, 27, -15.4, -161.0, 0.0, 0.0],
            [-2, -22, -15.2, -132.1, 0.0, 0.0],
            [-92, -88, 0.0, -116.3, 0.0, 0.0],
            [-56, -93, 0.0, -21.5, 0.0, 0.0],
            [20, -88, 0.0, -123.4, 0.0, 0.0],
            [76, -90, 0.0, 11.0, 0.0, 0.0]
        ),
        ToontownGlobals.FunnyFarm: ( # TODO: Drop points!
            [0, 0, 0, 0, 0, 0],
        ),
        ToontownGlobals.GoofySpeedway: (
            [-0.7, 62, 0.08, 182, 0, 0],
            [-1, -30, 0.06, 183, 0, 0],
            [-13, -120, 0, 307, 0, 0],
            [16.4, -120, 0, 65, 0, 0],
            [-0.5, -90, 0, 182, 0, 0],
            [-30, -25, -0.373, 326, 0, 0],
            [29, -17, -0.373, 32, 0, 0]
        ),
        ToontownGlobals.GolfZone: (
            [-49.6, 102, 0, 162, 0, 0],
            [-22.8, 36.6, 0, 157.5, 0, 0],
            [40, 51, 0, 185, 0, 0],
            [48.3, 122.2, 0, 192, 0, 0],
            [106.3, 69.2, 0, 133, 0, 0],
            [-81.5, 47.2, 0, 183, 0, 0],
            [-80.5, -84.2, 0, 284, 0, 0],
            [73, -111, 0, 354, 0, 0]
        ),
        ToontownGlobals.OutdoorZone: (
            [-165.8, 108, 0.025, 252, 0, 0],
            [21, 130, 0.16, 170, 0, 0],
            [93, 78.5, 0.23, 112, 0, 0],
            [79, -1.6, 0.75, 163, 0, 0],
            [10, 33, 5.32, 130.379, 0, 0],
            [-200, -42, 0.025, 317.543, 0, 0],
            [-21, -65, 0.335, -18, 0, 0],
            [23, 68.5, 4.51, -22.808, 0, 0]
        ),
        ToontownGlobals.Tutorial: (
            [130.9, -8.6, -1.3, 105.5, 0, 0],
        ),
        ToontownGlobals.SellbotHQ: (
            [56.910, -173.576, -7.037, 15.061, 0, 0],
            [-53.105, -197.259, -4.812, 25.870, 0, 0],
            [-103, -118, 0.367, 622.422, 0, 0],
            [-5.361, -228.596, -10.817, -118.934, 0, 0],
            [-8.2536, -175.53, -19.5944, -313.592, 0, 0],
            [66.7811, -96.8434, 0.286679, -567.363, 0, 0]
        ),
        ToontownGlobals.CashbotHQ: (
            [102, -437, -23.439, 360, 0, 0],
            [124, -437, -23.439, 360, 0, 0],
            [110, -446, -23.439, 360, 0, 0],
            [132, -446, -23.439, 360, 0, 0]
        ),
        ToontownGlobals.LawbotHQ: (
            [77.5, 129.13, -68.4, -166.6, 0, 0],
            [-57.7, 80.75, -68.4, -139.2, 0, 0],
            [203.3, 46.36, -68.4, -213.37, 0, 0],
            [88.2, -336.52, -68.4, -720.4, 0, 0],
            [232.77, -305.33, -68.4, -651, 0, 0],
            [-20.16, -345.76, -68.4, -777.98, 0, 0]
        ),
        ToontownGlobals.BossbotHQ: ( # TODO: Drop points!
            [0, 0, 0, 0, 0, 0],
        )
    }
    hoodName2Id = {
        'dd': ToontownGlobals.DonaldsDock,
        'tt': ToontownGlobals.ToontownCentral,
        'br': ToontownGlobals.TheBrrrgh,
        'mm': ToontownGlobals.MinniesMelodyland,
        'dg': ToontownGlobals.DaisyGardens,
        'oz': ToontownGlobals.OutdoorZone,
        'ff': ToontownGlobals.FunnyFarm,
        'gs': ToontownGlobals.GoofySpeedway,
        'dl': ToontownGlobals.DonaldsDreamland,
        'bosshq': ToontownGlobals.BossbotHQ,
        'sellhq': ToontownGlobals.SellbotHQ,
        'cashhq': ToontownGlobals.CashbotHQ,
        'lawhq': ToontownGlobals.LawbotHQ,
        'gz': ToontownGlobals.GolfZone,
        'boardhq': ToontownGlobals.BoardbotHQ
    }
    hoodId2Name = {
        ToontownGlobals.DonaldsDock: 'dd',
        ToontownGlobals.ToontownCentral: 'tt',
        ToontownGlobals.Tutorial: 'tt',
        ToontownGlobals.TheBrrrgh: 'br',
        ToontownGlobals.MinniesMelodyland: 'mm',
        ToontownGlobals.DaisyGardens: 'dg',
        ToontownGlobals.OutdoorZone: 'oz',
        ToontownGlobals.FunnyFarm: 'ff',
        ToontownGlobals.GoofySpeedway: 'gs',
        ToontownGlobals.DonaldsDreamland: 'dl',
        ToontownGlobals.BossbotHQ: 'bosshq',
        ToontownGlobals.SellbotHQ: 'sellhq',
        ToontownGlobals.CashbotHQ: 'cashhq',
        ToontownGlobals.LawbotHQ: 'lawhq',
        ToontownGlobals.GolfZone: 'gz',
        ToontownGlobals.BoardbotHQ: 'boardhq'
    }
    DefaultDropPoint = [0] * 6
    dbgDropMode = 0
    currentDropPoint = 0

    def __init__(self, cr):
        self.cr = cr

    def getDropPoint(self, dropPointList):
        if self.dbgDropMode == 0:
            return random.choice(dropPointList)
        else:
            droppnt = self.currentDropPoint % len(dropPointList)
            self.currentDropPoint = (self.currentDropPoint + 1) % len(dropPointList)
            return dropPointList[droppnt]

    def getAvailableZones(self):
        if base.launcher == None:
            return self.getZonesInPhase(4) + self.getZonesInPhase(6) + self.getZonesInPhase(8) + self.getZonesInPhase(9) + self.getZonesInPhase(10) + self.getZonesInPhase(11) + self.getZonesInPhase(12) + self.getZonesInPhase(13)
        else:
            zones = []
            for phase in set(ToontownGlobals.phaseMap.values()):
                if base.launcher.getPhaseComplete(phase):
                    zones = zones + self.getZonesInPhase(phase)

            return zones
        return

    def getZonesInPhase(self, phase):
        p = []
        for i in ToontownGlobals.phaseMap.items():
            if i[1] == phase:
                p.append(i[0])

        return p

    def getPhaseFromHood(self, hoodId):
        hoodId = ZoneUtil.getCanonicalHoodId(hoodId)
        return ToontownGlobals.phaseMap[hoodId]

    def getPlaygroundCenterFromId(self, hoodId):
        dropPointList = self.dropPoints.get(hoodId, None)
        if dropPointList:
            return self.getDropPoint(dropPointList)
        else:
            self.notify.warning('getPlaygroundCenterFromId: No such hood name as: ' + str(hoodId))
            return self.DefaultDropPoint
        return

    def getIdFromName(self, hoodName):
        id = self.hoodName2Id.get(hoodName)
        if id:
            return id
        else:
            self.notify.error('No such hood name as: %s' % hoodName)
            return None
        return None

    def getNameFromId(self, hoodId):
        name = self.hoodId2Name.get(hoodId)
        if name:
            return name
        else:
            self.notify.error('No such hood id as: %s' % hoodId)
            return None
        return None

    def getFullnameFromId(self, hoodId):
        hoodId = ZoneUtil.getCanonicalZoneId(hoodId)
        return ToontownGlobals.hoodNameMap[hoodId][-1]

    def addLinkTunnelHooks(self, hoodPart, nodeList, currentZoneId):
        tunnelOriginList = []
        for i in nodeList:
            linkTunnelNPC = i.findAllMatches('**/linktunnel*')
            for p in range(linkTunnelNPC.getNumPaths()):
                linkTunnel = linkTunnelNPC.getPath(p)
                name = linkTunnel.getName()
                nameParts = name.split('_')
                hoodStr = nameParts[1]
                zoneStr = nameParts[2]
                hoodId = self.getIdFromName(hoodStr)
                zoneId = int(zoneStr)
                hoodId = ZoneUtil.getTrueZoneId(hoodId, currentZoneId)
                zoneId = ZoneUtil.getTrueZoneId(zoneId, currentZoneId)
                linkSphere = linkTunnel.find('**/tunnel_trigger')
                if linkSphere.isEmpty():
                    linkSphere = linkTunnel.find('**/tunnel_sphere')
                if not linkSphere.isEmpty():
                    cnode = linkSphere.node()
                    cnode.setName('tunnel_trigger_' + hoodStr + '_' + zoneStr)
                    cnode.setCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.GhostBitmask)
                else:
                    linkSphere = linkTunnel.find('**/tunnel_trigger_' + hoodStr + '_' + zoneStr)
                    if linkSphere.isEmpty():
                        self.notify.error('tunnel_trigger not found')
                tunnelOrigin = linkTunnel.find('**/tunnel_origin')
                if tunnelOrigin.isEmpty():
                    self.notify.error('tunnel_origin not found')
                tunnelOriginPlaceHolder = render.attachNewNode('toph_' + hoodStr + '_' + zoneStr)
                tunnelOriginList.append(tunnelOriginPlaceHolder)
                tunnelOriginPlaceHolder.setPos(tunnelOrigin.getPos(render))
                tunnelOriginPlaceHolder.setHpr(tunnelOrigin.getHpr(render))
                hood = base.localAvatar.cr.playGame.hood
                if ZoneUtil.tutorialDict:
                    how = 'teleportIn'
                    tutorialFlag = 1
                else:
                    how = 'tunnelIn'
                    tutorialFlag = 0
                hoodPart.accept('enter' + linkSphere.getName(), hoodPart.handleEnterTunnel, [{'loader': ZoneUtil.getLoaderName(zoneId),
                  'where': ZoneUtil.getToonWhereName(zoneId),
                  'how': how,
                  'hoodId': hoodId,
                  'zoneId': zoneId,
                  'shardId': None,
                  'tunnelOrigin': tunnelOriginPlaceHolder,
                  'tutorial': tutorialFlag}])

        return tunnelOriginList

    def extractGroupName(self, groupFullName):
        return groupFullName.split(':', 1)[0]

    def makeLinkTunnelName(self, hoodId, currentZone):
        return '**/toph_' + self.getNameFromId(hoodId) + '_' + str(currentZone)

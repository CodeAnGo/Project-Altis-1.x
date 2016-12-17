from panda3d.core import *
from panda3d.direct import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedSellbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle
import random
from toontown.hood import ZoneUtil

class SellbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQBossBattle')

    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        self.teleportInPosHpr = (0, 95, 18, 180, 0, 0)

    def load(self):
        self.fog = Fog('VPFog')
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)
        self.fog = None

    def enter(self, requestStatus):
        self.setFog()
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus, DistributedSellbotBoss.OneBossCog)
        self.__setupHighSky()

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)
        self.__cleanupHighSky()

    def __setupHighSky(self):
        self.loader.hood.startSky()
        sky = self.loader.hood.sky
        sky.setH(150)
        sky.setZ(-100)

    def __cleanupHighSky(self):
        self.loader.hood.stopSky()
        sky = self.loader.hood.sky
        sky.setH(0)
        sky.setZ(0)

    def setFog(self):
        if base.wantFog:
            self.fog.setColor(0.1, 0.1, 0.1)
            self.fog.setExpDensity(0.004)
            render.clearFog()
            render.setFog(self.fog)

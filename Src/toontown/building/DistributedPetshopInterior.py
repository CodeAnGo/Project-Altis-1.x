from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
import random
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.actor import Actor
import ToonInteriorColors
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase

class DistributedPetshopInterior(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dnaStore = cr.playGame.dnaStore

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount - 1)
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def chooseDoor(self):
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        return door

    def setup(self):
        self.dnaStore = base.cr.playGame.dnaStore
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)
        self.interior = loader.loadModel('phase_4/models/modules/PetShopInterior')
        self.interior.reparentTo(render)
        self.fish = Actor.Actor('phase_4/models/props/interiorfish-zero', {'swim': 'phase_4/models/props/interiorfish-swim'})
        self.fish.reparentTo(self.interior)
        self.fish.setColorScale(0.8, 0.9, 1, 0.8)
        self.fish.setScale(0.8)
        self.fish.setPos(0, 6, -4)
        self.fish.setPlayRate(0.7, 'swim')
        self.fish.loop('swim')

        self.white = Actor.Actor('phase_4/models/char/nurseShark-zero', {'swim': 'phase_4/models/char/nurseShark-swim'})
        self.white.reparentTo(render)
        self.white.setScale(3.60)
        self.white.setPos(0, 30, 3)
        self.white.loop('swim')

        self.doctor = loader.loadSfx('phase_4/audio/sfx/Nurse_Shark.ogg')
        self.doctor.play()

        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        door = self.chooseDoor()
        doorOrigin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(doorOrigin)
        doorOrigin.setScale(0.8, 0.8, 0.8)
        doorOrigin.setPos(doorOrigin, 0, -0.25, 0)
        doorColor = self.randomGenerator.choice(self.colors['TI_door'])
        DNADoor.setupDoor(doorNP, self.interior, doorOrigin, self.dnaStore, str(self.block), doorColor)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)
        del self.colors
        del self.dnaStore
        del self.randomGenerator
        self.interior.flattenMedium()
        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()

    def disable(self):
        self.fish.stop()
        self.fish.cleanup()
        del self.fish
        self.interior.removeNode()
        del self.interior
        
        self.white.stop()
        self.white.removeNode()
        del self.white

        self.doctor.stop()

        DistributedObject.DistributedObject.disable(self)

from panda3d.core import *
from panda3d.direct import *
import ToonHood
from toontown.town import DDTownLoader
from toontown.safezone import DDSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from otp.ai.MagicWordGlobal import *

class DDHood(ToonHood.ToonHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = DonaldsDock
        self.townLoaderClass = DDTownLoader.DDTownLoader
        self.safeZoneLoaderClass = DDSafeZoneLoader.DDSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_DD.pdna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_6/dna/winter_storage_DD.pdna'],
         WACKY_WINTER_DECORATIONS: ['phase_6/dna/winter_storage_DD.pdna'],
         HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_DD.pdna'],
         SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_DD.pdna']}
        self.skyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (0.8, 0.6, 0.5, 1.0)
        self.whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)
        self.underwaterFogColor = Vec4(0.0, 0.0, 0.6, 1.0)
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('DDHood').addChild(self.fsm)
        self.fog = Fog('DDFog')

    def unload(self):
        self.parentFSM.getStateNamed('DDHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        self.fog = None

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)

    def setUnderwaterFog(self):
        if base.wantFog:
            self.fog.setColor(self.underwaterFogColor)
            self.fog.setLinearRange(0.1, 100.0)
            render.setFog(self.fog)
            if not self.sky:
                return

            self.sky.setFog(self.fog)

    def setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(self.whiteFogColor)
            self.fog.setLinearRange(0.0, 400.0)
            render.clearFog()
            render.setFog(self.fog)
            if not self.sky:
                return
            
            self.sky.clearFog()
            self.sky.setFog(self.fog)

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            self.sky.clearFog()

@magicWord(category=CATEGORY_OVERRIDE)
def spooky():
    """
    Activates the 'spooky' effect on the current area.
    """
    hood = base.cr.playGame.hood
    if not hasattr(hood, 'startSpookySky'):
        return "Couldn't find spooky sky."
    if hasattr(hood, 'magicWordSpookyEffect'):
        return 'The spooky effect is already active!'
    hood.magicWordSpookyEffect = True
    hood.startSpookySky()
    fadeOut = base.cr.playGame.getPlace().loader.geom.colorScaleInterval(
        1.5, Vec4(0.55, 0.55, 0.65, 1), startColorScale=Vec4(1, 1, 1, 1),
        blendType='easeInOut')
    fadeOut.start()
    spookySfx = base.loadSfx('phase_4/audio/sfx/spooky.ogg')
    spookySfx.play()
    return 'Activating the spooky effect...'

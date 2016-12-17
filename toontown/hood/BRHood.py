from panda3d.core import *
from panda3d.direct import *
import ToonHood
from toontown.town import BRTownLoader
from toontown.safezone import BRSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from otp.ai.MagicWordGlobal import *

class BRHood(ToonHood.ToonHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = TheBrrrgh
        self.townLoaderClass = BRTownLoader.BRTownLoader
        self.safeZoneLoaderClass = BRSafeZoneLoader.BRSafeZoneLoader
        self.storageDNAFile = 'phase_8/dna/storage_BR.pdna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_8/dna/winter_storage_BR.pdna'],
         WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_BR.pdna'],
         HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_BR.pdna'],
         SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_BR.pdna']}
        self.skyFile = 'phase_3.5/models/props/BR_sky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (0.3, 0.6, 1.0, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('BRHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('BRHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)

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

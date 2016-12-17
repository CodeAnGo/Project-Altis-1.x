from panda3d.core import *
from panda3d.direct import *
import SafeZoneLoader
import MMPlayground
from toontown.toonbase import ToontownGlobals

class MMSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = MMPlayground.MMPlayground
        self.musicFile = 'phase_6/audio/bgm/MM_nbrhood.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/MM_SZ_activity.ogg'
        self.dnaFile = 'phase_6/dna/minnies_melody_land_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_MM_sz.pdna'

    def load(self):
        print 'loading MM safezone'
        SafeZoneLoader.SafeZoneLoader.load(self)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

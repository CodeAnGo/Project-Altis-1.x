from panda3d.core import Point3, VBase3, Vec3, Vec4
from toontown.betaevent.DistributedEvent import DistributedEventfrom toontown.betaevent import CogTV
from toontown.hood import ZoneUtil
from direct.fsm import ClassicFSM, State
from direct.interval.IntervalGlobal import * 
from toontown.toon import Toon, ToonDNA
from direct.actor.Actor import Actor
from otp.avatar import Avatar
from otp.nametag.NametagConstants import *
from toontown.nametag.NametagGroup import *
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toon import NPCToons
from toontown.betaevent import BeteEventGlobals as BEGlobals
from toontown.battle import BattleParticles

class DistributedBetaEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedBetaEvent')
    
    def __init__(self, cr):
        DistributedEvent.__init__(self, cr)
        self.cr = cr
        self.spark = loader.loadSfx('phase_11/audio/sfx/LB_sparks_1.ogg') # i think this could be used somewhere
        
        # The toon version of Looney Labs - Before it gets taken over
        self.toonLabs = None
        
        # The cog version of Looney Labs - After it gets taken over
        self.cogLabs = None

        # Create flippy
        self.flippy = Toon.Toon()
        self.flippy.setName('Flippy')
        self.flippy.setPickable(0)
        self.flippy.setPlayerType(NametagGlobals.CCNonPlayer)
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties('dss', 'ms', 'm', 'm', 17, 0, 17, 17, 3, 3, 3, 3, 7, 2)
        self.flippy.setDNA(dna)
        self.flippy.animFSM.request('neutral')
        self.flippy.reparentTo(render)
        self.flippy.setPosHpr(68, -10, 4.024, 75, 0, 0)
        self.flippy.blinkEyes()
        self.flippy.head = self.flippy.find('**/__Actor_head')
        self.flippy.initializeBodyCollisions('toon')

    def announceGenerate(self):
        DistributedEvent.announceGenerate(self)
        
    def start(self):
        pass

    def delete(self):
        DistributedEvent.delete(self)
        self.flippy.delete()
            
    def enterPreEvent(self, timestamp):
        # If for some reason the cog lab is loaded, unload
        if self.cogLabs:
            self.cogLabs.destroy()
            self.cogLabs = None
        
        # Load the toon lab if its not already loaded incase a new player enters
        if not self.toonLabs:
            self.loadToonLab()
        
    def exitPreEvent(self, timestamp):
        pass
    
    def enterAnnouncement(self, timestamp):
        """
        Announcing looney labs's renovation
        """
        # If for some reason the cog lab is loaded, unload
        if self.cogLabs:
            self.cogLabs.destroy()
            self.cogLabs = None
        
        # Load the toon lab if its not already loaded incase a new player enters
        if not self.toonLabs:
            self.loadToonLab()
        
    def exitAnnouncement(self, timestamp):
        pass

    def enterCogTv(self, timestamp):
        # Todo: Make the models and make the tv code.
        '''
        self.cogTvModel = None
        self.cogTvModel.setPosHpr(0, 0, 0, 0, 0, 0) 
        self.cogTv = CogTV.CogTV
        self.cogTv.setScreen("Introduction")
        '''
        pass
    
    def exitCogTv(self, timestamp):
        pass
    
    def enterCogTakeover(self, timestamp):
        """
        Cogs take over looney labs
        - Fade screen to black
        - Delete looney labs model and replace it with the Cog version of looney labs
        - AI will create suit planner
        - Screen unfades
        """
        # Unload the toon labs if its loaded
        if self.toonLabs:
            self.toonLabs.destroy()
            self.toonLabs = None
        
        # Load the cog lab if its not already loaded incase a new player enters
        if not self.cogLabs:
            self.loadCogLab()
    
    def exitCogTakeover(self, timestamp):
        pass
    
    def toonTalk(self, phrase, toon):
        toon.setChatAbsolute(phrase, CFSpeech|CFTimeout)
        
    def loadToonLab(self):
        # After the model is loaded, spawn it in
        def spawnToonLab(self, *args):
            self.toonLabs = args[0]
            self.toonLabs.reparentTo(render)
        
        # Asynchronously load the model to not lag the game
        #loader.loadModel('phase_14/models/looneylabs/looney_labs_toon', callback = spawnToonLab) # TODO: Models
        pass
        
    def loadCogLab(self):
        # After the model is loaded, spawn it in
        def spawnCogLab(self, *args):
            self.cogLabs = args[0]
            self.cogLabs.reparentTo(render)
        
        # Asynchronously load the model to not lag the game
        #loader.loadModel('phase_14/models/looneylabs/looney_labs_cog', callback = spawnCogLab) # TODO: Models
        pass
        
        
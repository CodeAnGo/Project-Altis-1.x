from panda3d.core import Point3, VBase3, Vec3, Vec4
from toontown.betaevent.DistributedEvent import DistributedEventfrom toontown.betaevent import CogTV
from toontown.hood import ZoneUtil
from direct.fsm import ClassicFSM, State
from direct.interval.IntervalGlobal import * 
from toontown.toon import Toon, ToonDNA
from direct.actor.Actor import Actor
from otp.avatar import Avatar
from otp.nametag.NametagConstants import *
from otp.nametag.NametagGroup import *
from otp.nametag.NametagGlobals import *
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toon import NPCToons
from toontown.betaevent import BetaEventGlobals as BEGlobals
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

        # Create surlee
        self.surlee = Toon.Toon()
        self.surlee.setName('Doctor Surlee')
        self.surlee.setPickable(0)
        self.surlee.setPlayerType(CCNonPlayer)
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties('pls', 'ls', 'l', 'm', 9, 0, 9, 9, 98, 27, 86, 27, 38, 27)
        self.surlee.setDNA(dna)
        self.surlee.animFSM.request('neutral')
        self.surlee.reparentTo(render)
        self.surlee.setPosHpr(4, -3, -68.367, 0, 0, 0)
        self.surlee.blinkEyes()
        self.surlee.head = self.surlee.find('**/__Actor_head')
        self.surlee.initializeBodyCollisions('toon')
        
        self.gate = loader.loadModel('phase_14/models/looneylabs/tunnel_gate')
        self.gate.reparentTo(render)
        self.gate.setPos(3, -21, -68)
        self.gateLeft = self.gate.find('**/L_gate')
        
        self.headHoncho1 = DistributedSuitBase.DistributedSuitBase(self.cr)
        headHoncho1suitDNA = SuitDNA.SuitDNA()
        headHoncho1suitDNA.newSuit('hho')
        self.headHoncho1.setDNA(headHoncho1suitDNA)
        self.headHoncho1.setDisplayName('???')
        self.headHoncho1.setPickable(0)
        self.headHoncho1.setPosHpr(0, 0, 0, 0, 0, 0)
        self.headHoncho1.reparentTo(render)
        self.headHoncho1.hide()
        #self.headHoncho1.initializeBodyCollisions('toon')
        
        base.musicManager.stopAllSounds()
        self.toonMusic = loader.loadMusic('phase_14/audio/bgm/ttiHalcyon.mp3') # Placeholder
        base.playMusic(self.toonMusic, looping = 1)

    def announceGenerate(self):
        DistributedEvent.announceGenerate(self)
        
    def start(self):
        pass

    def delete(self):
        DistributedEvent.delete(self)
        self.surlee.delete()
            
    def enterPreEvent(self, timestamp):
        # If for some reason the cog lab is loaded, unload
        if self.cogLabs:
            self.cogLabs.removeNode()
            self.cogLabs = None
        
        # Load the toon lab if its not already loaded incase a new player enters
        if not self.toonLabs:
            self.loadToonLab()
        
        self.gateLeft.hprInterval(1, VBase3(90, 0, 0)).start()
        
    def exitPreEvent(self):
        pass
    
    def enterAnnouncement(self, timestamp):
        """
        Announcing looney labs's renovation
        """
        # If for some reason the cog lab is loaded, unload
        if self.cogLabs:
            self.cogLabs.removeNode()
            self.cogLabs = None
        
        # Load the toon lab if its not already loaded incase a new player enters
        if not self.toonLabs:
            self.loadToonLab()
            
        self.gateLeft.hprInterval(1, VBase3(0, 0, 0)).start()
        
        Sequence(
                    Func(self.surlee.setChatAbsolute, 'Greetings Toons of the world!', CFSpeech|CFTimeout),
                    Wait(3),
                    Func(self.surlee.setChatAbsolute, 'Today, we are proud to announce...', CFSpeech|CFTimeout),
                    Wait(3),
                    Func(self.surlee.setChatAbsolute, 'The renovation and public opening of...', CFSpeech|CFTimeout),
                    Wait(4),
                    Func(self.surlee.setChatAbsolute, 'Looney Labs!', CFSpeech|CFTimeout),
                    Wait(2),
                    self.gateLeft.hprInterval(1, VBase3(90, 0, 0))
                 ).start()
        
    def exitAnnouncement(self):
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
    
    def exitCogTv(self):
        pass
    
    def enterCogInvade(self, timestamp):
        self.headHoncho1.show()
        self.headHoncho1.beginSupaFlyMove(Vec3(12, -4, -68.367), True, "firstCogInvadeFlyIn", walkAfterLanding=False).start()
        Sequence(
                    Wait(6),
                    Func(self.headHoncho1.loop, 'walk'),
                    self.headHoncho1.hprInterval(2, VBase3(90, 0, 0)),
                    Wait(2),
                    Func(self.headHoncho1.loop, 'neutral'),
                    Wait(1),
                    Func(self.headHoncho1.setChatAbsolute, 'Hello Toon...', CFSpeech|CFTimeout),
                    Wait(4),
                    Func(self.headHoncho1.setChatAbsolute, "I'd hate to crash the party...", CFSpeech|CFTimeout),
                    Wait(4),
                    Func(self.headHoncho1.setChatAbsolute, "Actually... I'd love to!", CFSpeech|CFTimeout)
                 ).start()
        
    def exitCogInvade(self):
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
            self.toonLabs.removeNode()
            self.toonLabs = None
        
        # Load the cog lab if its not already loaded incase a new player enters
        if not self.cogLabs:
            self.loadCogLab()
    
    def exitCogTakeover(self):
        pass
    
    def toonTalk(self, phrase, toon):
        toon.setChatAbsolute(phrase, CFSpeech|CFTimeout)
        
    def loadToonLab(self):
        # After the model is loaded, spawn it in
        def spawnToonLab(*args):
            self.toonLabs = args[0]
            self.toonLabs.reparentTo(render)
            self.toonLabs.setPos(0, -140, -60.3)
        
        # Asynchronously load the model to not lag the game
        asyncloader.loadModel('phase_14/models/looneylabs/temp_observatory', callback = spawnToonLab) # TODO: Models
        pass
        
    def loadCogLab(self):
        # After the model is loaded, spawn it in
        def spawnCogLab(*args):
            self.cogLabs = args[0]
            self.cogLabs.reparentTo(render)
        
        # Asynchronously load the model to not lag the game
        #asyncloader.loadModel('phase_14/models/looneylabs/looney_labs_cog', callback = spawnCogLab) # TODO: Models
        pass
        
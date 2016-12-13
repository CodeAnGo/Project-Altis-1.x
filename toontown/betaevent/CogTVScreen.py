'''
Created on Apr 15, 2016

@author: Drew
'''
from direct.fsm.FSM import FSM
from panda3d.core import NodePath

from toontown.suit.BossCog import BossCog
from toontown.suit.SuitDNA import SuitDNA


class CogTVScreen(NodePath):
    def __init__(self, name):
        NodePath.__init__(self, name)
        self.camPos = (0, 0, 0, 0, 0, 0)
        
    def delete(self):
        NodePath.removeNode(self)
        
    def setCamPos(self, px, py, pz, rh, rp, rr):
        self.camPos = (px, py, pz, rh, rp, rr)
        
    def getCamPos(self):
        return self.camPos

# These are the individual scenes

class IntroductionScene(CogTVScreen, FSM):
    '''Maybe have some boss like the chairman saying something - kind of like tti's blimp plan'''
    def __init__(self):
        CogTVScreen.__init__(self, 'IntroductionScene')
        FSM.__init__(self, 'IntroductionScene')

        self.hqLobby = loader.loadModel('phase_9/models/cogHQ/SellbotHQLobby')
        self.hqLobby.reparentTo(self)
        
        self.vp = BossCog()
        dna = SuitDNA()
        dna.newBossCog('s')
        self.vp.setDNA(dna)
        self.vp.reparentTo(self)
        self.vp.setPosHpr(6, 35, 0, 168, 0, 0)
        self.vp.loop('Bb_neutral')
        
    def delete(self):
        if self.vp is not None:
            self.vp.delete()
            self.vp = None
            
        if self.hqLobby is not None:
            self.hqLobby.removeNode()
            self.hqLobby = None
            
        IntroductionScene.delete(self)
        
    def enterSceneOne(self):
        self.setCamPos(1, -.5, 18, 0, 0, 0)
        


from DistributedEventAI import DistributedEventAI
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals


class DistributedBetaEventAI(DistributedBetaEventAI):
    notify = directNotify.newCategory('DistributedBetaEventAI')

    def __init__(self, air):
        DistributedEventAI.__init__(self, air)
        self.air = air

    def start(self):
        DistributedEventAI.start(self)
        
    def systemMessageAll(self, text):
        # Whisper to everyone if we need to
        for doId in simbase.air.doId2do:
            if str(doId)[:2] == '10':
                player = simbase.air.doId2do.get(doId)
                player.d_setSystemMessage(0, text)


    def enterPreEvent(self):
        pass

    def exitPreEvent(self):
        pass
        
    def enterCogTv(self):
        pass
        
    def exitCogTv(self):
        pass
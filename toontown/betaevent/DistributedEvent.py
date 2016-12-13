from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM

class DistributedEvent(DistributedObject, FSM):
    notify = directNotify.newCategory('DistributedEvent')

    def __init__(self,cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, self.__class__.__name__)
    
    def announceGenerate(self):
        self.cr.event = self
    
    def start(self):
        pass

    def setState(self, state, timestamp):
        self.request(state, timestamp)
        
    def delete(self):
        self.cr.event = None
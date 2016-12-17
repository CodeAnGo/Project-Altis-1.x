from panda3d.core import *
from panda3d.direct import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class StaffManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('StaffManager')
	
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
		
    def modOnline(self, doId):
        #messenger.send('modOnline', [doId]) These aren't working quite yet
        pass
		
    def adminOnline(self, doId):
        #messenger.send('adminOnline', [doId])
        pass
		
    def sysadminOnline(self, doId):
        #messenger.send('sysadminOnline', [doId])
        pass

    def staffOffline(self, doId):
        #messenger.send('friendOffline', [doId])
        pass
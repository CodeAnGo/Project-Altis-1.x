import random
from panda3d.core import *
from panda3d.direct import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from pandac.PandaModules import NodePath
from toontown.toonbase import ToontownGlobals
ChangeDirectionDebounce = 1.0
ChangeDirectionTime = 1.0

class DistributedMMPiano(DistributedObject.DistributedObject):
    whitePartNodeName = 'midkey_floor_1'
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.spinStartTime = 0.0
        self.rpm = 0.0
        self.degreesPerSecond = self.rpm / 60.0 * 360.0
        self.offset = 0.0
        self.speedUpSound = None
        self.changeDirectionSound = None
        self.lastChangeDirection = 0.0

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        taskMgr.doMethodLater(4, self.setupGeom, self.uniqueName('setup-geom'))
        
    def setupGeom(self, task):
        geom = self.cr.playGame.getPlace().loader.geom            
        self.piano = geom.find('**/center_icon')
        if self.piano.isEmpty():
            loader.notify.error('Piano not found')
            return

        geom.find('**/center_icon').setPos(0,-20.1,0)
        geom.find('**/midkey_floor').setPos(0,20.1,0)
        geom.find('**/pond_floor').setPos(0,20.1,0)
        geom.find('**/pond_floor').setScale(1.01,1.01,1)
        geom.find('**/MMsz_water').setPos(0,20.0,0)
        geom.find('**/midkey_floor').setScale(1.01,1.01,1)
        geom.find('**/midkey_floor_1').setScale(1.01,1.01,1)
        base.cr.parentMgr.registerParent(ToontownGlobals.SPMinniesPiano, self.piano)
        self.accept('enter' + self.whitePartNodeName, self.__handleOnFloor)
        self.accept('exit' + self.whitePartNodeName, self.__handleOffFloor)
        self.accept('entermid_fishpond', self.__handleChangeDirectionButton)
        self.speedUpSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_gliss.ogg')
        self.changeDirectionSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_cymbal.ogg')
        self.__setupSpin()
        return task.done

    def __setupSpin(self):
        taskMgr.add(self.__updateSpin, self.taskName('pianoSpinTask'))

    def __stopSpin(self):
        taskMgr.remove(self.taskName('pianoSpinTask'))

    def __updateSpin(self, task):
        if self.degreesPerSecond == 0:
            return Task.cont
            
        elapsed = globalClock.getRealTime() - self.spinStartTime
        offset = self.offset
        heading = ((self.degreesPerSecond * elapsed) + offset) % 360
        self.piano.setH(heading)
        return Task.cont

    def disable(self):
        if hasattr(self, 'piano'):
            del self.piano
            base.cr.parentMgr.unregisterParent(ToontownGlobals.SPMinniesPiano)
        self.ignoreAll()
        self.speedUpSound = None
        self.changeDirectionSound = None
        self.__stopSpin()
        DistributedObject.DistributedObject.disable(self)

    def setSpeed(self, rpm, offset, timestamp):
        timestamp = globalClockDelta.networkToLocalTime(timestamp)
        degreesPerSecond = rpm / 60.0 * 360.0
        self.rpm = rpm
        self.degreesPerSecond = degreesPerSecond
        self.offset = offset
        self.spinStartTime = timestamp

    def playSpeedUp(self, avId):
        if avId != base.localAvatar.doId:
            base.playSfx(self.speedUpSound)

    def playChangeDirection(self, avId):
        if avId != base.localAvatar.doId:
            base.playSfx(self.changeDirectionSound)

    def __handleOnFloor(self, collEntry):
        self.cr.playGame.getPlace().activityFsm.request('OnPiano')
        self.sendUpdate('requestSpeedUp', [])
        base.playSfx(self.speedUpSound)

    def __handleOffFloor(self, collEntry):
        self.cr.playGame.getPlace().activityFsm.request('off')
        self.sendUpdate('requestSlowDown', [])

    def __handleSpeedUpButton(self, collEntry):
        self.sendUpdate('requestSpeedUp', [])
        base.playSfx(self.speedUpSound)

    def __handleChangeDirectionButton(self, collEntry):
        now = globalClock.getFrameTime()
        if now - self.lastChangeDirection < ChangeDirectionDebounce:
            loader.notify.debug('Rejecting change direction.')
            return
        shouldChange = random.randint(1,10)
        if int(shouldChange) == 10:
            self.lastChangeDirection = now
            self.sendUpdate('requestChangeDirection', [])
            base.playSfx(self.changeDirectionSound)
        else:
            loader.notify.debug('Rejecting change direction.')

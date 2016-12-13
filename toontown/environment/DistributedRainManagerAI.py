from panda3d.core import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
import random
import time
from direct.showbase import PythonUtil
import DayTimeGlobals
from DistributedWeatherMGRAI import DistributedWeatherMGRAI

class DistributedRainManagerAI(DistributedWeatherMGRAI):
    notify = directNotify.newCategory('DistributedRainManagerAI')
    
    def __init__(self, air):
        DistributedWeatherMGRAI.__init__(self, air)
        self.interval = 150

    def start(self, alwaysRain = False):
        DistributedWeatherMGRAI.start(self)
        
        # run a task to randomly start and stop snow, rain
        taskMgr.doMethodLater(self.interval, self.tick, 'weather-tick')
    
    def tick(self, task):
        if base.config.GetBool('want-rain'):
            if random.choice([True, False]):
                self.b_setState('Rain')
            else:
                self.b_setState('Sunny')
        else:
            self.b_setState('Snow')
        
        return task.again
    
    def stop(self):
        taskMgr.remove('weather-tick')

    def enterRain(self):
        pass
        
    def exitRain(self):
        pass
        
    def enterSunny(self):
        pass
        
    def exitSunny(self):
        pass

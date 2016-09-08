from pandac.PandaModules import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
import random

class ToontownLoadingScreen():
    __module__ = __name__

    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.gui = loader.loadModel('phase_3/models/gui/progress-background')
        self.banner = loader.loadModel('phase_3/models/gui/toon_council').find('**/scroll')
        self.banner.reparentTo(self.gui)
        self.banner.setScale(0.4, 0.4, 0.4)
        self.tip = DirectLabel(guiId='ToontownLoadingScreenTip', parent=self.banner, relief=None, text='', text_scale=TTLocalizer.TLStip, textMayChange=1, pos=(-1.2, 0.0, 0.1), text_fg=(0.4, 0.3, 0.2, 1), text_wordwrap=13, text_align=TextNode.ALeft)
        self.title = DirectLabel(guiId='ToontownLoadingScreenTitle', parent=self.gui, relief=None, pos=(0.05,0,-0.78), text='', textMayChange=1, text_scale=0.13, text_fg=(1,1,1,1), text_align=TextNode.ACenter, text_font=ToontownGlobals.getSignFont())
        self.waitBar = DirectWaitBar(guiId='ToontownLoadingScreenWaitBar', parent=self.gui, frameSize=(base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03), pos=(0, 0,-0.85), text='')
        logoScale = (1.10, 0.70, 0.70)  # Scale for our logo.
        self.logo = OnscreenImage(
            image='phase_3/maps/toontown-logo.png',
            scale=logoScale)
        self.logo.reparentTo(hidden)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        scale = self.logo.getScale()
        # self.logo.setPos(scale[0], 0, -scale[2])
        self.logo.setPos(0, 0, 0.65)
        return

    def destroy(self):
        self.tip.destroy()
        self.title.destroy()
        self.waitBar.destroy()
        self.banner.removeNode()
        self.gui.removeNode()
        self.logo.removeNode()

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + '\n' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory, zoneId):
        self.waitBar['range'] = range
        self.title['text'] = label
        if ToontownGlobals.BossbotHQ <= zoneId <= ToontownGlobals.LawbotHQ:
            self.title['text_font'] = ToontownGlobals.getSuitFont()
        else:
            self.title['text_font'] = ToontownGlobals.getSignFont()
        self.tip['text'] = self.getTip(tipCategory)
        self.__count = 0
        self.__expectedCount = range
        if gui:
            self.waitBar.reparentTo(self.gui)
            self.title.reparentTo(self.gui)
            self.logo.reparentTo(self.gui)
            self.gui.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        else:
            self.waitBar.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.title.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.logo.reparentTo(hidden)
            self.gui.reparentTo(hidden)
        self.waitBar.update(self.__count)

    def end(self):
        self.waitBar.finish()
        self.waitBar.reparentTo(self.gui)
        self.title.reparentTo(self.gui)
        self.gui.reparentTo(hidden)
        self.logo.reparentTo(hidden)
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.__count = self.__count + 1
        self.waitBar.update(self.__count)




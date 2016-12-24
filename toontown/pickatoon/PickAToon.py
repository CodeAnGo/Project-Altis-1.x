'''
Created on Sep 12, 2016

@author: Drew
'''

from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from panda3d.core import *
import random

from toontown.hood import SkyUtil
from toontown.launcher import DownloadForceAcknowledge
from toontown.toon import ToonDNA, Toon, ToonHead
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp
from toontown.toontowngui.TTDialog import *
import PickAToonOptions
from toontown.pickatoon import ShardPicker
from toontown.toontowngui import FeatureComingSoonDialog

COLORS = (Vec4(0.917, 0.164, 0.164, 1),
 Vec4(0.152, 0.75, 0.258, 1),
 Vec4(0.598, 0.402, 0.875, 1),
 Vec4(0.133, 0.59, 0.977, 1),
 Vec4(0.895, 0.348, 0.602, 1),
 Vec4(0.977, 0.816, 0.133, 1))
 
# The main position
MAIN_POS = (-60, 0, 11)
MAIN_HPR = (-90, -2, 0)

# To be used when entering PAT
TOON_HALL_POS = (110, 0, 8)
TOON_HALL_HPR = (-90, 0, 0)

# To be used when going to menu
HQ_POS = (14, 16, 8)
HQ_HPR = (-48, 0, 0)

DEL = TTLocalizer.PhotoPageDelete + ' %s?'
chooser_notify = DirectNotifyGlobal.directNotify.newCategory('PickAToon')

MAX_AVATARS = 6

class PickAToon:
    
    def __init__(self, avatarList, parentFSM, doneEvent):
        self.toonList = {i: (i in [x.position for x in avatarList]) for i in xrange(6)}
        self.avatarList = avatarList
        self.selectedToon = 0
        self.doneEvent = doneEvent
        self.jumpIn = None
        if base.showDisclaimer:
            FeatureComingSoonDialog.FeatureComingSoonDialog(text="\1textShadow\1Disclaimer:\2\nThis is an ALPHA build of Project Altis! There may be many bugs and crashes! If you encounter any, PLEASE report them to the developers!\nThanks, and enjoy Project Altis!")
        #self.optionsMgr = PickAToonOptions.PickAToonOptions()
        self.optionsMgr = PickAToonOptions.NewPickAToonOptions() # This is for the revamped options screen
        self.shardPicker = ShardPicker.ShardPicker()
        return

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)
        
    def enter(self):
        base.disableMouse()
        if base.showDisclaimer:
            settings['show-disclaimer'] = False
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        self.deleteButton.show()
        self.patNode.unstash()
        self.checkPlayButton()
        self.updateFunc()
                
    def exit(self):
        base.cam.iPosHpr()
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.deleteButton.hide()
        return None

    def load(self):
        self.patNode = render.attachNewNode('patNode')
        self.patNode2d = aspect2d.attachNewNode('patNode2d')
        gui = asyncloader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        gui2 = asyncloader.loadModel('phase_3/models/gui/quit_button')
        newGui = asyncloader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        

        self.title = OnscreenText(TTLocalizer.AvatarChooserPickAToon, scale=TTLocalizer.ACtitle, parent=hidden, fg=(1, 0.9, 0.1, 1), pos=(0.0, 0.82))

        # Quit Button
        quitHover = gui.find('**/QuitBtn_RLVR')
        self.quitHover = quitHover
        self.quitButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None, text=TTLocalizer.AvatarChooserQuit, text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=TTLocalizer.ACquitButton, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, pos=(1.08, 0, -0.907), command=self.__handleQuit)
        self.quitButton.reparentTo(base.a2dBottomLeft)
        self.quitButton.setPos(0.25, 0, 0.075)
        
        # Options Button
        self.optionsButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None, text="Options", text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=TTLocalizer.ACquitButton, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, pos=(1.08, 0, -0.907), command=self.openOptions)
        self.optionsButton.reparentTo(base.a2dBottomRight)
        self.optionsButton.setPos(-0.25, 0, 0.075)
        
        # Shard Selector Button
        self.shardsButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None, text="Districts", text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=0.08, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, pos=(1.08, 0, -0.907), command=self.openShardPicker)
        self.shardsButton.reparentTo(base.a2dBottomLeft)
        self.shardsButton.setPos(0.25, 0, 0.2)
        
        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()

        # Area toon is in
        self.area = OnscreenText(parent=self.patNode2d, font=ToontownGlobals.getToonFont(),
                                 pos=(-.1, -.1), scale=.075, text='', shadow=(0, 0, 0, 1), fg=COLORS[self.selectedToon])

        # DMENU Pat Screen Stuff
        self.play = DirectButton(relief = None, image = (quitHover, quitHover, quitHover), text = 'PLAY THIS TOON', text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=(0, -.016), text_scale = 0.045, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.4, pos=(0, 0, -0.90), command=self.playGame, parent=self.patNode2d)
        
        self.toon = Toon.Toon()
        self.toon.setPosHpr(-46, 0, 8.1, 90, 0, 0)
        self.toon.reparentTo(self.patNode)
        self.toon.stopLookAroundNow()
        
        def spawnToonButtons(*args):
            self.pickAToonGui = args[0]
            self.buttonBgs = []
            self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareRed'))
            self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareGreen'))
            self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squarePurple'))
            self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareBlue'))
            self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squarePink'))
            self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareYellow'))
            
            self.toon1 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [0], image = self.buttonBgs[0])
            self.toon1.reparentTo(self.patNode2d)
            self.toon1.setPos(-1, 0, 0.5)
            self.toon1.setScale(.5)
            
            self.toon2 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [1], image = self.buttonBgs[1])
            self.toon2.reparentTo(self.patNode2d)
            self.toon2.setPos(-.6, 0, 0.5)
            self.toon2.setScale(.5)
            
            self.toon3 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [2], image = self.buttonBgs[2])
            self.toon3.reparentTo(self.patNode2d)
            self.toon3.setPos(-.2, 0, 0.5)
            self.toon3.setScale(.5)
            
            self.toon4 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [3], image = self.buttonBgs[3])
            self.toon4.reparentTo(self.patNode2d)
            self.toon4.setPos(.2, 0, 0.5)
            self.toon4.setScale(.5)
            
            self.toon5 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [4], image = self.buttonBgs[4])
            self.toon5.reparentTo(self.patNode2d)
            self.toon5.setPos(.6, 0, 0.5)
            self.toon5.setScale(.5)
            
            self.toon6 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [5], image = self.buttonBgs[5])
            self.toon6.reparentTo(self.patNode2d)
            self.toon6.setPos(1, 0, 0.5)
            self.toon6.setScale(.5)
            
            self.setButtonNames()
            
        asyncloader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui', callback = spawnToonButtons)

        # Delete Toon button
        trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui.bam')
        self.deleteButton = DirectButton(parent=base.a2dBottomRight,
                                         geom=(trashcanGui.find('**/TrashCan_CLSD'),
                                               trashcanGui.find('**/TrashCan_OPEN'),
                                               trashcanGui.find('**/TrashCan_RLVR')),
                                         text=('', TTLocalizer.AvatarChoiceDelete,
                                                   TTLocalizer.AvatarChoiceDelete, ''),
                                         text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                         text_scale=0.15, text_pos=(0, -0.1), relief=None,
                                         scale=.5, command=self.__handleDelete, pos=(-.2, 0, .25))

    def selectToon(self, slot):
        self.selectedToon = slot
        self.updateFunc()
        
    def updateFunc(self):
        self.haveToon = self.toonList[self.selectedToon]
        self.area['fg'] = COLORS[self.selectedToon]
        if self.jumpIn:
            self.jumpIn.finish()
        if self.haveToon:
            self.showToon()
            taskMgr.add(self.turnHead, "turnHead")
            camZ = self.toon.getHeight()
            base.camera.setPos(-60, 0, 8 + camZ)
            self.deleteButton.show()
        else:
            self.toon.hide()
            base.camera.setPos(-60, 0, 11)
            taskMgr.remove("turnHead")
            self.deleteButton.hide()
        self.checkPlayButton()
        self.area['text'] = ''
            
    def showToon(self):
        av = [x for x in self.avatarList if x.position == self.selectedToon][0]
        dna = av.dna
        
        self.toon.setDNAString(dna)
        #self.jumpIn = Sequence(
        #         Func(self.toon.animFSM.request, 'PATTeleportIn'),
        #         Wait(2),
        #         Func(self.toon.animFSM.request, 'neutral'))
        #self.jumpIn.start() # ALTIS: TODO: Add the states to Toon.py
        self.toon.animFSM.request('neutral')
        self.toon.setName(av.name)
        self.toon.show()
        lastAreaName = ToontownGlobals.hoodNameMap.get(av.lastHood, [''])[-1]
        self.area.setText(lastAreaName)

    def turnHead(self, task):
        def clamprotation(i, mn = -1, mx = 1):
            return min(max(i, mn), mx)
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.toon.getGeomNode().find('**/__Actor_head').setP(clamprotation(mpos.getY()) * 25)
            self.toon.getGeomNode().find('**/__Actor_head').setH(clamprotation(mpos.getX()) * 40)

        return Task.cont
        
    def checkPlayButton(self):
        if self.toonList[self.selectedToon]:
            self.play['text'] = 'PLAY THIS TOON'
            self.play['command'] = self.playGame
        else:
            self.play['text'] = 'MAKE A TOON'
            self.play['command'] = self.makeToon
            
    def playGame(self):
        if self.jumpIn:
            self.jumpIn.finish()
        doneStatus = {"mode": "chose", "choice": self.selectedToon}
        #Sequence (
        #          Func(self.toon.animFSM.request, 'PATTeleportOut'),
        #          Wait(4),
        #          Func(messenger.send, self.doneEvent, [doneStatus]))#.start() # ALTIS: TODO: Add the states to toon.py
        messenger.send(self.doneEvent, [doneStatus])

    def makeToon(self):
        doneStatus = {"mode": "create", "choice": self.selectedToon}
        messenger.send(self.doneEvent, [doneStatus])
        
    def setButtonNames(self):
        for k in self.avatarList:
            if k.position == 0:
                av1 = k
                self.head1 = hidden.attachNewNode('head1')
                self.head1.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head1.reparentTo(self.toon1)
                self.headModel1 = ToonHead.ToonHead()
                self.headModel1.setupHead(ToonDNA.ToonDNA(av1.dna), forGui=1)
                self.headModel1.reparentTo(self.head1)
        
        for k in self.avatarList:
            if k.position == 1:
                av2 = k
                self.head2 = hidden.attachNewNode('head2')
                self.head2.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head2.reparentTo(self.toon2)
                self.headModel2 = ToonHead.ToonHead()
                self.headModel2.setupHead(ToonDNA.ToonDNA(av2.dna), forGui=1)
                self.headModel2.reparentTo(self.head2)
        
        for k in self.avatarList:
            if k.position == 2:
                av3 = k
                self.head3 = hidden.attachNewNode('head3')
                self.head3.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head3.reparentTo(self.toon3)
                self.headModel3 = ToonHead.ToonHead()
                self.headModel3.setupHead(ToonDNA.ToonDNA(av3.dna), forGui=1)
                self.headModel3.reparentTo(self.head3)
        
        for k in self.avatarList:
            if k.position == 3:
                av4 = k
                self.head4 = hidden.attachNewNode('head4')
                self.head4.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head4.reparentTo(self.toon4)
                self.headModel4 = ToonHead.ToonHead()
                self.headModel4.setupHead(ToonDNA.ToonDNA(av4.dna), forGui=1)
                self.headModel4.reparentTo(self.head4)
        
        for k in self.avatarList:
            if k.position == 4:
                av5 = k
                self.head5 = hidden.attachNewNode('head5')
                self.head5.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head5.reparentTo(self.toon5)
                self.headModel5 = ToonHead.ToonHead()
                self.headModel5.setupHead(ToonDNA.ToonDNA(av5.dna), forGui=1)
                self.headModel5.reparentTo(self.head5)
        
        for k in self.avatarList:
            if k.position == 5:
                av6 = k
                self.head6 = hidden.attachNewNode('head6')
                self.head6.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head6.reparentTo(self.toon6)
                self.headModel6 = ToonHead.ToonHead()
                self.headModel6.setupHead(ToonDNA.ToonDNA(av6.dna), forGui=1)
                self.headModel6.reparentTo(self.head6)

    def unload(self):
        taskMgr.remove("turnHead")
        cleanupDialog('globalDialog')
        self.patNode.removeNode()
        del self.patNode
        self.patNode2d.removeNode()
        del self.patNode2d
        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton
        self.optionsButton.destroy()
        del self.optionsButton
        self.shardsButton.destroy()
        del self.shardsButton
        self.shardPicker.unload()
        del self.avatarList
        self.toon.removeNode()
        del self.toon
        base.cr.DMENU_SCREEN.murder()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        return None

    def getChoice(self):
        return self.selectedToon

    def __handleDelete(self):
        av = [x for x in self.avatarList if x.position == self.selectedToon][0]

        def diagDone():
            mode = delDialog.doneStatus
            delDialog.cleanup()
            base.transitions.noFade()
            if mode == 'ok':
                messenger.send(self.doneEvent, [{'mode': 'delete'}])
        
        base.acceptOnce('pat-del-diag-done', diagDone)
        delDialog = TTGlobalDialog(message=DEL % av.name, style=YesNo,
                                   doneEvent='pat-del-diag-done')
        base.transitions.fadeScreen(.5)

    def __handleQuit(self):
        cleanupDialog('globalDialog')
        self.doneStatus = {'mode': 'exit'}
        messenger.send(self.doneEvent, [self.doneStatus])

    def openOptions(self):
        self.optionsMgr.showOptions()
        self.optionsButton["text"] = "Back"
        self.optionsButton["command"] = self.hideOptions
        self.shardsButton.hide()
        self.patNode2d.hide()
        self.patNode.hide()
        if self.haveToon:
            self.deleteButton.hide()

    def hideOptions(self):
        self.optionsMgr.hideOptions()
        self.optionsButton["text"] = "Options"
        self.optionsButton["command"] = self.openOptions
        self.shardsButton.show()
        self.patNode2d.show()
        self.patNode.show()
        if self.haveToon:
            self.deleteButton.show()
            
    def openShardPicker(self):
        self.shardPicker.showPicker()
        self.shardsButton["text"] = "Back"
        self.shardsButton["command"] = self.hideShardPicker
        self.patNode2d.hide()
        self.patNode.hide()
        if self.haveToon:
            self.deleteButton.hide()

    def hideShardPicker(self):
        self.shardPicker.hidePicker()
        self.shardsButton["text"] = "Districts"
        self.shardsButton["command"] = self.openShardPicker
        self.patNode2d.show()
        self.patNode.show()
        if self.haveToon:
            self.deleteButton.show()
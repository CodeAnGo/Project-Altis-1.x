from panda3d.core import *
from panda3d.direct import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
import string
from toontown.toon import LaffMeter
from toontown.battle import BattleBase
from direct.gui.DirectGui import *
from panda3d.core import *
from panda3d.direct import *
from toontown.toonbase import TTLocalizer

class TownBattleToonPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleToonPanel')

    def __init__(self, id):
        if settings['newGui'] == True:
            gui = loader.loadModel('phase_3.5/models/gui/battle_gui_new')
        else:
            gui = loader.loadModel('phase_3.5/models/gui/battle_gui_old')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=Vec4(0.5, 0.9, 0.5, 0.7))
        self.setScale(0.8)
        self.initialiseoptions(TownBattleToonPanel)
        self.avatar = None
        self.sosText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=TTLocalizer.TownBattleToonSOS, text_scale=0.06)
        self.sosText.hide()
        self.fireText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=TTLocalizer.TownBattleToonFire, text_scale=0.06)
        self.fireText.hide()
        self.roundsText = DirectLabel(parent=self, relief=None, pos=(0.16, 0, -0.07), text='', text_scale=0.045)
        self.roundsText.hide()
        self.undecidedText = DirectLabel(parent=self, relief=None, pos=(0.1, 0, 0.015), text=TTLocalizer.TownBattleUndecided, text_scale=0.1)
        self.healthText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.hpChangeEvent = None
        self.gagNode = self.attachNewNode('gag')
        self.gagNode.setPos(0.1, 0, 0.03)
        self.hasGag = 0
        passGui = gui.find('**/tt_t_gui_bat_pass')
        passGui.detachNode()
        self.passNode = self.attachNewNode('pass')
        self.passNode.setPos(0.1, 0, 0.05)
        passGui.setScale(0.2)
        passGui.reparentTo(self.passNode)
        self.passNode.hide()
        self.laffMeter = None
        self.whichText = DirectLabel(parent=self, text='', pos=(0.1, 0, -0.08), text_scale=0.05)
        self.hide()
        gui.removeNode()
        return

    def setLaffMeter(self, avatar):
        self.notify.debug('setLaffMeter: new avatar %s' % avatar.doId)
        if self.avatar == avatar:
            messenger.send(self.avatar.uniqueName('hpChange'), [avatar.hp, avatar.maxHp, 1])
            return None
        else:
            if self.avatar:
                self.cleanupLaffMeter()
            self.avatar = avatar
            self.laffMeter = LaffMeter.LaffMeter(avatar.style, avatar.hp, avatar.maxHp)
            self.laffMeter.setAvatar(self.avatar)
            self.laffMeter.reparentTo(self)
            self.laffMeter.setPos(-0.06, 0, 0.05)
            self.laffMeter.setScale(0.045)
            self.laffMeter.start()
            self.setHealthText(avatar.hp, avatar.maxHp)
            self.hpChangeEvent = self.avatar.uniqueName('hpChange')
            self.accept(self.hpChangeEvent, self.setHealthText)
        return None

    def setHealthText(self, hp, maxHp, quietly = 0):
        self.healthText['text'] = TTLocalizer.TownBattleHealthText % {'hitPoints': hp,
         'maxHit': maxHp}

    def show(self):
        DirectFrame.show(self)
        if self.laffMeter:
            self.laffMeter.start()

    def hide(self):
        DirectFrame.hide(self)
        if self.laffMeter:
            self.laffMeter.stop()

    def updateLaffMeter(self, hp):
        if self.laffMeter:
            self.laffMeter.adjustFace(hp, self.avatar.maxHp)
        self.setHealthText(hp, maxHp)

    def setValues(self, index, track, level = None, numTargets = None, targetIndex = None, localNum = None):
        self.notify.debug('Toon Panel setValues: index=%s track=%s level=%s numTargets=%s targetIndex=%s localNum=%s' % (index,
         track,
         level,
         numTargets,
         targetIndex,
         localNum))
        self.undecidedText.hide()
        self.sosText.hide()
        self.fireText.hide()
        self.roundsText.hide()
        self.gagNode.hide()
        self.whichText.hide()
        self.passNode.hide()
        self.whichText.setPos(0.1, 0, -0.08)
        self.whichText['text_scale'] = 0.05
        if self.hasGag:
            self.gag.removeNode()
            self.hasGag = 0
        if track == BattleBase.NO_ATTACK or track == BattleBase.UN_ATTACK:
            self.undecidedText.show()
        elif track == BattleBase.PASS_ATTACK:
            self.passNode.show()
        elif track == BattleBase.FIRE:
            self.fireText.show()
            self.whichText.show()
            self.whichText['text'] = self.determineWhichText(numTargets, targetIndex, localNum, index)
        elif track == BattleBase.SOS or track == BattleBase.NPCSOS or track == BattleBase.PETSOS:
            self.sosText.show()
        elif track >= MIN_TRACK_INDEX and track <= MAX_TRACK_INDEX:
            self.undecidedText.hide()
            self.passNode.hide()
            self.gagNode.show()
            invButton = base.localAvatar.inventory.buttonLookup(track, level)
            self.gag = invButton.instanceUnderNode(self.gagNode, 'gag')
            self.gag.setScale(0.8)
            self.gag.setPos(0, 0, 0.02)
            self.hasGag = 1
            if numTargets is not None and targetIndex is not None and localNum is not None:
                self.whichText.show()
                self.whichText['text'] = self.determineWhichText(numTargets, targetIndex, localNum, index)
                self.roundsText.setPos(0.16, 0, -0.07)
                self.roundsText['text_scale'] = 0.045
            elif track == LURE_TRACK:
                self.roundsText['text_scale'] = 0.05
                self.roundsText.setPos(0.1, 0, -0.08)
            if track == LURE_TRACK:
                self.roundsText.show()
                self.roundsText['text'] = str(NumRoundsLured[level])
                self.whichText.setPos(0.085, 0, -0.07)
                self.whichText['text_scale'] = 0.045
        else:
            self.notify.error('Bad track value: %s' % track)
        return

    def determineWhichText(self, numTargets, targetIndex, localNum, index):
        returnStr = ''
        targetList = range(numTargets)
        targetList.reverse()
        for i in targetList:
            if targetIndex == -1:
                returnStr += 'X'
            elif targetIndex == -2:
                if i == index:
                    returnStr += '-'
                else:
                    returnStr += 'X'
            elif targetIndex >= 0 and targetIndex <= 3:
                if i == targetIndex:
                    returnStr += 'X'
                else:
                    returnStr += '-'
            else:
                self.notify.error('Bad target index: %s' % targetIndex)

        return returnStr

    def cleanup(self):
        self.ignoreAll()
        self.cleanupLaffMeter()
        if self.hasGag:
            self.gag.removeNode()
            del self.gag
        self.gagNode.removeNode()
        del self.gagNode
        DirectFrame.destroy(self)

    def cleanupLaffMeter(self):
        self.notify.debug('Cleaning up laffmeter!')
        self.ignore(self.hpChangeEvent)
        if self.laffMeter:
            self.laffMeter.destroy()
            self.laffMeter = None
        return

from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
import string
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from panda3d.core import TransparencyAttrib, VBase3, TextNode
from direct.interval.IntervalGlobal import Wait, Func, Sequence, LerpColorScaleInterval, Parallel, LerpFunctionInterval

class PopupDialog:

    def __init__(self):
        self.popupGui = aspect2d.attachNewNode('popupGui')
        self.popupGui.reparentTo(aspect2d, 3000)
        self.dialogText = OnscreenText(text='put text here', align=TextNode.ACenter, scale=0.1, pos=(0, .2, 0), wordwrap = 20)
        self.background = OnscreenImage(image = 'phase_3.5/maps/loading/toon.jpg', parent = aspect2d)
        self.background.setBin('background', 1)
        self.background.reparentTo(aspect2d)
        self.background.setScale(2, 1, 1)
        
        self.yesButton = DirectButton(relief = None, text_style = 3, text_fg = (1, 1, 1, 1), text = 'Yes', text_scale = .1, scale = 0.95, command = self.doYesButton)
        self.yesButton.reparentTo(aspect2d)
        self.yesButton.setPos(0, 0, -.4)
        
        self.noButton = DirectButton(relief = None, text_style = 3, text_fg = (1, 1, 1, 1), text = 'No', text_scale = .1, scale = 0.95, command = self.doNoButton)
        self.noButton.reparentTo(aspect2d)
        self.noButton.setPos(0, 0, -.6)
        
    def start(self, text='put text here', yesText = 'Yes', noText = 'No', doneEvent = None, isError = False):
        self.dialogText['text'] = text
        self.yesButton['text'] = yesText
        self.noButton['text'] = noText
        
        self.background.show()
        self.yesButton.show()
        self.noButton.show()
        
        self.background.wrtReparentTo(self.popupGui)
        self.dialogText.wrtReparentTo(self.popupGui)
        self.yesButton.wrtReparentTo(self.popupGui)
        self.noButton.wrtReparentTo(self.popupGui)
        
        self.doneEvent = doneEvent
        if isError:
            base.playSfx((base.loader.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.ogg')))
        
        if yesText == 'HIDE_YES': # If we don't want the yes button to show, we set yesText to 'HIDE_YES' -- same with 'HIDE_NO'
            self.yesButton.hide()
            self.noButton.setPos(0, 0, -.4)
            
        elif noText == 'HIDE_NO':
            self.noButton.hide()
            self.yesButton.setPos(0, 0, -.4)
        
    def doYesButton(self):
        self.doneStatus = 'ok'
        messenger.send(self.doneStatus)
    
    def doNoButton(self):
        self.doneStatus = 'cancel'
        messenger.send(self.doneStatus)
        
    def stop(self):
        if self.popupGui:
            self.popupGui.removeNode()
            self.popupGui = None
            
        if self.dialogText:
            self.dialogText.destroy()
            self.dialogText = None

        if self.background:
            self.background.destroy()
            self.background = None
            
        if self.yesButton:
            self.yesButton.removeNode()
            self.yesButton = None
            
        if self.noButton:
            self.noButton.removeNode()
            self.noButton = None

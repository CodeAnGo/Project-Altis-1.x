from direct.gui.DirectGui import *
from panda3d.core import *
from panda3d.direct import *
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import TTLocalizer

class TrackPoster(DirectFrame):
    normalTextColor = (0.3, 0.25, 0.2, 1)

    def __init__(self, trackId, callback):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(TrackPoster)
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        self.trackName = ToontownBattleGlobals.Tracks[trackId].capitalize()
        self.poster = DirectFrame(parent=self, relief=None, image=bookModel.find('**/questCard'), image_scale=(0.8, 0.58, 0.58))
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        iconGeom = invModel.find('**/' + ToontownBattleGlobals.AvPropsNew[trackId][4])
        invModel.removeNode()
        self.pictureFrame = DirectFrame(parent=self.poster, relief=None, image=bookModel.find('**/questPictureFrame'), image_scale=0.25, image_color=(0.45, 0.8, 0.45, 1), text=self.trackName, text_font=ToontownGlobals.getInterfaceFont(), text_pos=(0, -0.16), text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ACenter, text_wordwrap=8.0, textMayChange=0, geom=iconGeom, pos=(-0.2, 0, 0.06))
        bookModel.removeNode()
        if trackId == ToontownBattleGlobals.HEAL_TRACK:
            help = TTLocalizer.TrackChoiceGuiHEAL
        elif trackId == ToontownBattleGlobals.TRAP_TRACK:
            help = TTLocalizer.TrackChoiceGuiTRAP
        elif trackId == ToontownBattleGlobals.LURE_TRACK:
            help = TTLocalizer.TrackChoiceGuiLURE
        elif trackId == ToontownBattleGlobals.SOUND_TRACK:
            help = TTLocalizer.TrackChoiceGuiSOUND
        elif trackId == ToontownBattleGlobals.THROW_TRACK:
            help = TTLocalizer.TrackChoiceGuiTHROW
        elif trackId == ToontownBattleGlobals.SQUIRT_TRACK:
            help = TTLocalizer.TrackChoiceGuiSQUIRT
        elif trackId == ToontownBattleGlobals.ZAP_TRACK:
            help = TTLocalizer.TrackChoiceGuiZAP
        elif trackId == ToontownBattleGlobals.DROP_TRACK:
            help = TTLocalizer.TrackChoiceGuiDROP
        else:
            help = ''
        self.helpText = DirectFrame(parent=self.poster, relief=None, text=help, text_font=ToontownGlobals.getInterfaceFont(), text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ALeft, text_wordwrap=8.0, textMayChange=0, pos=(-0.05, 0, 0.14))
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.chooseButton = DirectButton(parent=self.poster, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiChoose, text_scale=0.06, text_pos=(0, -0.02), command=callback, extraArgs=[trackId], pos=(0, 0, -0.45), scale=0.8)
        guiButton.removeNode()
        return


class TrackChoiceGui(DirectFrame):

    def __init__(self, tracks, timeout):
        DirectFrame.__init__(self, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=Vec4(0.8, 0.6, 0.4, 1), geom_scale=(1.5, 1, 1.5), geom_hpr=(0, 0, -90), pos=(-0.85, 0, 0))
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        arrowImage = (gui.find('**/tt_t_gui_mat_shuffleArrowUp'), gui.find('**/tt_t_gui_mat_shuffleArrowDown'))
        self.downArrow = DirectButton(parent=self, relief=None, image=arrowImage, pos=(-0.30, 0, -0.5), command=self.setPage, extraArgs=[-1])
        self.upArrow = DirectButton(parent=self, relief=None, image=arrowImage, pos=(0.30, 0, -0.5), scale=-1, command=self.setPage, extraArgs=[1])
        gui.removeNode()
        self.initialiseoptions(TrackChoiceGui)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.cancelButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiCancel, pos=(0.4, 0, -0.625), text_scale=0.06, text_pos=(0, -0.02), command=self.chooseTrack, extraArgs=[-1])
        guiButton.removeNode()
        self.trackName = DirectLabel(parent=self, relief=None, pos=(0, 0, -0.55), text='', text_font=ToontownGlobals.getBuildingNametagFont(), text_scale=0.1, text_fg=(1,1,1,1))
        self.index = 0
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.35)
        self.timer.setPos(0, 0, 0.6)
        self.timer.countdown(timeout, self.timeout)
        self.trackChoicePosters = []
        trackAccess = base.localAvatar.getTrackAccess()
        for trackId in xrange(ToontownBattleGlobals.NUM_GAG_TRACKS):
            if trackAccess[trackId] == 0:
                tp = TrackPoster(trackId, self.chooseTrack)
                tp.reparentTo(self)
                self.trackChoicePosters.append(tp)
        for track in self.trackChoicePosters:
            track.setPos(0, 0, 0)
            track.setScale(1.5)
            track.hide()
        self.setPage(self.index)
        return

    def chooseTrack(self, trackId):
        self.timer.stop()
        messenger.send('chooseTrack', [trackId])
		
    def setPage(self, direction):
        self.index = self.index + direction
        if len(self.trackChoicePosters) == 1:
            self.downArrow['state'] = DGG.DISABLED
            self.upArrow['state'] = DGG.DISABLED
        else:
            if self.index <= 0:
                self.downArrow['state'] = DGG.DISABLED
                self.upArrow['state'] = DGG.NORMAL
            elif self.index >= len(self.trackChoicePosters)-1:
                self.downArrow['state'] = DGG.NORMAL
                self.upArrow['state'] = DGG.DISABLED
            else:
                self.downArrow['state'] = DGG.NORMAL
                self.upArrow['state'] = DGG.NORMAL
        for track in self.trackChoicePosters:
            track.hide()
        self.trackChoicePosters[self.index].show()
        self.trackName['text'] = self.trackChoicePosters[self.index].trackName

    def timeout(self):
        messenger.send('chooseTrack', [-1])

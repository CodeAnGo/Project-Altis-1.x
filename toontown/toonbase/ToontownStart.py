from panda3d.core import *
from panda3d.direct import *
from toontown.distributed import PythonUtil
import __builtin__
import os


if __debug__:
    loadPrcFile('config/dev.prc')

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

import glob
for file in glob.glob('resources/*.mf'):
    mf = Multifile()
    mf.openReadWrite(Filename(file))
    names = mf.getSubfileNames()
    for name in names:
        ext = os.path.splitext(name)[1]
        if ext not in ['.jpg', '.jpeg', '.ogg', '.rgb']:
            mf.removeSubfile(name)
    vfs.mount(mf, Filename('/'), 0)

from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase.Settings import Settings
from otp.otpbase import OTPGlobals


notify = directNotify.newCategory('ToontownStart')
notify.setInfo(True)

settingsFilename = ConfigVariableString(
    'preferences-filename',
    'preferences.json'
).getValue()

notify.info('Reading %s...' % settingsFilename)

__builtin__.settings = Settings(settingsFilename)
__builtin__.NO_FADE_SORT_INDEX = 2000
__builtin__.FADE_SORT_INDEX = 1000
if 'res' not in settings:
    settings['res'] = (1280, 720)
if 'fullscreen' not in settings:
    settings['fullscreen'] = False
if 'musicVol' not in settings:
    settings['musicVol'] = 1.0
if 'sfxVol' not in settings:
    settings['sfxVol'] = 1.0
if 'loadDisplay' not in settings:
    settings['loadDisplay'] = 'pandagl'
if 'toonChatSounds' not in settings:
    settings['toonChatSounds'] = True
if 'newGui' not in settings:
    settings['newGui'] = False
if 'show-disclaimer' not in settings:
    settings['show-disclaimer'] = True
settings['newGui'] = False # Force this to be false

loadPrcFileData('Settings: res', 'win-size %d %d' % tuple(settings['res']))
loadPrcFileData('Settings: fullscreen', 'fullscreen %s' % settings['fullscreen'])
loadPrcFileData('Settings: musicVol', 'audio-master-music-volume %s' % settings['musicVol'])
loadPrcFileData('Settings: sfxVol', 'audio-master-sfx-volume %s' % settings['sfxVol'])
#loadPrcFileData('Settings: loadDisplay', 'load-display %s' % settings['loadDisplay'])
loadPrcFileData('Settings: newGui', 'newGui %s' % settings['newGui'])
loadPrcFileData('Settings: show-disclaimer', 'show-disclaimer %s' % settings['show-disclaimer'])
loadPrcFileData('', 'load-display pandagl')

class game:
    name = 'toontown'
    process = 'client'


__builtin__.game = game()
import time
import sys
import __builtin__
import os
import platform
try:
    launcher
except:
    from toontown.launcher.TTLauncher import TTLauncher
    launcher = TTLauncher()
    __builtin__.launcher = launcher

pollingDelay = 0.5

print('Starting the game...')
tempLoader = Loader()
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *

from toontown.pgui import DirectGuiGlobals as PGUIGlobals

print('Setting the default font...')
import ToontownGlobals

DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
PGUIGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)

import ToonBase
ToonBase.ToonBase()
from panda3d.core import *
if base.win is None:
    print('Unable to open window; aborting.')
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))

PGUIGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
PGUIGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
PGUIGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))

import TTLocalizer
if base.musicManagerIsValid:
    import random
    theme = ('phase_3/audio/bgm/tt_theme.ogg')
    music = base.loadMusic(theme)
    if music:
        music.setLoop(1)
        music.play()
    print('Loading the default GUI sounds...')
    DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = base.config.GetString('server-version', 'no_version_set')
print 'ToontownStart: serverVersion: ', serverVersion
version = OnscreenText(serverVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0.7, 0.7, 0.8, 1.0), align=TextNode.ALeft)
version.setPos(0.03,0.03)
version.reparentTo(base.a2dBottomLeft)
loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE, 0)
from ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
if not launcher.isDummy():
    base.startShow(cr, launcher.getGameServer())
else:
    base.startShow(cr)
del tempLoader
version.cleanup()
del version
base.loader = base.loader
__builtin__.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun:
    try:
        base.run()
    except SystemExit:
        raise
    except:
        print describeException()
        raise

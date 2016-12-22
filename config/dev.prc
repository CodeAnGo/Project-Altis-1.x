# DO NOT ENABLE UNLESS IN DEVELOPMENT
# Requirements:
# LibPandaDNA Built with 1.10.0 Pre-Release Non Static Lib
# OR
# Python DNA Reader
want-pipeline-renderer false

# Client settings
window-title Project Altis
server-version 1.1.0
build-version dev
sync-video #f
want-dev #f
preload-avatars #t
texture-anisotropic-degree 16
icon-filename phase_3/etc/icon.ico
audio-library-name p3fmod_audio
default-directnotify-level info
smooth-lag 0.4
support-stencil #f
framebuffer-stencil #f
textures-power-2 none
gl-finish #f
gl-force-no-error #t
gl-check-errors #f
gl-force-no-flush #t
gl-force-no-scissor #t
texture-magfilter linear
texture-minfilter linear
lock-to-one-cpu #f
support-threads #t
allow-incomplete-render #t
preload-simple-textures #t
allow-async-bind #t
gl-immutable-texture-storage #f
gl-dump-compiled-shaders #f
show-buffers #f
framebuffer-multisample #f
multisamples 0
# Pretty sure you're gonna want membership...
want-membership #t
want-speedhack-fix #t

# Disable after the holidays
want-rain #f


# VFS for resources.
vfs-mount resources/phase_3 /phase_3
vfs-mount resources/phase_3.5 /phase_3.5
vfs-mount resources/phase_4 /phase_4
vfs-mount resources/phase_5 /phase_5
vfs-mount resources/phase_5.5 /phase_5.5
vfs-mount resources/phase_6 /phase_6
vfs-mount resources/phase_7 /phase_7
vfs-mount resources/phase_8 /phase_8
vfs-mount resources/phase_9 /phase_9
vfs-mount resources/phase_10 /phase_10
vfs-mount resources/phase_11 /phase_11
vfs-mount resources/phase_12 /phase_12
vfs-mount resources/phase_13 /phase_13
model-path resources
default-model-extension .bam
model-cache-models #t
model-cache-textures #t

# Needed for running a local server...
eventlog-host 127.0.0.1

# Distributed Class File
dc-file config/ProjectAltis.dc

# Game Features
want-estates #t
want-pets #t
want-news-tab #f
want-news-page #f
want-accessories #t
want-parties #t
want-gardening #f
want-gifting #f
want-cogdominiums #t
want-boarding-groups #t
want-cheesy-expirations #t
want-toontorial #t
want-code-redemption #t
want-new-toonhall #t
want-picnic-games #f


# Playgrounds
want-playgrounds #t
want-toontown-central #t
want-donalds-dock #t
want-daisy-gardens #t
want-minnies-melodyland #t
want-the-brrrgh #t
want-donalds-dreamland #t
want-goofy-speedway #t
want-acorn-acres #t
want-mini-golf #t

# Cog HQs
want-cog-headquarters #t
want-sellbot-hq #t
want-cashbot-hq #t
want-lawbot-hq #t
want-bossbot-hq #t


# Misc. Modifications
estate-day-night #t
want-instant-parties #f
show-total-population #f

want-whitelist #t
force-avatar-understandable #t
force-player-understandable #t

force-holiday-decorations 6
active-holidays 63, 64, 65, 66
want-arg-manager #t

loading-threads 2

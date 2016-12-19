@echo off

set MAX_CHANNELS=999999
set STATE_SERVER=4002
set ASTRON_IP=188.165.250.225:7199
set EVENT_LOGGER_IP=188.165.250.225:7197
set DISTRICT_NAME=%~1
set BASE_CHANNEL=%~2
TITLE %DISTRICT_NAME%
set /P PPYTHON_PATH=<PPYTHON_PATH
echo ===============================
echo Starting Project Altis AI (district) Server...
echo ppython: %PPYTHON_PATH%
echo District Name: %DISTRICT_NAME%
echo Base Channel: %BASE_CHANNEL%
echo Max Channels: %MAX_CHANNELS%
echo State Server ID: %STATE_SERVER%
echo Message Director IP: %ASTRON_IP%
echo Event Logger IP: %EVENT_LOGGER_IP%
echo ===============================

:main
%PPYTHON_PATH% -m toontown.ai.ServiceStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATE_SERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENT_LOGGER_IP% ^
               --district-name "%DISTRICT_NAME%"
pause
goto main

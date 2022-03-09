:@echo off
setlocal
@echo Freeze rFactoryModManager into a single .exe with pyInstaller

call pyInstallerSetup env

::   --debug=imports 
::  --clean 
::  --paths env\Lib\site-packages 
::  --hidden-import pygame.base 

rem --icon doesn't seem to do anything
rem --noconsole removes the console in the background but for now
rem             it's best to keep it for error messages

::  --hiddenimport pkg_resources.py2_warn   Fixes ModuleNotFoundError: No module named 'pkg_resources.py2_warn'

REM Using the command line like this should also work but there were problems at some point.
pyinstaller ^
  --onefile ^
  --distpath .\ ^
  --log-level=DEBUG ^
  --workpath build\rFactoryModManager ^
  --add-data ModMaker.bat;.  ^
  --exclude-module dummyRF2 ^
  --exclude-module tabFavouriteServers ^
  --exclude-module tabGearshift ^
  --exclude-module tabGraphics ^
  --exclude-module tabJsonEditor ^
  --exclude-module tabOpponents ^
  --exclude-module tabServers ^
  --exclude-module tabSessions ^
  --exclude-module executeRF2 ^
  --paths env\Lib\site-packages ^
  --add-data resources\rfactory.ico;resources ^
  --add-data rFactoryModManagerFaq.txt;. ^
  --icon resources\rfactory.ico ^
  --debug=all ^
  "%~dp0\rFactoryModManager.py"
goto setVersion

:USESPEC
pyinstaller --debug all rFactoryModManager.spec 
copy /y dist\rFactoryModManager.exe

:setVersion
REM if exist rFactoryModManagerVersion.txt pyi-set_version rFactoryModManagerversion.txt rFactoryModManager.exe

pause
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts 	pip install -r requirements.txt


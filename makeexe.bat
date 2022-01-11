@echo off

call pyInstallerSetup env

::   --debug=imports 
::  --clean 
::  --paths env\Lib\site-packages 
::  --hidden-import pygame.base 

rem --icon doesn't seem to do anything
rem --noconsole removes the console in the background but for now
rem             it's best to keep it for error messages
pyinstaller ^
  --onefile ^
  --distpath . ^
  --log-level=DEBUG ^
  --paths rF2_serverNotify ^
  --paths env\lib\site-packages ^
  --hiddenimport rF2_joinServer ^
  --add-data resources\rfactory.ico;resources ^
  --add-data Faq.txt;. ^
  --icon resources\rfactory.ico ^
  "%~dp0\rFactory.py"
goto setVersion
:setVersion
if exist rFactoryVersion.txt pyi-set_version rFactoryVersion.txt rFactory.exe
pause
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts 	pip install -r requirements.txt


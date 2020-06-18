:@echo off
setlocal
@echo Freeze rFactoryModManager into a single .exe with pyInstaller

python -V | find "3.8"
if errorlevel 1 goto not38
echo pyinstaller only works with versions up to 3.8
pause
goto :eof

:not38
set path=c:\Python37;c:\Python37\scripts;%path%
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"


if exist env\scripts 	set path=%path%;env\Scripts
if not exist env\scripts	python.exe -m venv env && env/Scripts/activate && python -m pip install -r requirements.txt 

GOTO :USESPEC

::  --hiddenimport pkg_resources.py2_warn   Fixes ModuleNotFoundError: No module named 'pkg_resources.py2_warn'

REM Using the command line like this should also work but there were problems at some point.
pyinstaller ^
  --onefile ^
  --distpath .\ ^
  --log-level=WARN ^
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
  --hiddenimport pkg_resources.py2_warn ^
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


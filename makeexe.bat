@echo off
setlocal
@echo Freeze rFactory into a single .exe with pyInstaller

python -V | find "3.7"
if errorlevel 1 goto not37
echo pyinstaller only works with versions up to 3.6
pause
goto :eof

:not37
set path=c:\Python36;c:\Python36\scripts;%path%
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"


if exist env\scripts 	set path=%path%;env\Scripts
if not exist env\scripts	python.exe -m venv env && env/Scripts/activate && python -m pip install -r requirements.txt 

GOTO :USESPEC

REM Using the command line like this should also work but there were problems at some point.
pyinstaller ^
  --onefile ^
  --distpath .\ ^
  --log-level=DEBUG ^
  --paths ..\rF2_serverNotify ^
  --paths env\Lib\site-packages ^
  --hiddenimport rF2_joinServer ^
  "%~dp0\rFactory.py"

:USESPEC
pyinstaller --debug all rFactory.spec 

pause
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts 	pip install -r requirements.txt


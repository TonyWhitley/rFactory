::S@echo off
setlocal

python -V | find "3.7"
if errorlevel 1 goto not37
::python -V
echo pyinstaller only works with versions up to 3.6
pause
goto :eof

:not37
set path=c:\Python36;c:\Python36\scripts;%path%
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"


if exist env\scripts 	set path=%path%;env\Scripts
if not exist env\scripts	python.exe -m venv env && env/Scripts/activate && python -m pip install -r requirements.txt 

goto :useSpec

pyinstaller ^
  --onefile ^
  --distpath . ^
  --add-data CarDataFiles;.\CarDataFiles ^
  --add-data TrackDataFiles;.\TrackDataFiles ^
  --log-level=DEBUG ^
  --paths ..\rF2_serverNotify ^
  --hiddenimport rF2_joinServer ^
  "%~dp0\rFactory.py"

:useSpec
pyinstaller --debug all rFactory_data.spec 

pause
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts 	pip install -r requirements.txt


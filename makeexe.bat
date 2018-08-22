setlocal
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"

REM if exist env\scripts 	set path=%path%;env\Scripts
REM if not exist env\scripts	pip install -r requirements.txt

pyinstaller ^
  --onefile ^
  --distpath . ^
  "%~dp0\steps\rFactory.py"


pause

@echo off
cls
echo rFactor 2 ModMaker V1.5

setlocal

rem Default path, can be overridden in mod file
rem rf2dir=[path to rF2 install]
set rf2dir=c:\Program Files (x86)\Steam\steamapps\common\rFactor 2
set SteamCmd=%ProgramFiles(x86)%/Steam/steam.exe
set modfile=%1
if '%modfile%' == '' goto helpNoModfile
if not exist %modfile% goto helpNoModfile
echo Using %modfile%
REM set modfile=%cd%\%modfile%
set temporary_copy=%rf2dir%\UserData\temporary_copy
set verbose=0
set dryrun=0
rem Parse the modfile
for /f "eol=# tokens=1,2* delims==" %%i in (%modfile%) do (
 if /i '%%i' == 'Name' set modset=%%j
 if /i '%%i' == 'rf2dir' set rf2dir=%%j
 if /i '%%i' == 'SteamCmd' set SteamCmd=%%j
 if /i '%%i' == 'temporary_copy' set temporary_copy=%%j
 if /i '%%i' == 'verbose' set verbose=%%j
 if /i '%%i' == 'dryrun' set dryrun=%%j
 )
if %verbose% GTR 0 echo Full path: %modfile%

if '%modset%' == '' goto helpNoName

:::::::::::::::::::::::::::::::::::::::::::::::::
rem OK, ready to go
echo Name: %modset%
echo rf2dir: %rf2dir%
echo temporary_copy: %temporary_copy%
if %verbose% GTR 0 echo verbose: %verbose%
if %dryrun% GTR 0 echo dryrun ON
if %verbose% GTR 2 echo on
echo.

:::::::::::::::::::::::::::::::::::::::::::::::::
rem Check if Steam running
Set "MyProcess=Steam.exe"
tasklist /NH /FI "imagename eq %MyProcess%" 2>nul |find /i "%MyProcess%">nul
if not errorlevel 1 (
  Echo "%MyProcess%" is running
  goto :SteamRunning )

rem start it if not
echo Starting "%MyProcess%"
start "" /min "%SteamCmd%"
Set "MySubProcess=SteamService.exe"
:loop 
  timeout 1 > nul
  tasklist /NH /FI "imagename eq %MySubProcess%" 2>nul |find /i "%MySubProcess%">nul
  if errorlevel 1 goto loop
echo Steam takes some time to get going, allowing it to load...
timeout 15
echo "%MyProcess%" running

:SteamRunning
:::::::::::::::::::::::::::::::::::::::::::::::::

rem Create a folder for the mod

pushd "%rf2dir%"
md "%temporary_copy%\%modset%"
pushd "%temporary_copy%\%modset%"
set _modfolder=%cd%
echo Creating rFactor copy in %_modfolder%
echo.

:::::::::::::::::::::::::::::::::::::::::::::::::
rem Symlinks (actually "Junctions" which do not require admin rights)
rem back to the main install
for %%d in (Bin
Bin32
Bin64
Core
Launcher
LOG
Manifests
ModDev
PluginData
steamapps
steam_shader_cache
Support
Templates
Updates
UserData
_CommonRedist ) do if %verbose%==0 (
  mklink /j "%%d" "%rf2dir%\%%d" > nul
  ) else (
  mklink /j "%%d" "%rf2dir%\%%d"
  )

:::::::::::::::::::::::::::::::::::::::::::::::::
rem Symlinks to for the Installed folder, less Locations & Vehicles
md Installed
cd Installed
for %%d in (Commentary
HUD
Nations
rFm
Showroom
Sounds
Talent
UIData ) do if %verbose%==0 (
  mklink /j "%%d" "%rf2dir%\Installed\%%d" > nul
  ) else (
  mklink /j "%%d" "%rf2dir%\Installed\%%d"
  )
  
:::::::::::::::::::::::::::::::::::::::::::::::::
rem Symlinks to selected Locations & Vehicles
md Locations		
cd Locations		

rem Parse the modfile for Locations
for /f "eol=# tokens=1,2* delims==" %%i in (%modfile%) do if %verbose% GTR 1 (
  if /i '%%i' == 'Location' mklink /j "%%j" "%rf2dir%\Installed\Locations\%%j"
  ) else (
  if /i '%%i' == 'Location' mklink /j "%%j" "%rf2dir%\Installed\Locations\%%j" > nul
  if /i '%%i' == 'Location' echo Added Location %%j
  )
cd..

:::::::::::::::::::::::::::::::::::::::::::::::::
md Vehicles		
cd Vehicles		

rem Parse the modfile for Vehicles
for /f "eol=# tokens=1,2* delims==" %%i in (%modfile%) do if %verbose% GTR 1 (
  if /i '%%i' == 'Vehicle' mklink /j "%%j" "%rf2dir%\Installed\Vehicles\%%j"
  ) else (
  if /i '%%i' == 'Vehicle' mklink /j "%%j" "%rf2dir%\Installed\Vehicles\%%j" > nul
  if /i '%%i' == 'Vehicle' echo Added Vehicle %%j
  )

:::::::::::::::::::::::::::::::::::::::::::::::::
popd
echo.
@echo Starting rFactor 2 singleplayer...

if %dryrun%==0 (
  Bin64\rFactor2.exe  +singleplayer +path="%temporary_copy%\%modset%"
  ) else (
  echo      DRY RUN.  rFactor has now exited
  pause
  )

echo.
if %verbose% == 0 goto deleteCopy
  set /p _delete=Enter K if you want to KEEP the temporary rFactor copy "%modset%": 
  if /I '%_delete%' == 'k' goto :pauseExit

:deleteCopy
rmdir /s /q "%_modfolder%"
rem Delete the temporary_copy folder if there was nothing else in it.
rmdir %temporary_copy% > nul 2>&1
echo %_modfolder% deleted.

goto :eof
REM goto :pauseExit

:::::::::::::::::::::::::::::::::::::::::::::::::

:helpNoModfile
@echo off
echo Usage: %0 ^<Modfile^>

:helpNoName
@echo off
echo The Modfile must have
echo NAME=^<Name for the mod^> (preferably one word)
echo LOCATION=^<Track folder name^>
echo repeat as required
echo VEHICLE=^<Vehicle folder name^>
echo repeat as required
echo.
echo For example
echo name=1960s_F1_UK
echo Location=CRYSTAL PALACE 1969
echo Location=Silverstone90s
echo Location=BrandsHatch
echo etc.
echo Vehicle=Brabham_1966
echo Vehicle=Ferrari_312_67
echo Vehicle=Historic Challenge_EVE_1968
echo.
echo Anything on a line after # is a comment
echo.
echo If your rFactor is installed somewhere other than
echo c:\Program Files (x86)\Steam\steamapps\common\rFactor 2
echo then you can add a line like this
echo rf2dir=c:\Program Files (x86)\Steam\steamapps\common\rFactor 2
echo.
echo Similarly for the command to start Steam
echo SteamCmd=c:\Program Files (x86)\Steam\Steam
:pauseExit
pause



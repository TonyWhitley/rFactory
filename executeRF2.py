"""
The user has selected their options, collect them, edit rF2's data files
as required and then call rF2 with any command switches.
"""
import os
import subprocess
import sys

from data.rFactoryData import getAllCarData, getAllTrackData, getSingleCarData, getSingleTrackData
from edit.editRF2files import changeCar, changeTrack, changeOpponents
from data.rFactoryConfig import SteamExe, SteamDelayS, rF2root, DiscordCmd
from data.rFactoryConfig import CrewChiefCmd, VolumeControlExe, TeamSpeakExe
from data.rFactoryConfig import MyPreCommand, MyPostCommand

if getattr( sys, 'frozen', False ) :
  # running in a PyInstaller bundle (exe)
  rF2_serverNotify_path = r'rF2_serverNotify\steps'
else :
  # running live
  rF2_serverNotify_path = r'rF2_serverNotify\steps'
sys.path.append(rF2_serverNotify_path)
from rF2_joinServer import runRf2Online
import dummyRF2
import steam

settingsExample = [
    ['Car', ['COPERSUCAR', 'COPERSUCAR', '', '', 2, 'RWD', 1975, '1970-', '***', '1975COPERSUCAR']],
    ['Track', ['Oulton_Park_Circuit_2015']],
    ['Opponents', ['Opponents']],
    ['Graphics', ['Graphics']],
    ['Sessions', ['Sessions']],
    ['Options', ['Options']],
    ['Server', ['Server', 'password']],
    ['Scenarios', ['Scenario - what does that mean? Scenario sets all tab settings']]
  ]


settingsExample = [
    ['Car', ['134 JUDD', '134 JUDD', '', 'PortoAlto and rstRmo', 2, 'RWD', '', '', '***', '134_JUDD']],
    ['Track', ['Oulton_Park_Circuit_2015']],
    ['Opponents', ['Opponents']],
    ['Graphics', ['Graphics']],
    ['Sessions', ['Sessions']],
    ['Options', ['Options']],
    ['Server', ['Server', 'password']],
    ['Scenarios', ['Scenario - what does that mean? Scenario sets all tab settings']]
  ]

def runRF2(online='Offline', settings=None, _password=None):
  _status = 'OK'
  if online == 'Offline':
    _status = editRF2Files(settings)
    if _status != 'OK':
      return _status

  _dummy = False
  try:
    if settings['Options']['DummyRF2'] != '0':
      _dummy = True
  except:
    pass # DummyRF2 is not in Options

  if not _dummy or settings['Options']['RunCoPrograms'] != '0':
    _status = runCoProgram(settings, 'CrewChief', CrewChiefCmd)
    if _status == 'OK':
      _status = runCoProgram(settings, 'Discord', DiscordCmd)
    if _status == 'OK':
      _status = runCoProgram(settings, 'MyPreCommand', MyPreCommand)
    if _status == 'OK':
      _status = runCoProgram(settings, 'VolumeControl', VolumeControlExe)
    if _status == 'OK':
      _status = runCoProgram(settings, 'TeamSpeak', TeamSpeakExe)

  if _status == 'OK':
    if _dummy:
      _status = dummyRF2.dummyRF2(online, settings, _password)
    elif online == 'Offline':
      _status = runOffline(settings)
    elif online == 'Online':
      _status = runOnline(settings, _password)
    else:
      return ('settings error', settings)
    if _status == 'OK':
      if not _dummy or settings['Options']['RunCoPrograms'] != '0':
        _status = runCoProgram(settings, 'MyPostCommand', MyPostCommand)
  return _status

def editRF2Files(settings):
  # Car
  _carID = settings['Car'][-1]
  _carData = getSingleCarData(_carID, ['originalFolder', 'vehFile'])
  _status = changeCar(vehPath=_carData['originalFolder'], vehName=_carData['vehFile'])
  if _status != 'OK':
    return _status

  # Track
  _trackID = settings['Track'][-1]
  _trackData = getSingleTrackData(_trackID, ['originalFolder', 'Scene Description', 'Scene Description'])
  _status = changeTrack(scnPath=_trackData['originalFolder'], scnName=_trackData['Scene Description'], SceneDescription=_trackData['Scene Description'])
  if _status != 'OK':
    return _status

  if 0: # not working
    # Opponents
    _opponentIDs = settings['Opponents']
    _opponents = []
    for _opponent in _opponentIDs:
      _opponents.append(_opponent[-1])  # NO, it's not the DB file ID, see AllClasses.txt (NO SUCH FILE???) - another field we have to sort out
    _opponentStr= '|' + '|'.join(_opponents)
    #  Need to work out the field for this     _status = changeOpponents(opponents=_opponentStr)
    if _status != 'OK':
      return _status
  return 'OK'

def runCoProgram(settings, coProgramName, coProgramCmd):
  try:
    if settings['Options'][coProgramName] != '0':
      if len(coProgramCmd):
        try:
          subprocess.Popen(coProgramCmd)
        except:
          try:  # again as a shell command
            subprocess.Popen(coProgramCmd, shell=True)
          except:
            return "Couldn't execute '%s'" % coProgramCmd
    return 'OK'
  except:
    return "Failure with co-program '%s'" % coProgramName

def runOffline(settings):
  cmd = SteamExe
  _cmd =  '"%s" -applaunch 365960 +singleplayer +path=".."' % (SteamExe)
  # Alternative looks to be
  # "%ProgramFiles(x86)%\Steam\steamapps\common\rFactor 2\Bin64\rFactor2.exe"
  _pop = os.getcwd()  # save current directory
  os.chdir(rF2root)
  _cmd = '"%s/Bin64/rFactor2.exe" +path="."' % rF2root
  # +profile="rFactory"
  _cmd = os.path.normpath(_cmd) # change any / to \
  print(_cmd)
  # Steam must be running
  steam.runSteamMinimised(SteamExe, SteamDelayS)
  # TBD: Need to wait for Steam to run
  subprocess.call(_cmd)
  os.chdir(_pop)
  return 'OK'

def runOnline(settings, _password):
  _pop = os.getcwd()  # save current directory
  # Steam must be running
  steam.runSteamMinimised(SteamExe, SteamDelayS)
  # Use rF2_joinServer to execute (requires that it is refactored)
  server = settings['Favourite Servers'] #['Server']
  #password = settings['Favourite Servers']['Password']
  _status = runRf2Online(SteamExe, server, _password)
  os.chdir(_pop)
  return _status

if __name__ == '__main__':
  for row in settingsExample:
    print(row[0], row[1])

  runRF2('Offline', settingsExample)
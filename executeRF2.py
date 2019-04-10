"""
The user has selected their options, collect them, edit rF2's data files
as required and then call rF2 with any command switches.
"""
import os
import subprocess
import sys

from data.rFactoryData import getAllCarData, getAllTrackData, getSingleCarData, getSingleTrackData
from edit.editRF2files import changeCar, changeTrack, changeOpponents
from data.rFactoryConfig import SteamExe, SteamDelayS, rF2root
rF2_serverNotify_path = r'..\rF2_serverNotify\steps'
if os.path.exists(rF2_serverNotify_path):
  sys.path.append(rF2_serverNotify_path)
  from rF2_joinServer import runRf2Online
import dummyRF2
import steam

settingsExample = [
    ['Car', ['COPERSUCAR', 'COPERSUCAR', '', '', 2, 'RWD', 1975, '1970-', '***', '1975COPERSUCAR']],
    ['Track', ['Oulton_Park_Circuit_2015']],
    ['Opponents', ['Opponents']],
    ['Conditions', ['Conditions']],
    ['Sessions', ['Sessions']],
    ['Options', ['Options']],
    ['Server', ['Server', 'password']],
    ['Scenarios', ['Scenario - what does that mean? Scenario sets all tab settings']]
  ]


settingsExample = [
    ['Car', ['134 JUDD', '134 JUDD', '', 'PortoAlto and rstRmo', 2, 'RWD', '', '', '***', '134_JUDD']],
    ['Track', ['Oulton_Park_Circuit_2015']],
    ['Opponents', ['Opponents']],
    ['Conditions', ['Conditions']],
    ['Sessions', ['Sessions']],
    ['Options', ['Options']],
    ['Server', ['Server', 'password']],
    ['Scenarios', ['Scenario - what does that mean? Scenario sets all tab settings']]
  ]

def runRF2(online='Offline', settings=None, _password=None):
  if online == 'Offline':
    _status = editRF2Files(settings)
    if _status != 'OK':
      return _status
  try:
    if settings['Options']['DummyRF2'] != '0':
      _status = dummyRF2.dummyRF2(online, settings, _password)
      return _status
  except:
    pass # DummyRF2 is not in Options
  if online == 'Offline':
    _status = runOffline(settings)
  elif online == 'Online':
    _status = runOnline(settings, _password)
  else:
    return ('settings error', settings)
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
  runRf2Online(SteamExe, server, _password)
  os.chdir(_pop)
  return 'OK'

if __name__ == '__main__':
  for row in settingsExample:
    print(row[0], row[1])

  runRF2('Offline', settingsExample)
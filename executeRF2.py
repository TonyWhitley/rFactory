"""
The user has selected their options, collect them, edit rF2's data files
as required and then call rF2 with any command switches.
"""
import os
import subprocess

from data.rFactoryData import getAllCarData, getAllTrackData, getSingleCarData, getSingleTrackData
from edit.editRF2files import changeCar, changeTrack, changeOpponents
from data.rFactoryConfig import SteamExe, rF2root

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

def runRF2(online='Offline', settings=None):
  if online == 'Offline':
    runOffline(settings)
  elif online == 'Online':
    runOnline(settings)
  else:
    print('settings error', settings)

def runOffline(settings):
  # Car
  _carID = settings['Car'][-1]
  _carData = getSingleCarData(_carID, ['originalFolder', 'vehFile'])
  changeCar(vehPath=_carData['originalFolder'], vehName=_carData['vehFile'])

  # Track
  _trackID = settings['Track'][-1]
  _trackData = getSingleTrackData(_trackID, ['originalFolder', 'Scene Description', 'Scene Description'])
  changeTrack(scnPath=_trackData['originalFolder'], scnName=_trackData['Scene Description'], SceneDescription=_trackData['Scene Description'])

  if 0: # not working 
    # Opponents
    _opponentIDs = settings['Opponents']
    _opponents = []
    for _opponent in _opponentIDs:
      _opponents.append(_opponent[-1])  # NO, it's not the DB file ID, see AllClasses.txt (NO SUCH FILE???) - another field we have to sort out
    _opponentStr= '|' + '|'.join(_opponents)
    #  Need to work out the field for this     changeOpponents(opponents=_opponentStr)

  cmd = SteamExe
  _cmd =  '"%s" -applaunch 365960 +singleplayer +path=".."' % (SteamExe)
  # Alternative looks to be
  # "%ProgramFiles(x86)%\Steam\steamapps\common\rFactor 2\Bin64\rFactor2.exe"
  os.chdir(rF2root)
  _cmd = '"%s/Bin64/rFactor2.exe" +path="."' % rF2root
  # +profile="rFactory"
  _cmd = os.path.normpath(_cmd) # change any / to \
  print(_cmd)
  subprocess.call(_cmd)

def runOnline(settings):
  #  _cmd =  '"%s" -applaunch 365960 +autojoin="%s" +connect=:%s@%s:%s +multiplayer +path=".."' % (configFileO.SteamExe, configFileO.server, configFileO.
  pass

if __name__ == '__main__':
  for row in settingsExample:
    print(row[0], row[1])

  runRF2('Offline', settingsExample)
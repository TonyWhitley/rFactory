"""
The user has selected their options, collect them, edit rF2's data files
as required and then call rF2 with any command switches.
"""
import os
import subprocess

from data import getCarData, getTrackData
from editRF2files import changeCar, changeTrack
from rFactoryConfig import SteamExe, rF2root

settingsExample = [
    ['Car', ['COPERSUCAR', 'COPERSUCAR', '', '', 2, 'RWD', 1975, '1970-', '***', '1975COPERSUCAR']],
    ['Track', ['Track details']],
    ['Opponents', ['Opponents']],
    ['Conditions', ['Conditions']],
    ['Sessions', ['Sessions']],
    ['Options', ['Options']],
    ['Server', ['Server', 'password']],
    ['Scenarios', ['Scenario - what does that mean? Scenario sets all tab settings']]
  ]



def runRF2(online, settings):
  if online == 'Offline':
    runOffline(settings)
  elif online == 'Online':
    runOnline(settings)
  else:
    print('settings error', settings)

def runOffline(settings):
  d = getCarData(['DB file (hidden)', 'originalFolder', 'vehFile', 'Name'], maxWidth=100)
  for row in d:
    if row[0] == settings[0][1][9]:
      _vehFile = os.path.join(rF2root, row[1],row[2]+'.veh')
      changeCar(veh=_vehFile)
      cmd = SteamExe
      _cmd =  '"%s" -applaunch 365960 +singleplayer +path=".."' % (SteamExe)
      # Alternative looks to be
      # "C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Bin64\rFactor2.exe"
      subprocess.call(_cmd)

def runOnline(settings):
  #  _cmd =  '"%s" -applaunch 365960 +autojoin="%s" +connect=:%s@%s:%s +multiplayer +path=".."' % (configFileO.SteamExe, configFileO.server, configFileO.
  pass

if __name__ == '__main__':
  for row in settingsExample:
    print(row[0], row[1])

  runRF2('Offline', settingsExample)
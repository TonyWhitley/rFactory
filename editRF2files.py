"""
Read, __edit and then write rF2 files like UserData\player\All Tracks & Cars.cch
and UserData\player\Player.JSON
"""
import os
import re

from trawl_rF2_datafiles import getListOfFiles, readFile
from rFactoryConfig import rF2root
from data import getSingleCarData

def changeCar(vehPath = r'Norma_M30-LMP3_2017\1.51', vehName='NORMAM30_08'):
  if vehName == '':
    print('Veh name not in car data file')
    return
  _vehFile = os.path.join(rF2root, vehPath, vehName+'.veh').replace('\\', '\\\\\\\\')

  allTracks = os.path.join(rF2root, r'UserData\player\All Tracks & Cars.cch')
  _text3 = readFile(allTracks)
  _edit3 = [r'( *SinglePlayerVehicle *=).*',   r'\1"' + _vehFile+'"']
  _edited = __edit(_text3, [_edit3], doubleSlash=False)
  writeFile(allTracks, _edited)

def changeTrack(scnPath = r'F1_1988_Tracks\0.941', scnName='HOCKENHEIM_1988_C4', SceneDescription='HOCKENHEIM_1988_C4'):
  if scnName == '':
    print('Scene Description not in track data file')
    return
  _scnFile = os.path.join(rF2root, scnPath, scnName+'.scn').replace('\\', '\\\\\\\\')

  PlayerJSON = os.path.join(rF2root, r'UserData\player\Player.JSON')
  _text4 = readFile(PlayerJSON)
  _edit4 = [r'( *"Scene File" *:).*',   '\\1"' + _scnFile+'",']
  _edit5 = [r'( *"AI Database File" *:).*',   r'\1"",']  #blank it
  _edit6 = [r'( *"Scene Description" *:).*',   r'\1"%s",' % SceneDescription]
  _edit7 = [r'( *"Scene Signature" *:).*',   r'\1""']  #blank it  NOTE NO COMMA
  _edited = __edit(_text4, [_edit4,_edit5,_edit6,_edit7], doubleSlash=True)  
  writeFile(PlayerJSON, _edited)

def changeOpponents(opponents="|1971|AC_427_1954_Endurance|DPi"):
  allTracks = os.path.join(rF2root, r'UserData\player\All Tracks & Cars.cch')
  _text3 = readFile(allTracks)
  _edit3 = [r'( *SinglePlayerFilter *=).*',   r'\1"' + opponents+'"']
  _edited = __edit(_text3, [_edit3], doubleSlash=False)
  writeFile(allTracks, _edited)

def writeFile(_filepath, text):
  with open(_filepath, "w") as f:
    f.writelines(text)


def __edit(text, edits, doubleSlash):
  """
  edits is a list of regex pairs to substitute 
  """
  for __edit in edits:
    _outText = []
    for line in text:
      if re.search(__edit[0], line, re.IGNORECASE):
        _newLine = re.sub(__edit[0], __edit[1], line, re.IGNORECASE)
        # \rfactor in the substitute string gets escaped to \\rfactor
        # fix that by replacing \\ with \  
        # If the string is using \\ replace \\\\ with \\
        if doubleSlash:
          _outText.append(_newLine.replace(r'\\\\', r'\\'))
        else:
          _outText.append(_newLine.replace(r'\\', '\\'))
      else:
        _outText.append(line)
    text = list(_outText)
  return text

if __name__ == '__main__':

  _text1 = '"AI Database File":"C:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\Installed\\Locations\\Road America 2016\\1.4\\RA2016.AIW",\n'
  _edit1 = [r'( *"AI Database File" *:).*',   r'\1"FRED"']
  _edited = __edit([_text1], [_edit1], doubleSlash=True)
  assert _edited[0] == '"AI Database File":"FRED"\n'

  _text2 = 'SinglePlayerVehicle="C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\Porsche_991RSR_GTE_2017\1.49\991RSR_911.VEH"\n'
  _edit2 = [r'( *SinglePlayerVehicle *=).*',   r'\1"\\rF2\CHARLIE"']

  _edited = __edit([_text1, _text2], [_edit1, _edit2], doubleSlash=False)
  assert _edited[0] == '"AI Database File":"FRED"\n'
  assert _edited[1] == 'SinglePlayerVehicle="\\rF2\\CHARLIE"\n'

  allTracks = os.path.join(rF2root, r'UserData\player\All Tracks & Cars.cch')
  _text3 = readFile(allTracks)
  # NOTE THE \\ BEFORE rFactor
  _edit3 = [r'( *SinglePlayerVehicle *=).*',   r'\1"' + 
            os.path.join(rF2root, r'Installed\Vehicles\Oreca_07_LMP2_2017\1.41\ORECA07PREE6ED8B36.VEH"').replace('\\', '\\\\')]
  _edit3 = [r'( *SinglePlayerVehicle *=).*',   r'\1"' + 
            os.path.join(rF2root, r'Installed\Vehicles\Norma_M30-LMP3_2017\1.51\NORMAM30_08.VEH"').replace('\\', '\\\\')]
  
  #_edit3 = [r'( *SinglePlayerVehicle *=).*',   r'\1' '"C:\Program Files (x86)\Steam\steamapps\common\\rFactor 2\Installed\Vehicles\Oreca_07_LMP2_2017\1.41\ORECA07PREE6ED8B36.VEH"']
  _edited = __edit(_text3, [_edit3], doubleSlash=False)
  writeFile(allTracks, _edited)

  PlayerJSON = os.path.join(rF2root, r'UserData\player\Player.JSON')
  _text4 = readFile(PlayerJSON)
  # NOTE THE \\ BEFORE rFactor
  doubleSlashed_rF2root = r'C:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2'
  _edit4 = [r'( *"Scene File" *:).*',   '\\1"' + 
            os.path.join(rF2root, r'Installed\Locations\F1_1988_Tracks\0.941\HOCKENHEIM_1988_C4.SCN",').replace('\\', '\\\\\\\\')]
  #_edit4 = [r'( *"Scene File" *:).*',   '\\1"' + 
  #          os.path.join(rF2root, r'Installed\Locations\OULTON_PARK_CIRCUIT_2015\1.25\OULTONPARK_INT.SCN",').replace('\\', '\\\\\\\\')]

  #_edit4 = [r'( *"Scene File" *:).*',   r'\1"C:\\\\Program Files (x86)\\\\Steam\\\\steamapps\\\\common\\\\rFactor 2\\\\Installed\\\\Locations\\\\F1_1988_Tracks\\\\0.941\\\\HOCKENHEIM_1988_C4.SCN",']
  _edit5 = [r'( *"AI Database File" *:).*',   r'\1"",']  #blank it
  _edit6 = [r'( *"Scene Description" *:).*',   r'\1"HOCKENHEIM_1988_C4",']
  _edit6 = [r'( *"Scene Description" *:).*',   r'\1"OULTONPARK_INT",']
  _edit7 = [r'( *"Scene Signature" *:).*',   r'\1""']  #blank it  NOTE NO COMMA
  _edited = __edit(_text4, [_edit4,_edit5,_edit6,_edit7], doubleSlash=True)
  writeFile(PlayerJSON, _edited)

  changeCar(vehPath = r'Installed\Locations\Oreca_07_LMP2_2017\1.41', vehName='ORECA07PREE6ED8B36')
  changeTrack(scnPath = r'Installed\Locations\OULTON_PARK_CIRCUIT_2015\1.25', scnName='OULTONPARK_INT', SceneDescription=r'OULTONPARK_INT')

  changeCar(vehPath = r'Installed\Locations\Norma_M30-LMP3_2017\1.51', vehName='NORMAM30_08')
  changeTrack(scnPath = r'Installed\Locations\F1_1988_Tracks\0.941', scnName='HOCKENHEIM_1988_C4', SceneDescription=r'HOCKENHEIM_1988_C4')
  
  vehBits = getSingleCarData(Oreca_07_LMP2_2017, ['originalFolder', 'vehFile', 'Name'])
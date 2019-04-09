""" 
All the configuration items for rFactory.
Some can be edited to change how rFactory works, e.g. the car table columns.

"""
import json
import os

from data.utils import readFile, writeFile

# General items

# Tags used by rFactory. Only some are present in rFactor files, 
# the rest are all included but may be blank
carTags = ['Manufacturer', 'Model', 'Class', 'tType', 'F/R/4WD', 
           'Year', 'Decade', 'Rating', 'DB file ID', 'Gearshift', 'Aids',
           'AIstrengthFactor', 'GraphicDetailsFactor', 'originalFolder', 'vehFile',
           # The standard ones we include:
           'Name','Version','Type','Author','Origin','Category',
           'ID','URL','Desc','Date','Flags','RefCount','MinVersion']
# Omit 'Signature','MASFile','BaseSignature'

trackTags = ['Track Name', 'Continent', 'Country', 'tType',
             'Year', 'Decade', 'Rating', 'DB file ID', 
             'AIstrengthFactor', 'GraphicDetailsFactor', 'originalFolder', 'Scene Description',
             # The standard ones we include:
             'Name','Version','Type','Author','Origin','Category',
             'ID','URL','Desc','Date','Flags','RefCount','MinVersion']

serverTags = ['Server name', 'Track Name', 'Players', 'Password', 'Version']

CarDatafilesFolder = 'CarDatafiles'
TrackDatafilesFolder = 'TrackDatafiles'
dataFilesExtension = '.rFactory.txt'

# File-specific items
config_tabCar = {
  'carColumns' : ['Manufacturer', 'Model', 'Class', 'Author', 'tType', 'Date',
                  'F/R/4WD', 'Year', 'Decade', 'Rating', 'DB file ID'],
  'carFilters' : ['Manufacturer', 'Model', 'Class', 'Author', 'tType',  'Date',
                  'F/R/4WD', 'Year', 'Decade', 'Rating']
  }

config_tabTrack = {
  'trackColumns' : ['Track Name', 'Version', 'Continent', 'Country', 'Author', 'tType',  'Date',
                  'Year', 'Decade', 'Rating', 'Scene Description','DB file ID'],
  'trackFilters' : ['Author', 'Continent', 'Country', 'tType','Year', 'Decade', 'Rating','Scene Description','Date']
  }

config_tabServer = {
  'serverColumns' : ['Favourite', 'Server Name', 'Track Name', 'Humans', 'Maybe', 'AI', 'Max', 'Password', 'Version', 'blank'],
  'serverFilters' : ['Favourite', 'Server Name', 'Track Name', 'Humans', 'Maybe', 'AI', 'Password', 'Version']
  }

scenarioFilesFolder = 'scenarioFiles' 
scenarioFilesExtension = '.rFactoryScenarioJSON'

favouriteServersFilesFolder = 'favourites'
favouriteServersFilesExtension = '.JSON'

rFactoryConfigFileFolder = 'favourites'
rFactoryConfigFileExtension = '.JSON'

# Editable items in config file
filename =  os.path.join(rFactoryConfigFileFolder, 'rFactoryConfig'+rFactoryConfigFileExtension)

_text = readFile(filename)
if len(_text):
  config = json.loads(''.join(_text))
else: # No rFactoryConfig file, create one
  config = {
    # rF2 items
    'rF2root' : '%ProgramFiles(x86)%/Steam/steamapps/common/rFactor 2',
    'SteamExe' : "%ProgramFiles(x86)%/Steam/steam.exe",
    'SteamDelaySeconds' : 10,  
    '#SteamDelaySeconds How long it takes Steam to start up before we can start rF2' : "",
    'UserData player' : 'player'
    }
  _text = json.dumps(config, sort_keys=True, indent=4)
  writeFile(filename, _text)
# rF2 items
rF2root = os.path.expandvars(config['rF2root'])
SteamExe = os.path.expandvars(config['SteamExe'])
SteamDelayS = config['SteamDelaySeconds']  # How long it takes Steam to start up
player = config['UserData player']
playerPath = os.path.join(rF2root, 'UserData', player)
pass


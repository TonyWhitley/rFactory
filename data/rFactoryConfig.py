"""
All the configuration items for rFactory.
Some can be edited to change how rFactory works, e.g. the car table columns.

"""
import json
import os

from data.utils import readFile, writeFile

def getKey(filename, keyname):
    """ Error trap when reading config file keys """
    try:
        return config[keyname]
    except Exception as e:
        print('Config file "%s" has no entry for "%s"' % (filename, e.args[0]))
        return '"No such key %s"' % e.args[0]

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

CarDatafilesFolder = 'Datafiles/Cars'
TrackDatafilesFolder = 'Datafiles/Tracks'
dataFilesExtension = '.rFactory.txt'
markerfileExtension = '.folder.SCNs.scanned'

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

scenarioFilesFolder = 'Datafiles/scenarioFiles'
scenarioFilesExtension = '.rFactoryScenarioJSON'

favouriteServersFilesFolder = 'Datafiles/favourites'
favouriteServersFilesExtension = '.JSON'

rFactoryConfigFileFolder = 'Datafiles/favourites'
rFactoryConfigFileExtension = '.JSON'

# Editable items in config file
filename =  os.path.join(rFactoryConfigFileFolder, 'rFactoryConfig'+rFactoryConfigFileExtension)

_text = readFile(filename)
try:
  config = json.loads(''.join(_text))
except: # No rFactoryConfig file, create one
  config = {
    # rF2 items
    '# %ProgramFiles(x86)% will be expanded to your Windows setting but you can write it explicitly if you want' : "",
    '# Same for %LOCALAPPDATA%' : "",
    '# Use / not backslash' : "",
    'rF2root' : '%ProgramFiles(x86)%/Steam/steamapps/common/rFactor 2',
    'SteamExe' : "%ProgramFiles(x86)%/Steam/steam.exe",
    'SteamDelaySeconds' : 10,
    '#SteamDelaySeconds: How long it takes Steam to start up before we can start rF2' : "",
    #'DiscordExe' : '"%APPDATA%/Microsoft/Windows/Start Menu/Programs/Discord Inc/Discord.lnk"',
    #'#DiscordExe: had to use short cut as the command wouldn\'t work' : '',
    'DiscordExe' : '%LOCALAPPDATA%/Discord/Update.exe',
    'DiscordArgs' : '--processStart Discord.exe',
    'CrewChiefExe' : '"%ProgramFiles(x86)%/Britton IT Ltd/CrewChiefV4/CrewChiefV4.exe"',
    'CrewChiefArgs' : 'RF2_64BIT',
    'VolumeControlExe' : '"%ProgramFiles(x86)%/VolumeControl/VolumeControl.exe"',
    'TeamSpeakExe' : '"%ProgramFiles(x86)%/TeamSpeak 3 Client/ts3client_win64.exe"',
    '#MyPreCommand: use this call a program or batch file before rF2 runs' : "",
    'MyPreCommand' : '',
    'MyPreCommandArgs' : '',
    '#MyPostCommand: use this call a program or batch file after rF2 runs' : "",
    'MyPostCommand' : '',
    'MyPostCommandArgs' : '',
    'UserData player' : 'player'
    }
  _text = json.dumps(config, sort_keys=True, indent=4)
  writeFile(filename, _text)
# rF2 items
rF2root = os.path.normpath(os.path.expandvars(getKey(filename, 'rF2root')))
SteamExe = os.path.normpath(os.path.expandvars(getKey(filename, 'SteamExe')))
DiscordExe = os.path.normpath(os.path.expandvars(getKey(filename, 'DiscordExe'))) + ' ' + getKey(filename, 'DiscordArgs')
CrewChiefExe = os.path.normpath(os.path.expandvars(getKey(filename, 'CrewChiefExe'))) + ' ' + getKey(filename, 'CrewChiefArgs')
VolumeControlExe = os.path.normpath(os.path.expandvars(getKey(filename, 'VolumeControlExe')))
TeamSpeakExe = os.path.normpath(os.path.expandvars(getKey(filename, 'TeamSpeakExe')))
if len(getKey(filename, 'MyPreCommand')):
    MyPreCommand = os.path.normpath(os.path.expandvars(getKey(filename, 'MyPreCommand'))) + ' ' + getKey(filename, 'MyPreCommandArgs')
else:
    MyPreCommand = ''
if len(getKey(filename, 'MyPostCommand')):
    MyPostCommand = os.path.normpath(os.path.expandvars(getKey(filename, 'MyPostCommand'))) + ' ' + getKey(filename, 'MyPostCommandArgs')
else:
    MyPostCommand = ''

SteamDelayS = getKey(filename, 'SteamDelaySeconds')  # How long it takes Steam to start up

player = getKey(filename, 'UserData player')
playerPath = os.path.join(rF2root, 'UserData', player)

"""
All the configuration items for rFactory.
Some can be edited to change how rFactory works, e.g. the car table columns.

"""
import json
import os

from data.utils import readFile, writeFile

def getKey(config_filename, keyname):
    """ Error trap when reading config file keys """
    try:
        return config[keyname]
    except Exception as e:
        print('Config file "%s" has no entry for "%s"' % (config_filename, e.args[0]))
        return '"No such key %s"' % e.args[0]

# General items

# Tags used by rFactory. Only some are present in rFactor files,
# the rest are all included but may be blank
carTags = ['Manufacturer', 'Model', 'Class', 'tType', 'F/R/4WD',
           'Year', 'Decade', 'Rating', 'DB file ID', 'Gearshift', 'Aids',
           'AIstrengthFactor', 'GraphicDetailsFactor', 'originalFolder', 'vehFile',
           'Aero', 'Turbo', 'Mass',
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
carCacheDataFile = 'Datafiles/rFactoryCarCache.csv'
trackCacheDataFile = 'Datafiles/rFactoryTrackCache.csv'
modMakerFilesFolder = 'Datafiles/ModMaker'
modMakerFilesExtension = 'ModMaker.txt'

# File-specific items
config_tabCar = {
  'carColumns' : ['Manufacturer', 'Model', 'Class', 'Author', 'tType', 'Date',
                  'F/R/4WD', 'Aero', 'Turbo', 'Mass', 'Year', 'Decade', 'Rating', 'DB file ID'],
  'carFilters' : ['Manufacturer', 'Model', 'Class', 'Author', 'tType',  'Date',
                  'F/R/4WD', 'Aero', 'Turbo', 'Year', 'Decade', 'Rating']
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
config_filename =  os.path.join(rFactoryConfigFileFolder, 'rFactoryConfig'+rFactoryConfigFileExtension)

_text, error = readFile(config_filename)
try:
  config = json.loads(''.join(_text))
except: # No rFactoryConfig file, create one
  config = new_config_file()

# rF2 items
rF2root = os.path.normpath(os.path.expandvars(getKey(config_filename, 'rF2root')))
SteamExe = os.path.normpath(os.path.expandvars(getKey(config_filename, 'SteamExe')))
DiscordExe = os.path.normpath(os.path.expandvars(getKey(config_filename, 'DiscordExe')))
DiscordCmd = DiscordExe + ' ' + getKey(config_filename, 'DiscordArgs')
CrewChiefExe = os.path.normpath(os.path.expandvars(getKey(config_filename, 'CrewChiefExe')))
CrewChiefCmd = CrewChiefExe + ' ' + getKey(config_filename, 'CrewChiefArgs')
VolumeControlExe = os.path.normpath(os.path.expandvars(getKey(config_filename, 'VolumeControlExe')))
TeamSpeakExe = os.path.normpath(os.path.expandvars(getKey(config_filename, 'TeamSpeakExe')))
if len(getKey(config_filename, 'MyPreCommand')):
    MyPreCommand = os.path.normpath(os.path.expandvars(getKey(config_filename, 'MyPreCommand'))) + ' ' + getKey(config_filename, 'MyPreCommandArgs')
else:
    MyPreCommand = ''
if len(getKey(config_filename, 'MyPostCommand')):
    MyPostCommand = os.path.normpath(os.path.expandvars(getKey(config_filename, 'MyPostCommand'))) + ' ' + getKey(config_filename, 'MyPostCommandArgs')
else:
    MyPostCommand = ''

SteamDelayS = getKey(config_filename, 'SteamDelaySeconds')  # How long it takes Steam to start up

player = getKey(config_filename, 'UserData player')
playerPath = os.path.join(rF2root, 'UserData', player)

def validate():
    """
    Check that the paths have the expected files. Some are optional
    """
    paths = dict()
    paths['rF2root'] = os.path.isdir(rF2root)
    paths['SteamExe'] = os.path.isfile(SteamExe)
    paths['DiscordExe'] = os.path.isfile(DiscordExe)
    paths['CrewChiefExe'] = os.path.isfile(CrewChiefExe)
    paths['VolumeControlExe'] = os.path.isfile(VolumeControlExe)
    paths['TeamSpeakExe'] = os.path.isfile(TeamSpeakExe)

    paths['playerPath'] = os.path.isdir(playerPath)
    # Check rF2 install a little further
    _vehicles = os.path.join(rF2root, 'Installed', 'Vehicles')
    paths['vehicles'] = os.path.isdir(_vehicles)

    return paths

def new_config_file():
  """ Make sure we have a fresh config by deleting any existing one """
  os.remove(config_filename)
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
    'CrewChiefExe' : "%ProgramFiles(x86)%/Britton IT Ltd/CrewChiefV4/CrewChiefV4.exe",
    'CrewChiefArgs' : 'RF2_64BIT',
    'VolumeControlExe' : "%ProgramFiles(x86)%/VolumeControl/VolumeControl.exe",
    'TeamSpeakExe' : "%ProgramFiles(x86)%/TeamSpeak 3 Client/ts3client_win64.exe",
    '#MyPreCommand: use this call a program or batch file before rF2 runs' : "",
    'MyPreCommand' : '',
    'MyPreCommandArgs' : '',
    '#MyPostCommand: use this call a program or batch file after rF2 runs' : "",
    'MyPostCommand' : '',
    'MyPostCommandArgs' : '',
    'UserData player' : 'player'
    }
  _text = json.dumps(config, sort_keys=True, indent=4)
  writeFile(config_filename, _text)
  return config

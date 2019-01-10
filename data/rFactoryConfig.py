""" 
All the configuration items for rFactory.
Some can be edited to change how rFactory works, e.g. the car table columns.

"""
import os

# rF2 items
rF2root = r'C:\Program Files (x86)\Steam\steamapps\common\rFactor 2'
SteamExe = "C:/Program Files (x86)/Steam/steam.exe"
player = 'player'
playerPath = os.path.join(rF2root, 'UserData', player)

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

""" 
All the configuration items for rFactory.
Some can be edited to change how rFactory works, e.g. the car table columns.

"""

# General items

# Tags used by rFactory. Only some are present in rFactor files, the rest are all included but are blank
carTags = ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 
           'Year', 'Decade', 'Rating', 'DB file (hidden)', 'Gearshift', 'Aids',
           'Name','Version','Type','Origin','Category','ID','URL','Desc',
           'Date','Flags','RefCount','MinVersion', 'originalFolder']
trackTags = ['Track Name', 'Continent', 'Country', 'Author', 'Type',
             'Year', 'Decade', 'Rating', 'DB file (hidden)', 
             'Name','Version','Type','Origin','Category','ID','URL','Desc',
             'Date','Flags','RefCount','MinVersion']

CarDatafilesFolder = 'CarDatafiles'
TrackDatafilesFolder = 'TrackDatafiles'
dataFilesExtension = '.rFactory.txt'

# File-specific items
config_tabCar = {
  'carColumns' : ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating', 'DB file (hidden)'],
  'carFilters' : ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
  }

"""
Accessing the data for rFactory.

This reads rFactory's data files - one for each car, one for each track.
File naming matches the name used by rFactor.  Data in the files is derived
from rFactor but then enhanced - e.g. S397 __cars and __tracks do not specify that
S397 is the author.  Additional data such as 
__cars:
* type (open-wheeler, sports, GT, Indy, endurance, etc)
* class (F1, GT3, GTE, etc)
* type of gearshift (H, dogleg, paddles, sequential, auto, preselector!) 
* what driving aids the car has (TC, ABS, etc)  [a list?]
* year and decade of manufacture
* star rating

__tracks:
* year and decade
* continent
* country
* type (permanent, temporary, road, speedway, fictional, historic, etc)
* star rating

It also handles writing the files if they've been edited.
"""

from rFactoryConfig import carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension
from trawl_rF2_datafiles import getListOfFiles, readFile, getTags

__cars = {
  'dummyData' : [
          ['Ferrari',  '458', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Corvette', 'C7', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Bentley',  'Continental', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Eve',      'F1', 'F1', 'ISI', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'Historic Challenge_EVE_1968'],
          ['Spark',    'F1', 'F1', 'ISI', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'Historic Challenge_spark_1968'],
          ['Porsche',  '917K', 'Gp.C', 'Apex', 'GT', 'RWD', '1967', '1960-', '*****', 'FLAT12_917k_1971'],
          ['Lola',     'T70', 'Gp.C', 'Crossply', 'GT', 'RWD', '1974', '1970-', '***', 'car DB file'],
          ['Sauber',   'C11', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Sauber_C11'],
          ['Porsche',  '962C', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Porsche_062C'],
          ['Mazda',    '787B', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Mazda_787B'],
          ['Ferrari',  '312', 'F1', 'Chief Wiggum/Postipate', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'car DB file'],
          ['Caterham', '7', 'C7', 'MikeeCZ', 'Sports', 'RWD', '2016', '2010-', '****', 'car DB file']
        ],
  'tags' : []
  }

__tracks = {
  'dummyData' : [
          ['Spa',  'S397', 'Historic', '1966', '1960-', '*****', 'track DB file']
        ],
  'tags' : []
  }

def __readDatafiles():
  # Run this once to get the data
  if len(__cars['tags']) == 0:
    carFiles = getListOfFiles(path=CarDatafilesFolder, pattern='*'+dataFilesExtension)
    trackFiles = getListOfFiles(path=TrackDatafilesFolder, pattern='*'+dataFilesExtension)

    for car in carFiles:
      text = readFile(car[0])
      tags = getTags(text)
      _entry = tags#{tags['Name'] : tags}
      __cars['tags'].append(_entry)

    for track in trackFiles:
      text = readFile(track[0])
      tags = getTags(text)
      _entry = tags#{tags['Name'] : tags}
      __tracks['tags'].append(_entry)
  # else it's already loaded

def getAllCarData(tags, maxWidth=30):
  __readDatafiles()
  _result = []
  for _car in __cars['tags']:
    _row = []
    for tag in tags:
      _row.append(_car[tag][:maxWidth])
    _result.append(_row)
  return _result

def getSingleCarData(id='Howston_G4_1968', tags=['originalFolder', 'vehFile', 'Name']):
  d = getAllCarData(['DB file ID']+tags, maxWidth=100)
  for row in d:
    if row[0] == id:
      return row[1:]

def getSingleTrackData(id='Brianza_1966', tags=['originalFolder', 'Scene Description', 'Name']):
  d = getAllTrackData(['DB file ID']+tags, maxWidth=100)
  for row in d:
    if row[0] == id:
      return row[1:]


def getAllTrackData(tags, maxWidth=30):
  __readDatafiles()
  _result = []
  for _track in __tracks['tags']:
    _row = []
    for tag in tags:
      _row.append(_track[tag][:maxWidth])
    _result.append(_row)
  return _result


if __name__ == '__main__':
  # To run this by itself for development
  __readDatafiles()
  carData = getAllCarData(carTags)

  car = getSingleCarData(id='Howston_G4_1968', tags=['originalFolder', 'vehFile', 'Name'])
  assert car == ['Installed\\vehicles\\Howston_G4_1968\\1.96', '', 'Howston_G4_1968']

  track = getSingleTrackData(id='Brianza_1966', tags=['originalFolder', 'Scene Description', 'Name'])
  assert track == ['Installed\\locations\\Brianza_1966\\2.04', '', 'Brianza_1966']
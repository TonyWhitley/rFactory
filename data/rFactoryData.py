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
from data.trawl_rF2_datafiles import CarDataFiles, TrackDataFiles, translate_date
from data.utils import getListOfFiles, readFile, getTags
from data.rFactoryConfig import carTags, trackTags, CarDatafilesFolder, \
    TrackDatafilesFolder, dataFilesExtension
import sys

sys.path.append('..')

__cars = {
    'dummyData': {
        '134_JUDD': {
            'Manufacturer': '134 JUDD',
            'Model': '134 JUDD',
            'Class': '',
            'tType': 'Prototype',
            'F/R/4WD': 'RWD',
            'Year': '',
            'Decade': '',
            'Rating': '***',
            'DB file ID': '134_JUDD',
            'Gearshift': 'Paddles',
            'Aids': '',
            'AIstrengthFactor': '',
            'GraphicDetailsFactor': '',
            'originalFolder': 'Installed\\vehicles\\134_JUDD\\0.7',
            'vehFile': '134_JUDD',
            'Name': '134_JUDD',
            'Version': '0.7',
            'Type': '2',
            'Author': 'PortoAlto and rstRmods',
            'Origin': '2',
            'Category': '7',
            'ID': '',
            'URL': '',
            'Desc': '',
            'Date': '131465248676360000',
            'Flags': '270536704',
            'RefCount': '1',
            'MinVersion': ''},
        '1975BRABHAM': {
            'Manufacturer': 'BRABHAM',
            'Model': 'BRABHAM',
            'Class': '',
            'tType': '',
            'F/R/4WD': 'RWD',
            'Year': '1975',
            'Decade': '1970-',
            'Rating': '***',
            'DB file ID': '1975BRABHAM',
            'Gearshift': 'Paddles',
            'Aids': '',
            'AIstrengthFactor': '',
            'GraphicDetailsFactor': '',
            'originalFolder': 'Installed\\vehicles\\1975BRABHAM\\1.0',
            'vehFile': 'Reutemann_07',
            'Name': '1975BRABHAM',
            'Version': '1.0',
            'Type': '2',
            'Author': '',
            'Origin': '0',
            'Category': '0',
            'ID': '',
            'URL': '',
            'Desc': '',
            'Date': '1493632923',
            'Flags': '3149824',
            'RefCount': '1',
            'MinVersion': ''},
        '1975BRM': {
            'Manufacturer': 'BRM',
            'Model': 'BRM',
            'Class': '',
            'tType': '',
            'F/R/4WD': 'RWD',
            'Year': '1975',
            'Decade': '1970-',
            'Rating': '***',
            'DB file ID': '1975BRM',
            'Gearshift': 'Paddles',
            'Aids': '',
            'AIstrengthFactor': '',
            'GraphicDetailsFactor': '',
            'originalFolder': 'Installed\\vehicles\\1975BRM\\1.0',
            'vehFile': 'Evans_14',
            'Name': '1975BRM',
            'Version': '1.0',
            'Type': '2',
            'Author': '',
            'Origin': '0',
            'Category': '0',
            'ID': '',
            'URL': '',
            'Desc': '',
            'Date': '1493632924',
            'Flags': '3149824',
            'RefCount': '1',
            'MinVersion': ''},
    },
    'tags': {}}

__tracks = {
    'dummyData': {
        '3PA_Bathurst_2014': {
            'Track Name': 'PA Bathurst ',
            'Continent': '',
            'Country': '',
            'tType': 'Temporary',
            'Year': '2014',
            'Decade': '2010-',
            'Rating': '***',
            'DB file ID': '3PA_Bathurst_2014',
            'AIstrengthFactor': '',
            'GraphicDetailsFactor': '',
            'originalFolder': 'Installed\\locations\\3PA_Bathurst_2014\\1.02',
            'Scene Description': '',
            'Name': '3PA_Bathurst_2014',
            'Version': '1.02',
            'Type': '1',
            'Author': 'mianiak',
            'Origin': '3',
            'Category': '57',
            'ID': '',
            'URL': 'http://rfactor.net/downloads/getmod.php',
            'Desc': '3PA_Bathurst_2014\x0f',
            'Date': '130871461203380000',
            'Flags': '270536704',
            'RefCount': '1',
            'MinVersion': ''},
        '3PA_Matsusaka_2015': {
            'Track Name': 'PA Matsusaka ',
            'Continent': '',
            'Country': '',
            'tType': 'Permanent',
            'Year': '2015',
            'Decade': '2010-',
            'Rating': '***',
            'DB file ID': '3PA_Matsusaka_2015',
            'AIstrengthFactor': '',
            'GraphicDetailsFactor': '',
            'originalFolder': 'Installed\\locations\\3PA_Matsusaka_2015\\1.00',
            'Scene Description': '',
            'Name': '3PA_Matsusaka_2015',
            'Version': '1.00',
            'Type': '1',
            'Author': 'woochoo, & ISI',
            'Origin': '3',
            'Category': '55',
            'ID': '',
            'URL': 'http://rfactor.net/downloads/getmod.php',
            'Desc': '',
            'Date': '131103652938530000',
            'Flags': '271593472',
            'RefCount': '1',
            'MinVersion': ''},
        '60sHockenheim': {
            'Track Name': 'sHockenheim',
            'Continent': '',
            'Country': '',
            'tType': 'Permanent',
            'Year': '1960',
            'Decade': '1960-',
            'Rating': '***',
            'DB file ID': '60sHockenheim',
            'AIstrengthFactor': '',
            'GraphicDetailsFactor': '',
            'originalFolder': 'Installed\\locations\\60sHockenheim\\0.85',
            'Scene Description': '',
            'Name': '60sHockenheim',
            'Version': '0.85',
            'Type': '1',
            'Author': '',
            'Origin': '3',
            'Category': '55',
            'ID': '',
            'URL': '',
            'Desc': 'an early hockenheim layout done for a bit of fun and a blast with the historics\x0f',
            'Date': '1531869330',
            'Flags': '3145728',
            'RefCount': '1',
            'MinVersion': ''}},
    'tags': {}}


def reloadAllData():
    """ Reset all tags and read them again """
    __cars['tags'] = {}
    __tracks['tags'] = {}
    __readDatafiles()


def __readDatafiles():
    cdf = CarDataFiles()
    for car in cdf.cache_o.cache:
        __cars['tags'][car['DB file ID']] = car
    tdf = TrackDataFiles()
    for track in tdf.cache_o.cache:
        __tracks['tags'][track['DB file ID']] = track

    """ LEGACY
  Run this once to get the data
  if len(__cars['tags']) == 0:
    carFiles = getListOfFiles(path=CarDatafilesFolder, pattern='*'+dataFilesExtension)
    trackFiles = getListOfFiles(path=TrackDatafilesFolder, pattern='*'+dataFilesExtension)

    if len(carFiles) > 0:
      for car in carFiles:
        text, error = readFile(car[0])
        tags = getTags(text)
        __carID = tags['DB file ID']
        __cars['tags'][__carID] = tags
    else:
      print('No car data files')

    if len(trackFiles) > 0:
      for track in trackFiles:
        text, error = readFile(track[0])
        tags = getTags(text)
        __trackID = tags['DB file ID']
        __tracks['tags'][__trackID] = tags
        # to print dummy data print(tags)
        # print()
    else:
      print('Using dummy data')
      __tracks['tags'] = __tracks['dummyData']
  # else it's already loaded
  """


def getAllData(__carsTracks, tags, maxWidth):
    """ Get a list for all cars or tracks of dicts of the requested tags """
    __readDatafiles()
    _result = {}
    for _carsTrack in __carsTracks['tags']:
        _row = {}
        for tag in tags:
            if tag == 'DB file ID':  # Do not shorten that
                _row[tag] = __carsTracks['tags'][_carsTrack][tag]
            elif tag == 'Date':
                if len(__carsTracks['tags'][_carsTrack][tag]) > 10:
                    # Date not translated
                    _row[tag] = translate_date(
                        __carsTracks['tags'][_carsTrack][tag])
                else:
                    _row[tag] = __carsTracks['tags'][_carsTrack][tag]
            else:
                try:
                    _row[tag] = __carsTracks['tags'][_carsTrack][tag][:maxWidth]
                except KeyError:
                    print(F'Missing tag {tag}')
        _result[_carsTrack] = _row
    return _result


def getSingleData(__carsTracks, id, tags):
    """ Get a dict of the requested tags for one car/track """
    __readDatafiles()
    _result = {}
    _carsTrack = id
    _row = {}
    for tag in tags:
        if tag in __carsTracks['tags'][_carsTrack]:
            _row[tag] = __carsTracks['tags'][_carsTrack][tag]
        else:  # tag isn't present in data file.
            _row[tag] = ''
    return _row


def getAllCarData(tags, maxWidth=30):
    return getAllData(__cars, tags, maxWidth)


def getSingleCarData(
    id='Howston_G4_1968',
    tags=[
        'originalFolder',
        'vehFile',
        'Name']):
    """ Get a dict of the requested tags for one car """
    return getSingleData(__cars, id, tags)


def getSingleTrackData(
    id='Brianza_1966',
    tags=[
        'originalFolder',
        'Scene Description',
        'Name']):
    """ Get a dict of the requested tags for one track """
    return getSingleData(__tracks, id, tags)


def getAllTrackData(tags, maxWidth=30):
    return getAllData(__tracks, tags, maxWidth)


if __name__ == '__main__':
    # To run this by itself for development
    __readDatafiles()
    carData = getAllCarData(carTags)

    car = getSingleCarData(
        id='Howston_G4_1968',
        tags=[
            'originalFolder',
            'vehFile',
            'Name'])
    assert car == {
        'Name': 'Howston_G4_1968',
        'originalFolder': 'Installed\\vehicles\\Howston_G4_1968\\2.00',
        'vehFile': 'HG4_37.VEH'}

    track = getSingleTrackData(
        id='Brianza_1966',
        tags=[
            'originalFolder',
            'Scene Description',
            'Name'])

    assert track == {
        'Name': 'Brianza_1966',
        'Scene Description': 'brianzajr',
        'originalFolder': 'Installed\\locations\Brianza_1966\\2.04'}

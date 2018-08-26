"""
Trawl rF2 data files for raw data as a baseline for rFactory data files
1) find files
2) read them
3) grep for data keywords
4) extract data into data file
"""

import fnmatch
import glob
import os
import re

from rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension

carCategories = {
  '3' : 'GT',
  '5' : 'Novel',
  '6' : 'Open',
  '7' : 'Prototype',
  '9' : 'Street',
  '10' : 'Touring'
  }

trackCategories = {
  '53' : 'Novel',
  '55' : 'Permanent',
  '56' : 'Rally',
  '57' : 'Temporary'
  }

def getListOfFiles(path, pattern='*.c', recurse=False):
    def getFiles(filepattern):
        filenames = []
        for filepath in glob.glob(filepattern):
            filenames.append([filepath, os.path.basename(filepath)])
        return filenames

    def walk(startPath, filepattern):
        filenames = []
        for root, dirs, files in os.walk(startPath):
            for file in files:
                if fnmatch.fnmatch(file, filepattern):
                    filenames.append([os.path.join(root, file), file])
        return filenames

    if recurse:
        files = walk(path, pattern)
    else:
        files = getFiles(os.path.join(path, pattern))

    return files

def readFile(filename):
  with open(filename) as f:
    originalText = f.readlines()
  return originalText

def readTags(text):
  """ Grep the tags in text and return them as a list """
  # Name=134_JUDD
  tags = []
  for line in text:
    m = re.match(r'(.*) *= *(.*)', line)
    if m:
      tags.append(m.group(1))
      #print(m.group(1), m.group(2))
  return tags

def getTags(text):
  """ Grep the tags in text and return them as a dict """
  # 'Name' 'Version' 'Type' 'Author' 'Origin' 'Category' 'ID' 
  # 'URL' 'Desc' 'Date' 'Flags' 'RefCount' 'Signature' 'MASFile'
  # 'BaseSignature' 'MinVersion'
  # Name=134_JUDD
  tags = {}
  for line in text:
    m = re.match(r'(.*) *= *(.*)', line)
    if m:
      tags[m.group(1)] = m.group(2)
      #print(m.group(1), m.group(2))
  return tags

def createDataFile(datafilesPath, filename, dict, tagsToBeWritten):
  _filepath = os.path.join(datafilesPath, filename+dataFilesExtension)
  try:
    os.makedirs(datafilesPath, exist_ok=True)
    with open(_filepath, "w") as f:
      for tag in tagsToBeWritten:
        if tag in dict:
          val = dict[tag]
        elif tag == 'DB file ID':
          val = filename # The unique identifier for the car/track. I think.
        elif tag in ['Track Name', 'Manufacturer', 'Model']:
          val = dict['strippedName'].replace('_', ' ')  # default
        elif tag == 'Rating':
          val = '***'
        elif tag == 'F/R/4WD':
          val = 'RWD' # Most cars are
        elif tag == 'Gearshift':
          val = 'Paddles' # a reasonable default
        else: # value not available
          val = ''
        f.write('%s=%s\n' % (tag, val))
  except:
    print('Failed to write %s' % _filepath)
    quit()

def cleanTrackName(name):
  """ Track names often include a version, strip that """
  name = re.sub(r'v\d+\.\d*', '', name)
  return name

def extractYear(name):
  # Cars and tracks often include the year, try to extract that.
  # Also return remainder of name when year removed.
  # skip first digit, may be 3PA....
  if name.startswith('3'):
    name = name[1:]
  year = ''
  decade = ''
  # Look for 4 digit years first to avoid BT44
  # Reverse as the year tends to be at the end, e.g. USF2000_2016
  _years = re.findall(r'(\d+)', name)
  if _years:
    _years.reverse()
    for y in _years:
      if len(y) == 4:
        year = y
        decade = year[:3] + '0-'
        print(name, year)
        return year, decade, name.replace(y,'')
    for y in _years:
      if len(y) == 2:
        if y[0] in '01':
          year = '20' + y
        else:
          year = '19' + y
        decade = year[:3] + '0-'
        return year, decade, name.replace(y,'')
  #print(name, year)
  return year, decade, name

def getVehScnNames(dataFilepath):
  """ 
  Read the data file containing Name xxxxx.veh pairs 
  Also for xxxxx.scn pairs
  """
  _dict = {}
  text = readFile(dataFilepath)
  for line in text:
    if line.startswith('#'):
      continue # comment line
    _split = line.split()
    if len(_split) == 2:
      name, vehScn = _split
      _dict[name] = vehScn
  return _dict

if __name__ == '__main__':
  getAllTags = False
  rF2_dir = os.path.join(rF2root, 'Installed')
  vehicleFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles'), pattern='*.mft', recurse=True)
  trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations'), pattern='*.mft', recurse=True)
  F1_1988_trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations', 'F1_1988_Tracks'), pattern='*.mas', recurse=True)

  vehNames = getVehScnNames('vehNames.txt')
  scnNames = getVehScnNames('scnNames.txt')

  tags = {}
  if getAllTags:
    for veh in vehicleFiles:
      text = readFile(veh[0])
      for tag in readTags(text):
        tags[tag] = 0
    print(tags)
  else: # create data file
    for veh in vehicleFiles:
      text = readFile(veh[0])
      tags = getTags(text)
      #print('\nData file: "%s.something"' % tags['Name'])
      for requiredTag in ['Name','Version','Type','Author','Origin','Category','ID','URL','Desc','Date','Flags','RefCount','#Signature','#MASFile','MinVersion','#BaseSignature']:
        # MASFile, Signature and BaseSignature filtered out - NO THEY AREN'T, 
        # tags[] still contains them.  tagsToBeWritten filters them out.
        # Not sure what this for loop is, er, for.
        if requiredTag in tags:
          """filter out boilerplate
          Author=Mod Team
          URL=www.YourModSite.com
          Desc=Your new mod.
          """
          if tags[requiredTag] in ['Mod Team', 'www.YourModSite.com', 'Your new mod.']:
            tags[requiredTag] = ''
          if tags[requiredTag] in ['Slow Motion', 'Slow Motion Modding Group']: # make up your minds boys!
            tags[requiredTag] = 'Slow Motion Group'
          if tags[requiredTag] in ['Virtua_LM Modding Team']: # make up your minds boys!
            tags[requiredTag] = 'Virtua_LM'
          #print('%s=%s' % (requiredTag, tags[requiredTag]))
          if requiredTag == 'Name':
            tags['Year'], tags['Decade'], tags['strippedName'] = extractYear(tags['Name'])
            # extract class from name if it's there
            for __class in ['F1', 'F3', 'GT3', 'GTE', 'BTCC', 'LMP1', 'LMP2', 'LMP3']: # 'F2' filters rF2...
              if __class in tags['Name']:
                tags['Class'] = __class
                tags['strippedName'] = tags['strippedName'].replace(__class, '')
      if tags['Category'] in carCategories:
        tags['tType'] = carCategories[tags['Category']]
      # We need the original data folder to assemble the .VEH file path to put in 
      # "All Tracks & Cars.cch" to force rF2 to switch cars.  We also need the .VEH 
      # file names and that's a bit more difficult.
      tags['originalFolder'], _ = os.path.split(veh[0][len(rF2root)+1:]) # strip the root
      # if veh file name is available in vehNames.txt use it
      if tags['Name'] in vehNames:
        tags['vehFile'] = vehNames[tags['Name']]
      createDataFile(datafilesPath=CarDatafilesFolder, filename=tags['Name'], dict=tags, tagsToBeWritten=carTags)


  print('\n\nTracks:')
  tags = {}
  if getAllTags:
    for track in trackFiles:
      text = readFile(track[0])
      for tag in readTags(text):
        tags[tag] = 0
    print(tags)
  else: # create data file
    for track in trackFiles:
      text = readFile(track[0])
      tags = getTags(text)
      #print('\nData file: "%s.something"' % tags['Name'])
      for requiredTag in ['Name','Version','Type','Author','Origin','Category','ID','URL','Desc','Date','Flags','RefCount','#Signature','#MASFile','MinVersion','#BaseSignature']:
        # MASFile, Signature and BaseSignature filtered out
        if requiredTag in tags:
          """filter out boilerplate
          Author=Mod Team
          URL=www.YourModSite.com
          Desc=Your new mod.
          """
          if tags[requiredTag] in ['Mod Team', 'www.YourModSite.com', 'Your new mod.']:
            tags[requiredTag] = ''
          #print('%s=%s' % (requiredTag, tags[requiredTag]))
          if requiredTag == 'Name':
            tags['strippedName'] = cleanTrackName(tags['Name'])
            tags['Year'], tags['Decade'], tags['strippedName'] = extractYear(tags['strippedName'])
      # We need the original data folder to assemble the .SCN file path to put in 
      # "Player.JSON" to force rF2 to switch tracks.  We also need the .SCN
      # file names and that's a bit more difficult.
      # To select the track we also need the "Scene Description"
      tags['originalFolder'], _ = os.path.split(track[0][len(rF2root)+1:]) # strip the root
      # if scn file name is available in scnNames.txt use it
      if tags['Name'] in scnNames:
        tags['Scene Description'] = scnNames[tags['Name']]

      if tags['Category'] in trackCategories:
        tags['tType'] = trackCategories[tags['Category']]

      if tags['Name'] != 'F1_1988_Tracks':
        createDataFile(datafilesPath=TrackDatafilesFolder, filename=tags['Name'], dict=tags, tagsToBeWritten=trackTags)
      else: # it's a folder of several tracks
        for f1988 in F1_1988_trackFiles:
          tags['Name'] = f1988[1][:-4]
          tags['strippedName'] = cleanTrackName(tags['Name'])
          tags['Year'], tags['Decade'], tags['strippedName'] = extractYear(tags['strippedName'])
          # if scn file name is available in scnNames.txt use it
          if tags['Name'] in scnNames:
            tags['Scene Description'] = scnNames[tags['Name']]
          if tags['Category'] in trackCategories:
            tags['tType'] = trackCategories[tags['Category']]
          createDataFile(datafilesPath=TrackDatafilesFolder, filename=tags['Name'], dict=tags, tagsToBeWritten=trackTags)

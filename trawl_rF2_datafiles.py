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

from rFactoryConfig import carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension

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
  f = open(filename)
  originalText = f.readlines()
  f.close()
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

def createDataFile(datafilesPath, filename, dict, tags_selected):
  _filepath = os.path.join(datafilesPath, filename+dataFilesExtension)
  try:
    os.makedirs(datafilesPath, exist_ok=True)
    with open(_filepath, "w") as f:
      for tag in tags:
        if tag in dict:
          val = dict[tag]
        elif tag == 'DB file (hidden)':
          val = filename # The unique identifier for the car/track. I think.
        elif tag in ['Track Name', 'Manufacturer', 'Model']:
          val = dict['strippedName'].replace('_', ' ')  # default
        elif tag == 'Rating':
          val = '***'
        else: # value not available
          val = ''
        f.write('%s=%s\n' % (tag, val))
  except:
    print('Failed to write %s' % _filepath)
    quit()

def extractYear(name):
  # Cars and tracks often include the year, try to extract that.
  # Also return remainder of name when year removed.
  # skip first digit, may be 3PA....
  if name.startswith('3'):
    name = name[1:]
  year = ''
  decade = ''
  for y in re.findall(r'(\d+)', name):  # Look for 4 digit years first to avoid BT44
    if len(y) == 4:
      year = y
      decade = y[:3] + '0-'
      print(name, year)
      return year, decade, name.replace(y,'')
  for y in re.findall(r'(\d+)', name):
    if len(y) == 2:
      if y[0] in '01':
        year = '20' + y
      else:
        year = '19' + y
      decade = y[:3] + '0-'
      return year, decade, name.replace(y,'')
  print(name, year)
  return year, decade, name

if __name__ == '__main__':
  getAllTags = False
  rF2_dir = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed'
  vehicleFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles'), pattern='*.mft', recurse=True)
  trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations'), pattern='*.mft', recurse=True)

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
        # tags[] still contains them.  tags_selected filters them out.
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
          #print('%s=%s' % (requiredTag, tags[requiredTag]))
          if requiredTag == 'Name':
            tags['Year'], tags['Decade'], tags['strippedName'] = extractYear(tags['Name'])
            # extract class from name if it's there
            for __class in ['F1', 'F3', 'GT3', 'GTE', 'BTCC', 'LMP1', 'LMP2', 'LMP3']: # 'F2' filters rF2...
              if __class in tags['Name']:
                tags['Class'] = __class
                tags['strippedName'] = tags['strippedName'].replace(__class, '')
      # We need the original data folder to assemble the .veh file path to put in 
      # "All Tracks & Cars.cch" to force rF2 to switch cars.  We also need the .veh 
      # file names and that's a bit more difficult.
      tags['originalFolder'], _ = os.path.split(veh[0])
      createDataFile(datafilesPath=CarDatafilesFolder, filename=tags['Name'], dict=tags, tags_selected=carTags)


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
            tags['Year'], tags['Decade'], tags['strippedName'] = extractYear(tags['Name'])
      createDataFile(datafilesPath=TrackDatafilesFolder, filename=tags['Name'], dict=tags, tags_selected=trackTags)

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

def createDataFile(datafilesPath, filename, dict, tags):
  _filepath = os.path.join(datafilesPath, filename+dataFilesExtension)
  try:
    os.makedirs(datafilesPath, exist_ok=True)
    with open(_filepath, "w") as f:
      for tag in tags:
        if tag in dict:
          val = dict[tag]
        elif tag == 'DB file (hidden)':
          val = filename
        elif tag == 'Track Name':
          val = dict['Name'].replace('_', ' ')  # default
        elif tag == 'Rating':
          val = '***'
        else: # value not available
          val = ''
        f.write('%s=%s\n' % (tag, val))
  except:
    print('Failed to write %s' % _filepath)
    quit()

def extractYear(name):
  # Cars and tracks often include the year, try to extract that
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
      return year, decade
  for y in re.findall(r'(\d+)', name):
    if len(y) == 2:
      if y[0] in '01':
        y = '20' + y
      else:
        y = '19' + y
      year = y
      decade = y[:3] + '0-'
  print(name, year)
  return year, decade

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
      for tag in ['Name','Version','Type','Author','Origin','Category','ID','URL','Desc','Date','Flags','RefCount','#Signature','#MASFile','MinVersion','#BaseSignature']:
        # MASFile, Signature and BaseSignature filtered out
        if tag in tags:
          """filter out boilerplate
          Author=Mod Team
          URL=www.YourModSite.com
          Desc=Your new mod.
          """
          if tags[tag] == 'Mod Team':
            continue
          if tags[tag] == 'www.YourModSite.com':
            continue
          if tags[tag] == 'Your new mod.':
            continue
          #print('%s=%s' % (tag, tags[tag]))
          if tag == 'Name':
            tags['Year'], tags['Decade'] = extractYear(tags['Name'])
          createDataFile(datafilesPath=CarDatafilesFolder, filename=tags['Name'], dict=tags, tags=carTags)


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
      for tag in ['Name','Version','Type','Author','Origin','Category','ID','URL','Desc','Date','Flags','RefCount','#Signature','#MASFile','MinVersion','#BaseSignature']:
        # MASFile, Signature and BaseSignature filtered out
        if tag in tags:
          """filter out boilerplate
          Author=Mod Team
          URL=www.YourModSite.com
          Desc=Your new mod.
          """
          if tags[tag] == 'Mod Team':
            continue
          if tags[tag] == 'www.YourModSite.com':
            continue
          if tags[tag] == 'Your new mod.':
            continue
          #print('%s=%s' % (tag, tags[tag]))
          if tag == 'Name':
            tags['Year'], tags['Decade'] = extractYear(tags['Name'])
          createDataFile(datafilesPath=TrackDatafilesFolder, filename=tags['Name'], dict=tags, tags=trackTags)

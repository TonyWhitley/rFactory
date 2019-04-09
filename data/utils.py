# Utility functions shared by trawl_rF2_datafiles and data.
import fnmatch
import glob
import os
import re

def readFile(filename):
  try:
    with open(filename) as f:
      originalText = f.readlines()
  except:
    originalText = []
  return originalText

def writeFile(_filepath, text):
  _path = os.path.dirname(_filepath)   # Create the path if it doesn't exist
  os.makedirs(_path, exist_ok=True)
  with open(_filepath, "w") as f:
    f.writelines(text)

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



# Utility functions shared by trawl_rF2_datafiles and data.
import fnmatch
import glob
import os
import re
import sys

def readFile(filename):
  try:
    with open(filename) as f:
      originalText = f.readlines()
  except Exception as e:
    originalText = ['Exception reading "%s": %s"' % (filename, e)]
  return originalText

def readTextFile(filename):
  """
  Read a wall of text, concatenate the lines, replace \n with newlines
  """
  _lines = readFile(filename)
  _txt = ''
  for line in _lines:
    _txt += ' '+line.strip()
  _txt = _txt.replace(r'\n ', '\n') # That will have added spaces after \n
  _txt = _txt.replace(r'\n', '\n')  # There may be other \n
  _txt = _txt[1:] # throw away the first space
  return _txt

def writeFile(_filepath, text):
  _path = os.path.dirname(_filepath)   # Create the path if it doesn't exist
  os.makedirs(_path, exist_ok=True)
  try:
    with open(_filepath, "w") as f:
      f.writelines(text)
      status = None
  except Exception as e:
    status = ['Exception writing  "%s": %s"' % (filename, e)]
  return status

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

def bundleFolder(filepath):
    """
    If running in a PyInstaller bundle the program is extracted into a 
    temporary folder.  If a file in that bundle is required calculate
    its path.
    A file is added to the bundle with a command line option like this:
      --add-data resources\rfactory.ico;resources 
    or in the .spec file like this:
      datas=[('resources\\rfactory.ico', 'resources')],

    """
    if getattr( sys, 'frozen', False ) :
      # running in a PyInstaller bundle (exe)
      _p = os.path.join(sys._MEIPASS, filepath)
      #print(_p)
      if os.path.exists(_p):
          return _p
      #__, _filename = os.path.split(filepath)
      #_p = os.path.join(sys._MEIPASS, _filename)
      #print(_p)
      #if os.path.exists(_p):
      #    return _p
    else :
      # running live
      return filepath

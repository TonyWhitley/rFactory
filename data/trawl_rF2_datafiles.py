"""
Trawl rF2 data files for raw data as a baseline for rFactory data files
1) find files
2) read them
3) grep for data keywords
4) Title Case them
5) extract data into data file

6) check if rF2 data file has been deleted

There are different sources for data (tags)
1) "cached_tags" are read from a sparsely-populated Excel file that is
   curated manually with tags that are known will be wrong if read by
   the subsequent automatic methods.  This file is a shared resource that can
   be updated by the community and then the new version downloaded.
   This is the "official" resource for tags, subsequent sources are just to
   provide data when it is not present in the spreadsheet.
   If a new mod is discovered then a row is added to the spreadsheet
   with the automatically-generated tags.  That means the spreadsheet is
   initialised with tags that need to be edited.
2) MFT files give some data and are quick to read
3) MAS files are slower to read
  a) Car MAS files contain hdv and ini files that provide some tags
  b) Track MAS files contain scns file (use the name) and gdb files which
     may have lat and longitude tags

Many tags need to be "massaged" to get the data in the required format, e.g.
converting car and track categories from numbers to names.
More tricky is extracting year information from the names of cars and tracks
simple example: USF2000_2016 is the car USF2000 from 2016

A tag is only written with a non-blank value once, if more data comes along
it is discarded, so the cached_tags have priority over ones from the MFT files
and they over those from MAS files (hmm... they are equally good sources)

Once the data has been extracted it is stored in rFactory's own data files
Marker files mark that a track folder has been processed
"""
"""
Process is
* Read spreadsheet of cached tags
* Search for cars and tracks
* If a car or track is not cached then extract tags and write a new row in
  the spreadsheet
* If a car or mod is updated then PERHAPS extract tags and overwrite the row in
  the spreadsheet
!!! There is no need for the "rFactory data files"
"""
"""
Note: rFactoryModManager does not need all the data, it only works down to the
granularity of a mod folder.
"""
import datetime
import os
import re
import subprocess
import sys
import time

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from data.rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension,playerPath,markerfileExtension
from data.utils import getListOfFiles, readFile, writeFile, getTags, \
    executeCmd, executeCmdInBatchFile

from data.rFactoryData import getSingleCarData, reloadAllData
from data.LatLong2Addr import google_address, country_to_continent
from data.cached_data import Cached_data

import edit.carNtrackEditor as carNtrackEditor

######################################################################
def translate_date(val):
    """
    Convert Windows or Unix datetime to YYYY-MM-DD
    """
    try:
        if len(val) == 18: # Windows filetime.
            # http://support.microsoft.com/kb/167296
            # How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
            EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
            HUNDREDS_OF_NANOSECONDS = 10000000
            ts = datetime.datetime.fromtimestamp((int(float(val)) - \
                EPOCH_AS_FILETIME) // HUNDREDS_OF_NANOSECONDS)
        else: # Unix
            ts = datetime.datetime.fromtimestamp(int(float(val)))
    except Exception as e:
        print(e)
        ts = datetime.datetime.today()
    return ts.strftime("%Y-%m-%d")

######################################################################
# Car/Track subclass
class DataFiles:
    installed_folder = None
    datafiles_folder = None
    mfts_and_timestamps = None
    data_files_and_timestamps = None
    newer_mfts = None
    newFiles = list()
    _tags = dict()
    encrypted_files = list()
    ModMgr = os.path.join(rF2root, r'Bin32\ModMgr.exe')

    def __getitem__(self, key):
        return self._tags[key]

    def __setitem__(self, key, value):
        """
        Only set tag if it does not already have a value
        """
        if type(value) != str:
            raise TypeError("tag must be string")
        if not key in self._tags or self._tags[key] == '':
            self._tags[key] = value

    def make_datafile_name(self, folder):
        r"""
        e.g.
        c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.94\USF2000_2016.mft
        to
        dataFiles\Cars\USF2000_2016.rFactory.txt
        """
        _mft = os.path.basename(folder).split('.')[0]
        if 'vehicles' in folder.lower():
            _res = f'datafiles\\cars\\{_mft}.rfactory.txt'.format()
        else:
            _res = f'datafiles\\tracks\\{_mft}.rfactory.txt'.format()
        return _res

    def find_multi_mas_folders(self):
        """
        Some mods contain many mas files in a folder, e.g. F1_1988_Tracks
        Try to spot them by checking the number of mas files in a revision
        folder.
        Mod folder structure is <mod name>\<revision>\*.mas

        The REAL test is to look for more than one .SCN file for tracks and
        .VEH files for cars (also found in all_vehicles.ini)

        rF2 installed_folder: 'vehicles' or 'locations'
        """
        rF2_dir = os.path.join(rF2root, 'Installed')
        _mods = getListOfFiles(os.path.join(rF2_dir, self.installed_folder),
                                    pattern='*',
                                    recurse=False)
        multi_mas = list()
        for _mod_folder, _mod in _mods:
            _revs = getListOfFiles(_mod_folder,
                                  pattern='*',
                                  recurse=False)
            for _rev in _revs:
                _mas_files = getListOfFiles(_rev[0],
                                            pattern='*.mas',
                                            recurse=True)
                if len(_mas_files) > 10:
                    multi_mas.append(_mod)
        pass
        return multi_mas

    def get_mfts_and_timestamps(self):
        """
        rF2 installed_folder: 'vehicles' or 'locations'
        """
        rF2_dir = os.path.join(rF2root, 'Installed')
        _mft_files = getListOfFiles(os.path.join(rF2_dir, self.installed_folder),
                                    pattern='*.mft',
                                    recurse=True)
        self.mfts_and_timestamps = dict()
        for folder in _mft_files:
            _folder = folder[0].lower() # os.path.dirname(
            _timestamp = os.path.getmtime(_folder)
            self.mfts_and_timestamps[_folder] = _timestamp
        return self.mfts_and_timestamps

    def get_data_files_and_timestamps(self):
        """
        rFactory datafiles_folder: 'CarDatafilesFolder' or 'TrackDatafilesFolder'
        """
        _mft_files = getListOfFiles(self.datafiles_folder,
                                            pattern='*.txt',
                                            recurse=False)
        self.data_files_and_timestamps = dict()
        for folder in _mft_files:
            _timestamp = os.path.getmtime(folder[0])
            self.data_files_and_timestamps[folder[0].lower()] = _timestamp
        return self.data_files_and_timestamps

    def get_newer_mfts(self):
        if not self.mfts_and_timestamps:
            self.get_mfts_and_timestamps()
        if not self.data_files_and_timestamps:
            self.get_data_files_and_timestamps()

        self.newer_mfts = list()
        for folder, timestamp in self.mfts_and_timestamps.items():
            # nope, we need to make c:\Users\tony_\source\repos\rFactory\dataFiles\Cars\USF2000_2016.rFactory.txt
            _datafile = self.make_datafile_name(folder)
            if _datafile in self.data_files_and_timestamps:
                if timestamp > self.data_files_and_timestamps[_datafile]:
                    self.newer_mfts.append(folder)
            else:
                self.newer_mfts.append(folder)
        return self.newer_mfts

    def get_data(self, _mft):
        """
        Get data from data file
        If data file does not exist create it
        """
        _mft = _mft.lower()

        if not self.newer_mfts:
            self.get_newer_mfts()
        if 1: #_mft in self.newer_mfts:
            self._tags, cache_write = self.new_data(_mft)
            if cache_write:
                # a new entry was written
                self.newFiles.append(self._tags['Name'])
        return self._tags

    def dir_files_in_mas_files(self, folder):
        """
        Dict of mas files and the files they contain
        """
        masFiles = getListOfFiles(folder, '*.mas')
        _pop = os.getcwd()  # save current directory
        os.chdir(os.path.dirname(masFiles[0][0]))
        files = dict()
        for mas in masFiles:
            # We need to record mas file name as well
            files[mas[1]] = self.dir_files_in_single_mas_file(mas[1])
        os.chdir(_pop)
        return files

    def dir_files_in_single_mas_file(self, mas):
        temporaryFile = os.path.join(r'c:\temp', 'temporaryFile')
        cmd = F'"{self.ModMgr}" -q -l"{mas}" 2>&1 {temporaryFile} > nul 2>&1'.format()
        executeCmdInBatchFile(cmd)

        files = readFile(temporaryFile)
        #os.remove(temporaryFile)
        return files

    def mas_file(self, mas, _filename, tags, keywords):
        """
        Extract file from mas file and add any keywords to tags
        """
        if not mas in self.encrypted_files:
            cmd = '"'+self.ModMgr + '" -q -x"%s" %s > nul 2>&1' \
                % (mas, _filename)
            retcode,rsp = executeCmdInBatchFile(cmd)
            lines = readFile(_filename)
            for line in lines:
                line = line.strip()
                for kw in keywords:
                    if line.startswith(f'{kw}'):
                        tags[kw]=re.split('[= /\t]+', line)[1].strip()
            try:
                os.remove(_filename)   # delete extracted file
            except:
                self.encrypted_files.append(mas)
                print('Failed to extract %s from %s' % (_filename, mas))
        else:
            pass    # Already identified as encrypted
            print()
        return tags

    def new_data(self, _mft, new_cache=False):
        """
        Create new rFactory data entry in the spreadsheet
        new_cache=False:
            First check if there is cached data in the spreadsheet
        Read the tags in the .MFT file
        Read the tags in a set of files in .mas files

        Return
            The tags
            If it was a new entry
        """
        cache_write = False
        _tags = self.get_initial_tags(_mft) # Get the name
        cache_o = Cached_data()
        cache_o.load()
        if new_cache:
            cached_tags = dict()
        else:
            cached_tags = cache_o.get_values(_tags['Name'])
        if not cached_tags:
            # Newly-installed mod
            cache_write = True
            for _tag, _val in _tags.items():
                cached_tags[_tag] = _val
            cached_tags['Rating'] = '***' # Default
            cached_tags = self.read_mas_files(cached_tags, os.path.dirname(_mft))
            for tag, val in cached_tags.items():
                cache_o.set_value(_tags['Name'], tag, val)
            cache_o.write()

        # These aren't kept in the spreadsheet so get the .MFT tags
        cached_tags['Date'] = translate_date(_tags['Date'])
        cached_tags['Desc'] = _tags['Desc']
        cached_tags['Name'] = _tags['Name']
        cached_tags['strippedName'] = _tags['strippedName']

        return cached_tags, cache_write

######################################################################

carCategories = {
  '3' : 'GT',
  '5' : 'Novel',
  '6' : 'Open',
  '7' : 'Prototype',
  '9' : 'Street',
  '10' : 'Touring'
  }

class CarDataFiles(DataFiles):
    def __init__(self):
        self.installed_folder = 'vehicles'
        self.datafiles_folder = os.path.normpath(CarDatafilesFolder)

    def get_initial_tags(self, mft):
        """
        Get the tags from the MFT file
        """
        vehNames = vehFiles()
        text = readFile(mft)
        _tags = getTags(text)
        for requiredTag in ['Name','Version','Type','Author','Origin',
                            'Category','ID','URL','Desc','Date','Flags',
                            'RefCount','#Signature','#MASFile','MinVersion',
                            '#BaseSignature']:
            # MASFile, Signature and BaseSignature filtered out - NO THEY AREN'T,
            # _tags[] still contains them.  tagsToBeWritten filters them out.
            # Not sure what this for loop is, er, for.
            if requiredTag in _tags:
              """filter out boilerplate
              Author=Mod Team
              URL=www.YourModSite.com
              Desc=Your new mod.
              """
              if _tags[requiredTag] in ['Mod Team', 'www.YourModSite.com', 'Your new mod.']:
                _tags[requiredTag] = ''
              if _tags[requiredTag] in ['Slow Motion', 'Slow Motion Modding Group']: # make up your minds boys!
                _tags[requiredTag] = 'Slow Motion Group'
              if _tags[requiredTag] in ['Virtua_LM Modding Team']: # make up your minds boys!
                _tags[requiredTag] = 'Virtua_LM'

              if requiredTag == 'Name':
                _tags['Year'], _tags['Decade'], _tags['strippedName'] = extractYear(_tags['Name'])
                # extract class from name if it's there
                for __class in ['F1','F3','GT3','GTE','BTCC',
                                'LMP1','LMP2','LMP3']: # 'F2' filters rF2...
                  if __class in _tags['Name']:
                    _tags['Class'] = __class
                    _tags['strippedName'] = _tags['strippedName'].replace(__class, '')
                _tags['strippedName'] = _tags['strippedName'].title() # Title Case The Name
        if _tags['Category'] in carCategories:
            _tags['tType'] = carCategories[_tags['Category']]
        # We need the original data folder to assemble the .VEH file path to put in
        # "All Tracks & Cars.cch" to force rF2 to switch cars.  We also need the .VEH
        # file names and that's a bit more difficult.
        # Not difficult, they're in all_vehicles.ini
        _tags['originalFolder'], _ = os.path.split(mft[len(rF2root)+1:]) # strip the root
        # if veh file name is available in vehNames.txt use it
        _tags['vehFile'] = vehNames.veh(_tags['Name'])

        for tag in ['Manufacturer', 'Model']:
            val = _tags['strippedName'].replace('_', ' ').strip()  # default
            if val.startswith('Isi'):
                val = val[4:]
            if val.startswith('Ngtc'):
                val = val[5:]
            if not val == '':
                if tag == 'Manufacturer':
                    val = val.split()[0]
                    # Fix case issues:
                    _mfrs = {'Ac':'AC', 'Ats':'ATS', 'Alfaromeo': 'Alfa Romeo',
                             'Brm':'BRM', 'Bmw':'BMW', 'Mclaren':'McLaren'}
                    if val in _mfrs:
                      val = _mfrs[val]
                if tag == 'Model' and len(val.split()) > 1:
                    val = ' '.join(val.split()[1:])
            _tags[tag] = val
        return _tags

    def read_mas_files(self, tags, mas_dir):
        """
        Open the car mas files and look for
        *.hdv
            ForwardGears=6
            WheelDrive=REAR // which wheels are driven: REAR, FOUR, or FRONT
            SemiAutomatic=0 // whether throttle and clutch are operated automatically (like an F1 car)

            maybe:
            TCSetting=0 ????
            TractionControlGrip=(1.4, 0.2)    // average driven wheel grip multiplied by 1st number, then added to 2nd
            TractionControlLevel=(0.33, 1.0)  // effect of grip on throttle for low TC and high TC
            ABS4Wheel=0                       // 0 = old-style single brake pulse, 1 = more effective 4-wheel ABS
            ABSGrip=(1.7, 0.0)                // grip multiplied by 1st number and added to 2nd
            ABSLevel=(0.31, 0.92)             // effect of grip on brakes for low ABS and high ABS
            Mass=828.0      Weight threshold
            FWRange=(0, 1, 1)             // front wing range
            FWSetting=0                   // front wing setting
            RWRange=(0, 1, 1)             // rear wing range
            RWSetting=0                   // rear wing setting

        (engine)*.ini
            BoostPower=0 no turbo?
            DumpValve=
            Turbo*


        """

        hdv_keywords = [
              'ForwardGears',
              'WheelDrive',
              'SemiAutomatic',
              'Mass',
              'FWSetting',
              'RWSetting'
              ]

        ini_keywords = [
              'DumpValve',
              'Turbo'
              ]

        _dir = self.dir_files_in_mas_files(mas_dir)
        # defaults
        tags['Gearshift'] = 'Paddles' # Paddles or sequential
        tags['F/R/4WD'] = 'REAR'
        tags['Aero'] = '1'
        tags['Turbo'] = '0'

        for mas, files in _dir.items():
            mas = os.path.join(mas_dir, mas)
            for _filename in files:
                _filename = _filename.lower().strip()
                if '.hdv' in _filename:
                    mas_tags = self.mas_file(mas, _filename, {}, hdv_keywords)
                    if 'SemiAutomatic' in mas_tags:
                        if mas_tags['SemiAutomatic'] == '0':
                            tags['Gearshift'] = 'H' + mas_tags['ForwardGears']
                    if 'WheelDrive' in mas_tags:
                        tags['F/R/4WD'] = mas_tags['WheelDrive']
                    if 'FWSetting' in mas_tags and 'RWSetting' in mas_tags:
                        if mas_tags['FWSetting'] == '0' and mas_tags['RWSetting'] == '0':
                            tags['Aero'] = '0'
                    if 'Mass' in mas_tags:
                        tags['Mass'] = str(
                            int(mas_tags['Mass'].split('.')[0])) # May be float
                if '.ini' in _filename:
                    mas_tags = self.mas_file(mas, _filename, {}, ini_keywords)
                    if 'DumpValve' in mas_tags:
                        tags['Turbo'] = '1'

        if not 'Mass' in tags:
            # that PROBABLY indicates that mas was encrypted
            # which PROBABLY => S397
            tags['Mass'] = ''
            if not 'Author' in tags or tags['Author'] == '':
                tags['Author'] = 'Studio 397?'
        return tags


######################################################################

trackCategories = {
  '53' : 'Novel',
  '55' : 'Permanent',
  '56' : 'Rally',
  '57' : 'Temporary'
  }

class TrackDataFiles(DataFiles):
    def __init__(self):
        self.installed_folder = 'locations'
        self.datafiles_folder = os.path.normpath(TrackDatafilesFolder)
    def get_initial_tags(self, mft):
        """
        Get the tags from the MFT file
        """
        text = readFile(mft)
        _tags = getTags(text)
        for requiredTag in ['Name','Version','Type','Author','Origin',
                            'Category','ID','URL','Desc','Date','Flags',
                            'RefCount','#Signature','#MASFile','MinVersion',
                            '#BaseSignature']:
            # MASFile, Signature and BaseSignature filtered out
            if requiredTag in _tags:
              """filter out boilerplate
              Author=Mod Team
              URL=www.YourModSite.com
              Desc=Your new mod.
              """
              if _tags[requiredTag] in ['Mod Team', 'www.YourModSite.com', 'Your new mod.']:
                _tags[requiredTag] = ''
              #print('%s=%s' % (requiredTag, _tags[requiredTag]))
              if requiredTag == 'Name':
                _tags['strippedName'] = cleanTrackName(_tags['Name'])
                _tags['Year'], _tags['Decade'], _tags['strippedName'] = extractYear(_tags['strippedName'])
                _tags['strippedName'] = _tags['strippedName'].title() # Title Case The Name
            # We need the original data folder to assemble the .SCN file path to put in
            # "Player.JSON" to force rF2 to switch tracks.  We also need the .SCN
            # file names and that's a bit more difficult.
            # To select the track we also need the "Scene Description"
            _tags['originalFolder'], _ = os.path.split(mft[len(rF2root)+1:]) # strip the root
            if not 'Scene Description' in _tags or _tags['Scene Description'] == '':
                # if scn file name is available in scnNames.txt use it
                scnNames = getVehScnNames('scnNames.txt')
                if _tags['Name'] in scnNames:
                  _tags['Scene Description'] = scnNames[_tags['Name']]

            if _tags['Category'] in trackCategories:
                _tags['tType'] = trackCategories[_tags['Category']]

            tag = 'Track Name'
            val = _tags['strippedName'].replace('_', ' ').strip()  # default
            _tags[tag] = val
        return _tags

    def read_mas_files(self, tags, mas_dir):
        """
        Open the track mas files and look for
        *.scn - use the name
        *.gdb
            Latitude
            Longitude
        """
        _dir = self.dir_files_in_mas_files(mas_dir)
        for mas, files in _dir.items():
            mas = os.path.join(mas_dir, mas)
            tags = self.read_mas_file(tags, mas, files)
        return tags
    def read_mas_file(self, tags, mas, files):
        """
        Scan track MAS file files for:
        .scns:      use the name
        .gdb files: add tags found in them
        """
        gdb_keywords = [
            'Latitude',
            'Longitude'
            ]
        for _filename in files:
            _filename = _filename.lower().strip()
            if '.scn' in _filename:
                scn = os.path.splitext(_filename)[0] # Strip .scn
                tags['Scene Description'] = scn
                tags['Name'] = scn
            if '.gdb' in _filename:
                tags = self.mas_file(mas, _filename, tags, gdb_keywords)
                # Only if cached_tags don't have it already?
                # (Only called if cached_tags is empty)
                if 'Latitude' in tags and 'Longitude' in tags:
                    lat = float(tags['Latitude'])
                    long = float(tags['Longitude'])
                    address_o = google_address(lat, long)

                    tags['Country'] = address_o.get_country()
                    tags['Continent'] = country_to_continent(tags['Country'])
                else:
                    tags['Country'] = 'No Lat'
                    tags['Continent'] = 'No Long'
        return tags

######################################################################
# Using the classes

def example_list_gearboxes():
    """ Example using the above classes """
    cdf = CarDataFiles()
    tags = dict()
    gearboxes = list()
    mfts_and_timestamps = cdf.get_mfts_and_timestamps()
    for mfts_and_timestamp in mfts_and_timestamps:
        mft = os.path.dirname(mfts_and_timestamp)
        tags = cdf.read_mas_files(tags,mft)
        _car = os.path.basename(mfts_and_timestamp)
        if 'Gearshift' in tags:
            _shift = tags['Gearshift']
        else:
            _shift = '[Unknown]'
        gearboxes.append(f'{_car}\t{_shift}'.format())
        print()
        for _g in gearboxes:
            print(_g)



######################################################################
# Legacy:

def trawl_for_new_rF2_datafiles(parentFrame):
  """ The "do everything" access function """
  filesToDelete = listDeletedDataFiles()
  # THIS SHOULD BE IN THE GUI!
  if len(filesToDelete):
    delete = messagebox.askyesno(
              'Scanned rFactory data files',
              'rFactory data files out of date:\n%s\nDo you want to delete them?\n' % '\n'.join(filesToDelete)
          )
    if delete:
      for file in filesToDelete:
        os.remove(file)

  newFiles = createDefaultDataFiles(overwrite=False) # Create new rFactory data files

  reloadAllData()

  if len(newFiles):
    if len(newFiles) < 10:    # if there are too many forget it
      edit = messagebox.askyesno(
                'Scanned rF2 data files',
                'New rFactory data files created:\n%s\nDo you want to edit them now?\n' % '\n'.join(newFiles)
            )
    else:
      messagebox.askokcancel(
                'Scanned rF2 data files',
                '%s new rFactory data files created. Edit them at some time.\n' % len(newFiles)
            )
      edit = False
    if edit:
      for newFile in newFiles:
        root = tk.Tk()
        tabTrack = ttk.Frame(root, width=1200, height=600, relief='sunken', borderwidth=5)
        root.title('Editor')
        tabTrack.grid()

        fields = carTags
        data = getSingleCarData(id=newFile, tags=fields)
        o_tab = carNtrackEditor.Editor(tabTrack, fields, data, DatafilesFolder=CarDatafilesFolder)
        tk.mainloop()
  return newFiles

######################################################################


def dataFileExists(datafilesPath, filename):
  _filepath = os.path.join(datafilesPath, filename+dataFilesExtension)
  return os.path.exists(_filepath)

def createDataFile(datafilesPath, filename, dict, tagsToBeWritten, overwrite=False):
  _filepath = os.path.join(datafilesPath, filename+dataFilesExtension)
  _newFile = False
  if overwrite or not os.path.exists(_filepath):
      os.makedirs(datafilesPath, exist_ok=True)
      with open(_filepath, "w") as f:
        for tag in tagsToBeWritten:
          if tag in dict:
            val = dict[tag]
          elif tag == 'DB file ID':
            val = filename # The unique identifier for the car/track. I think.
          else: # value not available
            val = ''
          try:
            f.write('%s=%s\n' % (tag, val))
          except OSError:
            print('Failed to write %s' % _filepath)
            quit()
      _newFile = True
  return _newFile

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
        #print(name, year)
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

class vehFiles:
  #[VEHICLE]
  #ID=1
  #File="%ProgramFiles(x86)%\Steam\steamapps\common\rFactor 2\Installed\Vehicles\AC_427SC_1967\1.2\427SC_BLACK.VEH"
  #...

  vehDict = {}
  def __init__(self):
    self.all_vehicles_ini = os.path.join(playerPath, 'all_vehicles.ini')
    all_vehicles_text = readFile(self.all_vehicles_ini)
    for line in all_vehicles_text:
      if line.startswith('File='):
        _path, _veh = os.path.split(line[len('File="'):])
        _path, _rev = os.path.split(_path)
        _path, _car = os.path.split(_path)
        if not _car in self.vehDict:
          self.vehDict[_car] = _veh.strip()[:-1]  # lose the trailing "
  #@property
  def veh(self, carName) :
    try:
      return self.vehDict[carName]
    except:
      print('%s not in %s' % (carName, self.all_vehicles_ini))
    return ''

######################################################################

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

def createDefaultDataFiles(overwrite=False):
  newFiles = []
  getAllTags = False
  rF2_dir = os.path.join(rF2root, 'Installed')
  vehicleFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles'), pattern='*.mft', recurse=True)
  F1_1996_carFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles', 'F1 1996 - SL1DE'), pattern='*.mas', recurse=True)
  F1_2013_carFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles', 'F1RFT_2013_FB_1.4'), pattern='*.mas', recurse=True)
  trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations'), pattern='*.mft', recurse=True)
  F1_1988_trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations', 'F1_1988_Tracks'), pattern='*.mas', recurse=True)
  cdf = CarDataFiles()
  tdf = TrackDataFiles()
  cache_o = Cached_data()
  cache_o.load()

  #vehNames = getVehScnNames('vehNames.txt')
  vehNames = vehFiles()

  tags = {}
  if getAllTags:
    cache_write = True
    for veh in vehicleFiles:
      text = readFile(veh[0])
      for tag in readTags(text):
        tags[tag] = 0
    #print(tags)
  else: # create data file
    cache_write = False
    for veh in vehicleFiles:
      #if veh[1] != 'F1 1996 - SL1DE.mft' and veh[1] != 'F1RFT_2013_FB_1.4.mft':
      text = readFile(veh[0])
      tags = getTags(text)
      if not overwrite and \
          dataFileExists(datafilesPath=CarDatafilesFolder,
                         filename=tags['Name']):
          continue
      ## Need to call get_initial_tags
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
            tags['strippedName'] = tags['strippedName'].title() # Title Case The Name
      if tags['Category'] in carCategories:
        tags['tType'] = carCategories[tags['Category']]
      # We need the original data folder to assemble the .VEH file path to put in
      # "All Tracks & Cars.cch" to force rF2 to switch cars.  We also need the .VEH
      # file names and that's a bit more difficult.
      # Not difficult, they're in all_vehicles.ini
      tags['originalFolder'], _ = os.path.split(veh[0][len(rF2root)+1:]) # strip the root
      # if veh file name is available in vehNames.txt use it
      tags['vehFile'] = vehNames.veh(tags['Name'])

      for tag in ['Manufacturer', 'Model']:
        val = tags['strippedName'].replace('_', ' ').strip()  # default
        if val.startswith('Isi'):
            val = val[4:]
        if val.startswith('Ngtc'):
            val = val[5:]
        if not val == '':
            if tag == 'Manufacturer':
                val = val.split()[0]
                # Fix case issues:
                _mfrs = {'Ac':'AC', 'Ats':'ATS', 'Alfaromeo': 'Alfa Romeo', 'Brm':'BRM', 'Bmw':'BMW', 'Mclaren':'McLaren'}
                if val in _mfrs:
                  val = _mfrs[val]
            if tag == 'Model' and len(val.split()) > 1:
                val = ' '.join(val.split()[1:])
        tags[tag] = val

      cached_tags = cache_o.get_values(tags['Name'])
      cache_write = False
      if not cached_tags:
          # We don't already have data scanned from MAS files

          """
          Legacy
          __scn, mas_tags = getMasInfo(
                os.path.join(rF2root, tags['originalFolder']))
          """
          mas_tags = cdf.read_mas_files(tags,
                os.path.join(rF2root, tags['originalFolder']))
          if 'SemiAutomatic' in mas_tags:
              if mas_tags['SemiAutomatic'] == '0':
                tags['Gearshift'] = 'H' + mas_tags['ForwardGears']
              else: # Paddles or sequential
                tags['Gearshift'] = 'Paddles'
          if 'WheelDrive' in mas_tags:
                tags['F/R/4WD'] = mas_tags['WheelDrive']
          tags['Aero'] = 1
          if 'FWSetting' in mas_tags and 'RWSetting' in mas_tags:
                if mas_tags['FWSetting'] == '0' and mas_tags['RWSetting'] == '0':
                    tags['Aero'] = 0
          if 'DumpValve' in mas_tags:
                tags['Turbo'] = '1'
          else:
                tags['Turbo'] = '0'
          if 'Mass' in mas_tags:
                try:
                    tags['Mass'] = int(mas_tags['Mass'].split('.')[0]) # May be float
                except:
                    tags['Mass'] = ''
          else: # that probably indicates that mas was encrypted => S397
                tags['Mass'] = ''
                if tags['Author'] == '':
                    tags['Author'] = 'Studio 397?'
                if not 'Gearshift' in tags or tags['Gearshift'] == '':
                    tags['Gearshift'] = 'Paddles'
                if not 'F/R/4WD' in tags or tags['F/R/4WD'] == '':
                    tags['F/R/4WD'] = 'REAR'
          for tag in ['Gearshift','F/R/4WD','Aero','Turbo','Mass','Author']:
            if tag in tags:
              cache_o.set_value(tags['Name'], tag, tags[tag])
          cache_write = True


      for tag in carTags:
        if cached_tags and tag in cached_tags:
          if cached_tags[tag] != '':
            # We have a cached tag for this one
            tags[tag] = cached_tags[tag]
          elif tag in tags:
            cache_o.set_value(tags['Name'], tag, tags[tag])
            cache_write = True

      if createDataFile(datafilesPath=CarDatafilesFolder,
                        filename=tags['Name'],
                        dict=tags,
                        tagsToBeWritten=carTags,
                        overwrite=overwrite):
        # a new file was written
        newFiles.append(tags['Name'])
  if cache_write:
      cache_o.write()

  #print('\n\nTracks:')
  tags = {}
  if getAllTags:
    for track in trackFiles:
      text = readFile(track[0])
      for tag in readTags(text):
        tags[tag] = 0
    #print(tags)
  else: # create data file
    for track in trackFiles:
      text = readFile(track[0])
      tags = getTags(text)
      ## Need to call get_initial_tags
      if track[1] != 'F1_1988_Tracks.mft':
        _markerfilepath = os.path.join(TrackDatafilesFolder,
                                       tags['Name']+markerfileExtension)
        if overwrite or not os.path.exists(_markerfilepath):
          # Create a marker file with the overall name
          # otherwise this scans for SCN files every time
          createMarkerFile(_markerfilepath)
          """
          Legacy
          scns, mas_tags = getMasInfo(os.path.dirname(track[0]))
          """
          mas_tags = tdf.read_mas_files(tags,
                os.path.dirname(track[0]))
          scn = tags['Name']
          if len(scn):
              tags['Scene Description'] = scn
              tags['Name'] = scn
              tags['Track Name'] = scn
              tags['Date'] = translate_date(tags['Date'])
              newTrack = processTrack(track, tags, mas_tags)
              if newTrack:
                newFiles.append(newTrack)

          else:
            newTrack = processTrack(track, tags, mas_tags)
            if newTrack:
              newFiles.append(newTrack)

      else: # it's a folder of several tracks
        for track in F1_1988_trackFiles:
          tags['Name'] = track[1][:-4]
          _filepath = os.path.join(TrackDatafilesFolder, tags['Name']+dataFilesExtension)
          if overwrite or not os.path.exists(_filepath):
            """
            Legacy
            scns, mas_tags = getMasInfo(None, track[0])
            scns = tags['Name']
            tags['Scene Description'] = tags['Name']
            """
            files = tdf.dir_files_in_single_mas_file(track[0])
            mas_tags = tdf.read_mas_file(tags, track[0], files)
            newTrack = processTrack(track, tags, mas_tags)
            if newTrack:
              newFiles.append(newTrack)
  return newFiles

def processTrack(track, tags, mas_tags=None):
  #print('\nData file: "%s.something"' % tags['Name'])
  cache_o = Cached_data()
  cache_o.load()

  # SNIPPED
  cached_tags = cache_o.get_values(tags['Name'])
  cache_write = False


  if cached_tags:
    for tag in cached_tags:
      if cached_tags[tag] != '':
        # We have a cached tag for this one
        tags[tag] = cached_tags[tag]
      elif tag in tags:
        cache_o.set_value(tags['Name'], tag, tags[tag])
        cache_write = True

  if cache_write:
      cache_o.write()

  if createDataFile(datafilesPath=TrackDatafilesFolder,
                    filename=tags['Name'],
                    dict=tags,
                    tagsToBeWritten=trackTags):
    # a new file was written
    return tags['Name']
  return None

def createMarkerFile(filepath):
  """ Create a file to mark that a track folder has been processed """
  writeFile(filepath,
            'This marks that the track folder has been processed.\n'
            'No need to scan for SCN files again.')

def listDeletedDataFiles():
  """
  Get a list of rFactory data files that no longer have a corresponding
  rF2 Installed.... folder
  """
  newFiles = []
  rF2_dir = os.path.join(rF2root, 'Installed')
  rFactoryVehicleFiles = getListOfFiles('CarDatafiles',
                                        pattern='*.txt', recurse=False)
  rFactoryTrackFiles = getListOfFiles('TrackDatafiles',
                                      pattern='*.txt', recurse=False)

  filesToDelete = []
  for car in rFactoryVehicleFiles:
    _data = readFile(car[0])
    for line in _data:
      if line.startswith('originalFolder'):
        _f = line[len('originalFolder='):-1]
        if not os.path.isdir(os.path.join(rF2root, _f)):
          filesToDelete.append(car[0])
  for track in rFactoryTrackFiles:
    _data = readFile(track[0])
    for line in _data:
      if line.startswith('originalFolder'):
        _f = line[len('originalFolder='):-1]
        if not os.path.isdir(os.path.join(rF2root, _f)):
          filesToDelete.append(track[0])
  return filesToDelete


if __name__ == '__main__':
  root = tk.Tk()
  tabCar = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabCar.grid()

  """ Legacy
  scns, mas_tags = getMasInfo(r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\BATHURST_2016_V3\3.0" )
  """

  #createDefaultDataFiles(overwrite=True)
  newFiles = trawl_for_new_rF2_datafiles(root)
  #if newFiles != []:
  #  root.mainloop()

  rF2_dir = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed"
  vehicleFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles'), pattern='*', recurse=False)

  car_scn, mas_dict = getMasInfo(r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\ferrari_312_67\1.2")
  print(mas_dict)

  cdf = CarDataFiles()
  tags = dict()
  mft = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\ASR_OWC_1990_641-2\1.73"
  tags = cdf.read_mas_files(tags,mft)

  example_list_gearboxes()
  """

  mas_list = list()
  for vehicleFile in vehicleFiles:
      folder = getListOfFiles(vehicleFile[0], pattern='*')[0][0]
      car_scn, mas_dict = getMasInfo(folder)
      mas_list.append(mas_dict)
  """
  pass
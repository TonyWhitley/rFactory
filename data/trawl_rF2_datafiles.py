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
3) Some tags ALWAYS come from MFT files
    Version
    Date
    others?
4) MAS files are slower to read
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
import time

import tkinter as tk
from tkinter import ttk

from data.rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,playerPath, carCacheDataFile, trackCacheDataFile, unusableMasFilesFile
from data.utils import getListOfFiles, readFile, writeFile, getTags, executeCmdInBatchFile

from data.LatLong2Addr import google_address, country_to_continent
from data.cached_data import Cached_data


######################################################################
#
# Utility functions:


def translate_date(val):
    """
    Convert Windows or Unix datetime to YYYY-MM-DD
    """
    try:
        if len(val) == 18:  # Windows filetime.
            # http://support.microsoft.com/kb/167296
            # How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
            EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
            HUNDREDS_OF_NANOSECONDS = 10000000
            ts = datetime.datetime.fromtimestamp(
                (int(float(val)) - EPOCH_AS_FILETIME) // HUNDREDS_OF_NANOSECONDS)
        else:  # Unix
            ts = datetime.datetime.fromtimestamp(int(float(val)))
    except Exception as e:
        print(e)
        ts = datetime.datetime.today()
    return ts.strftime("%Y-%m-%d")


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
                return year, decade, name.replace(y, '')
        for y in _years:
            if len(y) == 2:
                if y[0] in '01':
                    year = '20' + y
                else:
                    year = '19' + y
                decade = year[:3] + '0-'
                return year, decade, name.replace(y, '')
    #print(name, year)
    return year, decade, name


def parse_mfr_model(_tags):
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
                _mfrs = {'Ac': 'AC', 'Ats': 'ATS', 'Alfaromeo': 'Alfa Romeo',
                         'Brm': 'BRM', 'Bmw': 'BMW', 'Mclaren': 'McLaren'}
                if val in _mfrs:
                    val = _mfrs[val]
            if tag == 'Model' and len(val.split()) > 1:
                val = ' '.join(val.split()[1:])
        _tags[tag] = val
    return _tags


def parse_name(_tags):
    _tags['Year'], _tags['Decade'], _tags['strippedName'] = extractYear(
        _tags['Name'])
    # extract class from name if it's there
    for __class in ['F1', 'F3', 'GT3', 'GTE', 'BTCC',
                    'LMP1', 'LMP2', 'LMP3']:  # 'F2' filters rF2...
        if __class in _tags['Name']:
            _tags['Class'] = __class
            _tags['strippedName'] = _tags['strippedName'].replace(__class, '')
    if _tags['strippedName'].startswith('STK'):
        _tags['Author'] = 'Simtek Mods'
    # extract certain words from name if they're there
    for __word in ['FIA', 'OWC', 'HE', '96', 'MAIN', '88', 'C4']:
        if __word in _tags['Name'] and '488' not in _tags['Name']:
            _tags['strippedName'] = _tags['strippedName'].replace(__word, '')
    _tags['strippedName'] = _tags['strippedName'].title()  # Title Case The Name
    return _tags

######################################################################
# Common Car/Track subclass:


class DataFiles:
    installed_folder = None
    datafiles_folder = None
    mfts_and_timestamps = None
    data_files_and_timestamps = None
    newer_mfts = None
    newFiles = list()
    _tags = dict()
    cache_o = None
    unusable_mas_files, error = readFile(unusableMasFilesFile)
    if error:
        unusable_mas_files = list()
    ModMgr = os.path.join(rF2root, r'Bin32\ModMgr.exe')

    def __getitem__(self, key):
        return self._tags[key]

    def __setitem__(self, key, value):
        """
        Only set tag if it does not already have a value
        """
        if type(value) != str:
            raise TypeError("tag must be string")
        if key not in self._tags or self._tags[key] == '':
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

    def find_single_mod_folders(self):
        """
        Find ALL folders with .MFT files then subtract multi-mod folders

        Looks like none of the multifold

        rF2 installed_folder: 'vehicles' or 'locations'
        """
        rF2_dir = os.path.join(rF2root, 'Installed')
        all_mfts = getListOfFiles(os.path.join(rF2_dir,
                                               self.installed_folder),
                                  pattern='*.mft',
                                  recurse=True)
        self.multis, multi_mfts = self.find_multi_mod_folders()
        # all_mfts, list of folder, mft tuples
        # self.multis, list of folders
        # multi_mfts, list of folder, mft tuples
        for mmft in multi_mfts:
            for i, mft in enumerate(all_mfts):
                if mft[1] == mmft[1]:
                    del all_mfts[i]
        return all_mfts

    def find_multi_mod_folders(self):
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
        multi_mfts = list()
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
                    _mft_files = getListOfFiles(_rev[0],
                                                pattern='*.mft',
                                                recurse=True)
                    multi_mfts += _mft_files
        pass
        return multi_mas, multi_mfts

    def get_mfts_and_timestamps(self):
        """
        rF2 installed_folder: 'vehicles' or 'locations'
        """
        rF2_dir = os.path.join(rF2root, 'Installed')
        _mft_files = getListOfFiles(
            os.path.join(
                rF2_dir,
                self.installed_folder),
            pattern='*.mft',
            recurse=True)
        self.mfts_and_timestamps = dict()
        for folder in _mft_files:
            _folder = folder[0].lower()  # os.path.dirname(
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
        """
        Get a list of MFT files that haven't been processed before or are a
        new version
        """
        if not self.mfts_and_timestamps:
            self.get_mfts_and_timestamps()
        if not self.data_files_and_timestamps:
            self.get_data_files_and_timestamps()

        self.newer_mfts = list()
        for folder, timestamp in self.mfts_and_timestamps.items():
            # nope, we need to make
            # c:\Users\tony_\source\repos\rFactory\dataFiles\Cars\USF2000_2016.rFactory.txt
            _datafile = self.make_datafile_name(folder)
            if _datafile in self.data_files_and_timestamps:
                if timestamp > self.data_files_and_timestamps[_datafile]:
                    self.newer_mfts.append(folder)
            else:
                self.newer_mfts.append(folder)
        return self.newer_mfts

    def dir_files_in_mas_files(self, folder):
        """
        Dict of mas files and the files they contain
        """
        masFiles = getListOfFiles(folder, '*.mas')
        _pop = os.getcwd()  # save current directory
        files = dict()
        if masFiles:
            os.chdir(os.path.dirname(masFiles[0][0]))
            for mas in masFiles:
                # We need to record mas file name as well
                files[mas[1]] = self.dir_files_in_single_mas_file(mas[1])
            os.chdir(_pop)
        return files

    def dir_files_in_single_mas_file(self, mas):
        files = list()
        if not mas + '\n' in self.unusable_mas_files:
            temporaryFile = os.path.join(r'c:\temp', 'temporaryFile')
            cmd = F'"{self.ModMgr}" -q -l"{mas}" 2>&1 {temporaryFile} > nul 2>&1'.format()
            executeCmdInBatchFile(cmd)

            files, error = readFile(temporaryFile)
            try:
                os.remove(temporaryFile)
            except BaseException:
                pass    # temp file wasn't created
        return files

    def mas_file(self, mas, _filename, tags, keywords):
        """
        Extract file from mas file and add any keywords to tags
        """
        if not mas + '\n' in self.unusable_mas_files:
            cmd = '"' + self.ModMgr + '" -q -x"%s" "%s" > nul 2>&1' \
                % (mas, _filename)
            retcode, rsp = executeCmdInBatchFile(cmd)
            lines, error = readFile(_filename)
            for line in lines:
                line = line.strip()
                for kw in keywords:
                    if line.startswith(f'{kw}'):
                        _val = re.split('[= /\t]+', line)[1].strip()
                        # Hacking to write tyre names to a file
                        if '.tbc' in _filename:
                            _filepath = "c:/temp/rf2_tyres.txt"
                            with open(_filepath, "a") as f:
                                f.writelines(['MAS file: %s  Tyre name: %s\n' % (mas, line)])
                        tags[kw] = _val
            try:
                os.remove(_filename)   # delete extracted file
            except BaseException:
                self.unusable_mas_files.append(mas + '\n')
                writeFile(unusableMasFilesFile, self.unusable_mas_files)
                print('Failed to extract %s from %s' % (_filename, mas))
        else:
            pass    # Already identified as encrypted
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
        _mft_tags = self._get_mft_tags(_mft)  # Get the name
        cached_tag_name = _mft_tags['Name']
        if 'Date' in _mft_tags:
            _mft_tags['Date'] = translate_date(_mft_tags['Date'])
        else:
            _mft_tags['Date'] = ''

        if new_cache:
            cached_tags = dict()
        else:
            cached_tags = self.cache_o.get_values(cached_tag_name)
        if not cached_tags:
            # Newly-installed mod
            cache_write = True
            for _tag, _val in _mft_tags.items():
                cached_tags[_tag] = _val
            cached_tags['Rating'] = '***'  # Default
            cached_tags = self.read_mas_files(
                cached_tags, os.path.dirname(_mft))
            for tag, val in cached_tags.items():
                self.cache_o.set_value(cached_tag_name, tag, val)

        for tag, val in _mft_tags.items():
            self.cache_o.set_value(cached_tag_name, tag, val)

        for _tag in ['Desc', 'Name', 'strippedName']:
            if _tag in _mft_tags:
                cached_tags[_tag] = _mft_tags[_tag]
            else:
                cached_tags[_tag] = ''

        return cached_tags, cache_write

    def multi_mod(self, folder):
        """
        Multiple mods in one folder with a single MFT file

        Generator function, returns one mod each time
        Generator version broke when run in VS debugger, OK when run as Python file or exe
        for _tags, cache_write in tdf.multi_mod(folder):
        """

        rF2_dir = os.path.join(rF2root, 'Installed')
        mft_files = getListOfFiles(
            os.path.join(
                rF2_dir,
                self.installed_folder,
                folder),
            pattern='*.mft',
            recurse=True)
        mas_files = getListOfFiles(
            os.path.join(
                rF2_dir,
                self.installed_folder,
                folder),
            pattern='*.mas',
            recurse=True)

        results = list()
        for _mod in mas_files:
            cache_write = False
            _mft_tags = self._get_mft_tags(mft_files[0][0])  # Get the name
            if 'Date' in _mft_tags:
                _mft_tags['Date'] = translate_date(_mft_tags['Date'])
            else:
                _mft_tags['Date'] = ''

            _mft_tags['Name'] = _mod[1][:-4]
            cached_tag_name = _mft_tags['Name']
            cached_tags = self.cache_o.get_values(cached_tag_name)
            if not cached_tags:
                # Newly-installed mod
                files = self.dir_files_in_single_mas_file(_mod[0])
                if 'Track Name' in _mft_tags:
                    del _mft_tags['Track Name']
                for _tag, _val in _mft_tags.items():
                    cached_tags[_tag] = _val
                cached_tags['Rating'] = '***'  # Default
                cached_tags, cache_write = self._read_mas_file(
                    cached_tags, _mod[0], files)
                if cache_write:
                    cached_tags['strippedName'] = cached_tags['Name']
                    cached_tags = parse_name(cached_tags)
                    cached_tags = parse_mfr_model(cached_tags)
                    for tag, val in cached_tags.items():
                        self.cache_o.set_value(cached_tag_name, tag, val)
                    if 'Latitude' in cached_tags:
                        # It's a track
                        tag = 'Track Name'
                        val = cached_tags['strippedName'].replace(
                            '_', ' ').strip()
                        cached_tags[tag] = val
                        self.cache_o.set_value(cached_tag_name, tag, val)
                else:
                    if not _mod[0] + '\n' in self.unusable_mas_files:
                      self.unusable_mas_files.append(_mod[0] + '\n')
                      writeFile(unusableMasFilesFile, self.unusable_mas_files)

            if cache_write:
                for tag, val in _mft_tags.items():
                    self.cache_o.set_value(cached_tag_name, tag, val)

            for _tag in []:  # ['Desc', 'Name', 'strippedName']:
                if _tag in _mft_tags:
                    cached_tags[_tag] = _mft_tags[_tag]
            results.append([cached_tags, cache_write])
        return results

    def cache_write(self):
        """
        Write any new data to the spreadsheet
        """
        self.cache_o.write()

    def get_tags(self):
        self.cache_o.l

    def read_mas_files(self, tags, mas_dir):
        return dict() # Pylint - it's defined in subclass
    def _read_mas_file(self, tags, mas, files):
        return dict() # Pylint - it's defined in subclass
    def _get_mft_tags(self, mft):
        return dict() # Pylint - it's defined in subclass


    '''
    def get_data(self, _mft):
        """
        Get tags from MFT file
        """
        _mft = _mft.lower()

        if not self.newer_mfts:
            self.get_newer_mfts()
        if 1: #_mft in self.newer_mfts:
            self._tags, cache_write = self.new_data(_mft)
            if cache_write:
                # a new entry was written
                self.cache_o.write()
                self.newFiles.append(self._tags['Name'])
        return self._tags
    '''

######################################################################
#
#  Car specific:


carCategories = {
    '3': 'GT',
    '5': 'Novel',
    '6': 'Open',
    '7': 'Prototype',
    '9': 'Street',
    '10': 'Touring'
}


class CarDataFiles(DataFiles):
    def __init__(self):
        self.installed_folder = 'vehicles'
        self.datafiles_folder = os.path.normpath(CarDatafilesFolder)
        self.vehNames = vehFiles()  # Repeatedly reading this slows things down A LOT
        self.cache_o = Cached_data(carCacheDataFile, carTags)
        self.cache_o.load()

    def _get_mft_tags(self, mft):
        """
        Get the tags from the MFT file
        """
        text, error = readFile(mft)
        if error:
            return dict()
        _tags = getTags(text)
        for requiredTag in ['Name', 'Version', 'Type', 'Author', 'Origin',
                            'Category', 'ID', 'URL', 'Desc', 'Date', 'Flags',
                            'RefCount', '#Signature', '#MASFile', 'MinVersion',
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
                if _tags[requiredTag] in [
                    'Mod Team',
                    'www.YourModSite.com',
                        'Your new mod.']:
                    _tags[requiredTag] = ''
                if _tags[requiredTag] in ['Slow Motion',
                                           'Slow Motion Modding Group']: # make up your minds boys!
                    _tags[requiredTag] = 'Slow Motion Group'
                if _tags[requiredTag] in [
                        'Virtua_LM Modding Team']:  # make up your minds boys!
                    _tags[requiredTag] = 'Virtua_LM'

        if _tags['Category'] in carCategories:
            _tags['tType'] = carCategories[_tags['Category']]
        # We need the original data folder to assemble the .VEH file path to put in
        # "All Tracks & Cars.cch" to force rF2 to switch cars.  We also need the .VEH
        # file names and that's a bit more difficult.
        # Not difficult, they're in all_vehicles.ini
        _tags['originalFolder'], _ = os.path.split(
            mft[len(rF2root) + 1:])  # strip the root
        # if veh file name is available in vehNames.txt use it
        _tags['vehFile'] = self.vehNames.veh(_tags['Name'])

        _tags = parse_name(_tags)
        _tags = parse_mfr_model(_tags)
        return _tags

    def _read_mas_file(self, tags, mas, files):
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

        *.tbc
            [COMPOUND]
            Name="Bias-Ply"
            but not
            [SLIPCURVE]
            Name="Lat"



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

        found = False
        for _filename in files:
            _filename = _filename.lower().strip()
            if '.hdv' in _filename:
                mas_tags = self.mas_file(mas, _filename, {}, hdv_keywords)
                if 'SemiAutomatic' in mas_tags:
                    if mas_tags['SemiAutomatic'] == '0':
                        tags['Gearshift'] = 'H' + mas_tags['ForwardGears']
                        found = True
                if 'WheelDrive' in mas_tags:
                    tags['F/R/4WD'] = mas_tags['WheelDrive']
                    found = True
                if 'FWSetting' in mas_tags and 'RWSetting' in mas_tags:
                    if mas_tags['FWSetting'] == '0' and mas_tags['RWSetting'] == '0':
                        tags['Aero'] = '0'
                        found = True
                if 'Mass' in mas_tags:
                    tags['Mass'] = str(
                        int(mas_tags['Mass'].split('.')[0]))  # May be float
                    found = True
            if '.ini' in _filename:
                mas_tags = self.mas_file(mas, _filename, {}, ini_keywords)
                if 'DumpValve' in mas_tags:
                    tags['Turbo'] = '1'
                    found = True
            # Hacking to get an idea of tyre names:
            if '.tbc' in _filename:
                mas_tags = self.mas_file(mas, _filename, {}, ['Name'])

        if 'Mass' not in tags:
            # that PROBABLY indicates that mas was encrypted
            # which PROBABLY => S397
            tags['Mass'] = ''
            if 'Author' not in tags or tags['Author'] == '':
                tags['Author'] = 'Studio 397?'
        return tags, found

    def read_mas_files(self, tags, mas_dir):
        """
        Scan car MAS files for:
        .hdv files: add tags found in them
        (engine)*.ini DumpValve tag
        """
        # defaults
        tags['Gearshift'] = 'Paddles'  # Paddles or sequential
        tags['F/R/4WD'] = 'REAR'
        tags['Aero'] = '1'
        tags['Turbo'] = '0'

        _dir = self.dir_files_in_mas_files(mas_dir)
        for mas, files in _dir.items():
            mas = os.path.join(mas_dir, mas)
            tags, found = self._read_mas_file(tags, mas, files)
        return tags


######################################################################
#
# Track specific:

trackCategories = {
    '53': 'Novel',
    '55': 'Permanent',
    '56': 'Rally',
    '57': 'Temporary'
}


class TrackDataFiles(DataFiles):
    def __init__(self):
        self.installed_folder = 'locations'
        self.datafiles_folder = os.path.normpath(TrackDatafilesFolder)
        self.vehNames = None  # (only used for car files)
        self.cache_o = Cached_data(
            trackCacheDataFile, trackTags + ['Longitude', 'Latitude'])
        self.cache_o.load()

    def _get_mft_tags(self, mft):
        """
        Get the tags from the MFT file
        """
        text, error = readFile(mft)
        _tags = getTags(text)
        for requiredTag in ['Name', 'Version', 'Type', 'Author', 'Origin',
                            'Category', 'ID', 'URL', 'Desc', 'Date', 'Flags',
                            'RefCount', '#Signature', '#MASFile', 'MinVersion',
                            '#BaseSignature']:
            # MASFile, Signature and BaseSignature filtered out
            if requiredTag in _tags:
                """filter out boilerplate
                Author=Mod Team
                URL=www.YourModSite.com
                Desc=Your new mod.
                """
                if _tags[requiredTag] in [
                    'Mod Team',
                    'www.YourModSite.com',
                        'Your new mod.']:
                    _tags[requiredTag] = ''
                #print('%s=%s' % (requiredTag, _tags[requiredTag]))
                if requiredTag == 'Name':
                    _tags['strippedName'] = cleanTrackName(_tags['Name'])
                    _tags['Year'], _tags['Decade'], _tags['strippedName'] = extractYear(
                        _tags['strippedName'])
                    # Title Case The Name
                    _tags['strippedName'] = _tags['strippedName'].title()
            # We need the original data folder to assemble the .SCN file path to put in
            # "Player.JSON" to force rF2 to switch tracks.  We also need the .SCN
            # file names and that's a bit more difficult.
            # To select the track we also need the "Scene Description"
            _tags['originalFolder'], _ = os.path.split(
                mft[len(rF2root) + 1:])  # strip the root
            if 'Scene Description' not in _tags or _tags['Scene Description'] == '':
                    # if scn file name is available in scnNames.txt use it
                scnNames = getVehScnNames('scnNames.txt')
                if 'Name' in _tags and _tags['Name'] in scnNames:
                    _tags['Scene Description'] = scnNames[_tags['Name']]
                else:
                    _tags['Name'] = 'No track name'


            if 'Category' in _tags and _tags['Category'] in trackCategories:
                _tags['tType'] = trackCategories[_tags['Category']]

            tag = 'Track Name'
            if 'strippedName' in _tags:
                val = _tags['strippedName'].replace('_', ' ').strip()  # default
                _tags[tag] = val
            else:
                _tags[tag] = 'No track name'
        return _tags

    def read_mas_files(self, tags, mas_dir):
        """
        Scan track MAS files for:
        .scns:      use the name
        .gdb files: add tags found in them
        """
        _dir = self.dir_files_in_mas_files(mas_dir)
        for mas, files in _dir.items():
            mas = os.path.join(mas_dir, mas)
            tags, found = self._read_mas_file(tags, mas, files)
        return tags

    def _read_mas_file(self, tags, mas, files):
        """
        Open the track MAS files and look for
        *.scn - use the name
        *.gdb
            Latitude
            Longitude
        """
        gdb_keywords = [
            'Latitude',
            'Longitude'
        ]

        found = False
        for _filename in files:
            _filename = _filename.lower().strip()
            if '.scn' in _filename:
                scn = os.path.splitext(_filename)[0]  # Strip .scn
                tags['Scene Description'] = scn
                tags['Name'] = scn
                found = True
            if '.gdb' in _filename:
                tags = self.mas_file(mas, _filename, tags, gdb_keywords)
                # Only if cached_tags don't have it already?
                # (Only called if cached_tags is empty)
                if 'Latitude' in tags and 'Longitude' in tags:
                    lat = float(tags['Latitude'])
                    long = float(tags['Longitude'])
                    address_o = google_address(lat, long)

                    tags['Country'] = address_o.get_country()
                    found = True
                    if tags['Country'] == '':
                        tags['Country'] = 'Lat ' + tags['Latitude']
                        tags['Continent'] = 'Long ' + tags['Longitude']
                    else:
                        tags['Continent'] = country_to_continent(
                            tags['Country'])
                else:
                    if 'Latitude' in tags:
                        tags['Country'] = 'Lat ' + tags['Latitude']
                        tags['Continent'] = '--No Long--'
                        found = True
                    if 'Longitude' in tags:
                        tags['Country'] = '--No Lat--'
                        tags['Continent'] = 'Long ' + tags['Longitude']
                        found = True
        return tags, found

######################################################################
#
# all_vehicles.ini specific


class vehFiles:
    """ Read a .VEH file name from all_vehicles.ini """
    # [VEHICLE]
    # ID=1
    #File="%ProgramFiles(x86)%\Steam\steamapps\common\rFactor 2\Installed\Vehicles\AC_427SC_1967\1.2\427SC_BLACK.VEH"
    # ...

    vehDict = {}

    def __init__(self):
        self.all_vehicles_ini = os.path.join(playerPath, 'all_vehicles.ini')
        all_vehicles_text, error = readFile(self.all_vehicles_ini)
        for line in all_vehicles_text:
            if line.startswith('File='):
                _path, _veh = os.path.split(line[len('File="'):])
                _path, _rev = os.path.split(_path)
                _path, _car = os.path.split(_path)
                if _car not in self.vehDict:
                    # lose the trailing "
                    self.vehDict[_car] = _veh.strip()[:-1]
    # @property

    def veh(self, carName):
        try:
            return self.vehDict[carName]
        except BaseException:
            print('%s not in %s' % (carName, self.all_vehicles_ini))
        return ''

######################################################################


def getVehScnNames(dataFilepath):
    """
    Read the data file containing Name xxxxx.veh pairs
    Also for xxxxx.scn pairs
    """
    _dict = {}
    text, error = readFile(dataFilepath)
    for line in text:
        if line.startswith('#'):
            continue  # comment line
        _split = line.split()
        if len(_split) == 2:
            name, vehScn = _split
            _dict[name] = vehScn
    return _dict

######################################################################
#
# Using the classes:


def createDefaultDataFiles(overwrite=False):
    """
    Find any NEW mods
    """
    newFiles = list()
    rF2_dir = os.path.join(rF2root, 'Installed')

    cdf = CarDataFiles()
    vehicleFiles = cdf.find_single_mod_folders()
    multifolders, multimfts = cdf.find_multi_mod_folders()

    for _veh in vehicleFiles:  # [:2]:
        _tags, cache_write = cdf.new_data(_veh[0])
        if cache_write:
            newFiles.append(_veh[1])
            cdf.cache_write()

    for folder in multifolders:
        results = cdf.multi_mod(folder)
        for _tags, cache_write in results:
            if cache_write:
                cdf.cache_write()
        """
        Generator version broke when run in VS debugger, OK when run as Python file or exe
        for _tags, cache_write in cdf.multi_mod(folder):
            if cache_write:
                cdf.cache_write()
        """

    tdf = TrackDataFiles()
    trackFiles = tdf.find_single_mod_folders()
    multifolders, multimfts = tdf.find_multi_mod_folders()

    for _track in trackFiles:  # [:2]:
        _tags, cache_write = tdf.new_data(_track[0])
        if cache_write:
            newFiles.append(_track[1])

    for folder in multifolders:
        results = tdf.multi_mod(folder)
        for _tags, cache_write in results:
            if cache_write:
                tdf.cache_write()
        """
        Generator version broke when run in VS debugger, OK when run as Python file or exe
        for _tags, cache_write in tdf.multi_mod(folder):
            if cache_write:
                tdf.cache_write()
        """
    return newFiles

######################################################################


def example_list_gearboxes():
    """ Example using the above classes """
    cdf = CarDataFiles()
    tags = dict()
    gearboxes = list()
    mfts_and_timestamps = cdf.get_mfts_and_timestamps()
    for mfts_and_timestamp in mfts_and_timestamps:
        mft = os.path.dirname(mfts_and_timestamp)
        tags = cdf.read_mas_files(tags, mft)
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
#
# Legacy interface


def trawl_for_new_rF2_datafiles(blah):
    createDefaultDataFiles()
######################################################################


if __name__ == '__main__':
    root = tk.Tk()
    tabCar = ttk.Frame(
        root,
        width=1200,
        height=1200,
        relief='sunken',
        borderwidth=5)
    tabCar.grid()

    if 0:
        cdf = CarDataFiles()
        tags = dict()
        mas_dir = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\ASR_OWC_1990_641-2\1.74"
        mft = os.path.join(mas_dir, 'ASR_OWC_1990_641-2.mft')

        mft_tags, __cache_write = cdf.new_data(mft)
        tags = cdf.read_mas_files(mft_tags, mas_dir)

    createDefaultDataFiles()

    example_list_gearboxes()
    """

  mas_list = list()
  for vehicleFile in vehicleFiles:
      folder = getListOfFiles(vehicleFile[0], pattern='*')[0][0]
      car_scn, mas_dict = getMasInfo(folder)
      mas_list.append(mas_dict)
  """
    pass

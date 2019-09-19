"""
Read from a CSV file data already determined for various cars and tracks.
Also functions to create and update that data.
End user program references this data when scanning user's car and track files.
"""

import csv
import os

from data.rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension,markerfileExtension,CacheDataFile
from data.utils import getListOfFiles, readFile, writeFile, getTags

from data.rFactoryData import getSingleCarData, reloadAllData
from data.LatLong2Addr import google_address, country_to_continent

class Cached_data:
    cache = []
    cache_tags = list(set(carTags + trackTags)) # dedupe union of all tags

    def __init__(self, cache_filename=CacheDataFile):
        self.cache_filename = cache_filename

    def load(self):
        """ Load the cached data CSV """
        if os.path.isfile(self.cache_filename):
            with open(self.cache_filename, mode='r') as csv_file:
                for row in csv.DictReader(csv_file):
                    self.cache.append(row)
        else:
            self.cache = []

    def set_value(self, id, key, value):
        """ Set a value in one row of the dict """
        if key in self.cache_tags:
            for row in self.cache:
                if row['DB file ID'] == id:
                    row[key] = value
                    return
            # New entry
            self.__new_entry(id)
            # Newly appended so it will be the last
            self.cache[-1][key] = value

    def __new_entry(self, id):
        row = {}
        for tag in self.cache_tags:
            row[tag] = ''
        row['DB file ID'] = id
        self.cache.append(row)

    def get_values(self, id):
        for row in self.cache:
            if row['DB file ID'] == id:
                return row
        # No such entry
        return None

    def write(self):
        with open(self.cache_filename, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.cache_tags)
            writer.writeheader()
            for row in self.cache:
                writer.writerow(row)


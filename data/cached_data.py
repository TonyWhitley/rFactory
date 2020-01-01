"""
Read from a CSV file data already determined for various cars and tracks.
Also functions to create and update that data.
End user program references this data when scanning user's car and track files.
"""

import csv
import os

from data.rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension,markerfileExtension
from data.utils import getListOfFiles, readFile, writeFile, getTags

from data.LatLong2Addr import google_address, country_to_continent

class Cached_data:
    cache = []
    cache_tags_set = set(carTags + trackTags) # dedupe union of all tags
    cache_tags_set.discard('DB file ID') # Remove to move to col 1
    cache_tags_set.discard('Desc')      # Move to the end because it's verbose
    #cache_tags_set.discard('Date')      # Remove because it gets turned into a float
    cache_tags = ['DB file ID']+list(cache_tags_set)+['Desc','strippedName']

    def __init__(self, cache_filename):
        self.cache_filename = cache_filename

    def load(self):
        """ Load the cached data CSV """
        self.cache = []
        if os.path.isfile(self.cache_filename):
            with open(self.cache_filename, mode='r') as csv_file:
                for row in csv.DictReader(csv_file):
                    row.pop('xDate', None) # Remove Date
                    self.cache.append(row)
                pass
        else:
            self.cache = []

    def set_value(self, id, key, value):
        """ Set a value in one row of the dict """
        if value == '':
            return
        if key in self.cache_tags:
            for row in self.cache:
                if row['DB file ID'] == id:
                    if row[key] == '':
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
        """
        Return the row for id if it is present
        """
        for row in self.cache:
            if row['DB file ID'] == id:
                return row
        # No such entry
        return dict()

    def write(self):
        """
        Write the spreadsheet
        """
        for r in self.cache:
            if 'xDate' in r:
                print(r)
        with open(self.cache_filename, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.cache_tags)
            writer.writeheader()
            writer.writerows(self.cache)


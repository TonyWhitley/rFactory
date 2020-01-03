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

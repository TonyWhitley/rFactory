from data.rFactoryData import getSingleCarData, reloadAllData

######################################################################
#
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



def createDefaultDataFiles(overwrite=False):
  newFiles = []
  getAllTags = False
  rF2_dir = os.path.join(rF2root, 'Installed')
  vehicleFiles = getListOfFiles(os.path.join(rF2_dir, 'vehicles'), pattern='*.mft', recurse=True)
  trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations'), pattern='*.mft', recurse=True)
  F1_1988_trackFiles = getListOfFiles(os.path.join(rF2_dir, 'locations', 'F1_1988_Tracks'), pattern='*.mas', recurse=True)
  cache_o = Cached_data()

  #vehNames = getVehScnNames('vehNames.txt')
  vehNames = vehFiles()

  tags = {}
  if getAllTags:
    cache_write = True
    for veh in vehicleFiles:
      text, error = readFile(veh[0])
      for tag in readTags(text):
        tags[tag] = 0
    #print(tags)
  else: # create data file
    cache_write = False
    cdf = CarDataFiles()
    for veh in vehicleFiles:
      #if veh[1] != 'F1 1996 - SL1DE.mft' and veh[1] != 'F1RFT_2013_FB_1.4.mft':
      text, error = readFile(veh[0])
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
      text, error = readFile(track[0])
      for tag in readTags(text):
        tags[tag] = 0
    #print(tags)
  else: # create data file
    tdf = TrackDataFiles()
    for track in trackFiles:
      text, error = readFile(track[0])
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
            mas_tags = tdf.__read_mas_file(tags, track[0], files)
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
    _data, error = readFile(car[0])
    for line in _data:
      if line.startswith('originalFolder'):
        _f = line[len('originalFolder='):-1]
        if not os.path.isdir(os.path.join(rF2root, _f)):
          filesToDelete.append(car[0])
  for track in rFactoryTrackFiles:
    _data, error = readFile(track[0])
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
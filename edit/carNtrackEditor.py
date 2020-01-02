"""
Given the unique ID for a car or track, edit its file.
Also have 'Save as...' for creating variants.
"""
# Python 3
import os
import tkinter as tk
from tkinter import ttk
import webbrowser

from data.rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension
from data.utils import writeFile
from data.rFactoryData import reloadAllData


############################
# The Editor's public class:
############################
class Editor:
  def __init__(self, parentFrame, fields, data, DatafilesFolder):
    """ Put this into the parent frame """
    self.tkEditor = tk.Message(parentFrame, aspect=500)
    self.parentFrame = parentFrame
    self.fields = list(fields)
    self.DatafilesFolder = DatafilesFolder

    self.tkEditor.columnconfigure(1, weight=1)

    self.numFields = len(fields)
    self.label = [0] * self.numFields
    self.entry = [0] * self.numFields
    for i, field in enumerate(fields):
      self.label[i] = tk.Label(self.tkEditor, text=field)
      self.label[i].grid(column=0, row=i, sticky='e')
      self.entry[i] = tk.Entry(self.tkEditor)
      self.entry[i].grid(column=1, row=i, ipadx=80, pady=5, ipady=2)
      self.entry[i].insert(0, data[field])

    try:
        self.lat = float(data['Latitude'])
        self.long = float(data['Longitude'])
        lat_long = True
    except:
        lat_long = False

    # Insert a blank line
    blank = tk.Label(self.tkEditor, text='')
    blank.grid(column=0, row=self.numFields, sticky='e')
    # Then the action buttons
    saveButton = tk.Button(self.tkEditor, text='Save', command=self.savePressed)
    saveAsButton = tk.Button(self.tkEditor, text='Save as...', command=self.saveAsPressed)
    browseButton = tk.Button(self.tkEditor, text='Browse', command=self.browsePressed)
    if lat_long:
        mapButton = tk.Button(self.tkEditor, text='Find on map', command=self.mapPressed)
    cancelButton = tk.Button(self.tkEditor, text='Cancel', command=self.cancelPressed)

    _col = 0
    saveButton.grid(column=_col, row=self.numFields+1)
    _col += 1
    saveAsButton.grid(column=_col, row=self.numFields+1)
    _col += 1
    if lat_long:
        mapButton.grid(column=_col, row=self.numFields+1)
        _col += 1
    browseButton.grid(column=_col, row=self.numFields+1)
    _col += 1
    cancelButton.grid(column=_col, row=self.numFields+1)
    self.tkEditor.grid(ipadx=10, ipady=10)

  def savePressed(self):
    # Write the data to a file named by the unique ID field
    text=[]
    for i, tag in enumerate(self.fields):
      if self.label[i]['text'] == 'DB file ID':
        _filename = self.entry[i].get()
      text.append('%s=%s\n' % (self.label[i]['text'], self.entry[i].get()))

    _filepath = os.path.join(self.DatafilesFolder, _filename+dataFilesExtension)

    writeFile(_filepath, text)
    reloadAllData()
    #self.parentFrame.destroy()

  def saveAsPressed(self):
    # open dialog to name file
    reloadAllData()

  def browsePressed(self):
    # open a browser with a search command
    for i, tag in enumerate(self.fields):
      if self.label[i]['text'] == 'Name':
        search_term = self.entry[i].get()
        break
    for i, tag in enumerate(self.fields):
      if self.label[i]['text'] == 'URL':
        if len(self.entry[i].get()) > 5:
          # It already has a URL
          url = self.entry[i].get()
        else:
          url = "https://www.google.com/search?q=rfactor 2 {}".format(search_term)
          # can't do that   self.entry[i].set(url)
    webbrowser.open(url)

  def mapPressed(self):
    # open a browser with a Google Maps lat/long
    url = F"https://www.google.com/maps/place/{self.lat},{self.long}".format()
    webbrowser.open(url)


  def cancelPressed(self):
    reloadAllData()
    self.parentFrame.destroy()

if __name__ == '__main__':
  # To run this tab by itself for development
  from data.rFactoryData import getSingleCarData, getSingleTrackData, reloadAllData

  root = tk.Tk()
  tabTrack = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  root.title('Editor')
  tabTrack.grid()

  edit = 'carData'

  if edit == 'sampleData':
    fields = 'Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating', 'DB file ID'
    sampleData = ['Porsche', '917K', 'Gp.C', 'Apex', 'GT', 'RWD', 1967, '1960-', '*****', 'FLAT12_917k_1971']
    o_tab = Editor(tabTrack, fields, sampleData, command=answer)

  elif edit == 'carData':
    sampleData = ['Porsche', '917K', 'Gp.C', 'Apex', 'GT', 'RWD', 1967, '1960-', '*****', 'FLAT12_917k_1971']
    data = getSingleCarData(sampleData[-1], carTags)
    o_tab = Editor(tabTrack, carTags, data, CarDatafilesFolder)

  elif edit == 'serverData': # doesn't really work, need a separate editor for favourite server handling
    fields = ['Favourite', 'Password', 'DB file ID']
    sampleData = {'Favourite':'N', 'Password':'', 'Server':'My favourite server', 'DB file ID':'favourite servers'}
    o_tab = Editor(tabTrack, fields, sampleData, 'favourites')

  root.mainloop()


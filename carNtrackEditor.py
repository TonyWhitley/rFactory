"""
Given the unique ID for a car or track, edit its file.
Also have 'Save as...' for creating variants.
"""
# Python 3
import os
import tkinter as tk
from tkinter import ttk

from rFactoryConfig import rF2root,carTags,trackTags,CarDatafilesFolder, \
  TrackDatafilesFolder,dataFilesExtension
from data import getSingleCarData, getSingleTrackData, reloadAllData
from editRF2files import writeFile

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

    # Insert a blank line
    blank = tk.Label(self.tkEditor, text='')
    blank.grid(column=0, row=self.numFields, sticky='e')
    # Then the action buttons
    saveButton = tk.Button(self.tkEditor, text='Save', command=self.savePressed)
    saveAsButton = tk.Button(self.tkEditor, text='Save as...', command=self.saveAsPressed)
    cancelButton = tk.Button(self.tkEditor, text='Cancel', command=self.cancelPressed)

    saveButton.grid(column=0, row=self.numFields+1)
    saveAsButton.grid(column=1, row=self.numFields+1)
    cancelButton.grid(column=2, row=self.numFields+1)
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

  def cancelPressed(self):
    reloadAllData()
    #self.parentFrame.destroy()

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabTrack = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  root.title('Editor')
  tabTrack.grid()
    
  fields = 'Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating', 'Car DB file'
  sampleData = ['Porsche', '917K', 'Gp.C', 'Apex', 'GT', 'RWD', 1967, '1960-', '*****', 'FLAT12_917k_1971']
#  o_tab = Editor(tabTrack, fields, sampleData, command=answer)

  data = getSingleCarData(sampleData[-1], carTags)
  o_tab = Editor(tabTrack, carTags, data, CarDatafilesFolder)

  root.mainloop()


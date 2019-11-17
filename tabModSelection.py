"""
Tab that lists car and track folders. User selects and adds them to a list
which is written to a data file for ModMaker.bat
"""
# Python 3
import json
import os
import sys
import tkinter as tk
from tkinter import ttk

from data.rFactoryConfig import rF2root
from data.utils import getListOfFiles, readFile, writeFile

_main = False # True if this is running standalone

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    self.settings = {}
    self.vars = {}

    xPadding = 10
    #############################################
    vehicles_path =  os.path.join(rF2root, 'Installed', 'Vehicles')
    vehicles = getListOfFiles(vehicles_path, pattern='*')

    tkFrame_vehicles = tk.LabelFrame(parentFrame, text='Vehicles', padx=xPadding)
    tkFrame_vehicles.grid(column=0, row=0, sticky='ew')

    # find the widest
    v = [x[1] for x in vehicles]
    w = max(v, key=len)
    self.tkVehicleListbox = tk.Listbox(tkFrame_vehicles,
                           selectmode=tk.EXTENDED,
                           width=len(w)-2,
                           height=min(20,len(vehicles))
                           )
    self.tkVehicleListbox.grid(rowspan=2)
    #
    tkVehicleScrollbar = tk.Scrollbar(tkFrame_vehicles, orient="vertical")
    tkVehicleScrollbar.config(command=self.tkVehicleListbox.yview)
    tkVehicleScrollbar.grid(column=1, row=0, sticky='ns', rowspan=2)

    for __, _v in vehicles:
        self.tkVehicleListbox.insert(tk.END, _v)

    self.tkVehicleListbox.activate(1)
    if _main:
      self.tkVehicleListbox.bind("<Double-Button-1>", self.copy_vehicles) # Double click selects the server

    ############################################
    tk.Button(tkFrame_vehicles, text="=>", command=self.copy_vehicles).\
        grid(column=2,row=0,pady=20, padx=xPadding)
    tk.Button(tkFrame_vehicles, text="<=", command=self.uncopy_vehicles).\
        grid(column=2,row=1,pady=20, padx=xPadding)

    #############################################
    self.tkSelectedVehicleListbox = tk.Listbox(tkFrame_vehicles,
                           selectmode=tk.EXTENDED,
                           width=20,
                           height=min(20,len(vehicles))
                           )
    self.tkSelectedVehicleListbox.grid(column=3, row=0, rowspan=2)


    #############################################
    #############################################
    locations_path =  os.path.join(rF2root, 'Installed', 'Locations')
    locations = getListOfFiles(locations_path, pattern='*')

    tkFrame_locations = tk.LabelFrame(parentFrame, text='Locations', padx=xPadding)
    tkFrame_locations.grid(column=2, row=0, sticky='ew')

    # find the widest
    l = [x[1] for x in locations]
    w = max(l, key=len)
    self.tkLocationListbox = tk.Listbox(tkFrame_locations,
                           selectmode=tk.EXTENDED,
                           width=len(w)-2,
                           height=min(20,len(locations))
                           )
    self.tkLocationListbox.grid(rowspan=2)
    #
    tkLocationScrollbar = tk.Scrollbar(tkFrame_locations, orient="vertical")
    tkLocationScrollbar.config(command=self.tkLocationListbox.yview)
    tkLocationScrollbar.grid(column=1, row=0, sticky='ns', rowspan=2)

    for __, _v in locations:
        self.tkLocationListbox.insert(tk.END, _v)

    self.tkLocationListbox.activate(1)
    if _main:
      self.tkLocationListbox.bind("<Double-Button-1>", self.copy_locations) # Double click selects the server

    ############################################
    tk.Button(tkFrame_locations, text="=>", command=self.copy_locations).\
        grid(column=2,row=0,pady=20, padx=xPadding)
    tk.Button(tkFrame_locations, text="<=", command=self.uncopy_locations).\
        grid(column=2,row=1,pady=20, padx=xPadding)

    #############################################
    self.tkSelectedLocationListbox = tk.Listbox(tkFrame_locations,
                           selectmode=tk.EXTENDED,
                           width=20,
                           height=min(20,len(locations))
                           )
    self.tkSelectedLocationListbox.grid(column=3, row=0, rowspan=2)

  def copy_vehicles(self, __=None):
      """ Copy selected to selection window """
      vehicles = [self.tkVehicleListbox.get(i) for i in self.tkVehicleListbox.curselection()]
      for _v in vehicles:
          self.tkSelectedVehicleListbox.insert(tk.END, _v)

  def uncopy_vehicles(self, __=None):
      """ Remove selected from selection window """
      [self.tkSelectedVehicleListbox.delete(i) for i in reversed(
          self.tkSelectedVehicleListbox.curselection())]

  def copy_locations(self, __=None):
      """ Copy selected to selection window """
      locations = [self.tkLocationListbox.get(i) for i in self.tkLocationListbox.curselection()]
      for _v in locations:
          self.tkSelectedLocationListbox.insert(tk.END, _v)

  def uncopy_locations(self, __=None):
      """ Remove selected from selection window """
      [self.tkSelectedLocationListbox.delete(i) for i in reversed(
          self.tkSelectedLocationListbox.curselection())]

  def getSettings(self):
    """ Return the settings for this tab """
    modSelection = dict()
    modSelection['cars'] = self.tkSelectedVehicleListbox.get(0,tk.END)
    modSelection['tracks'] = self.tkSelectedLocationListbox.get(0,tk.END)
    return modSelection

  def setSettings(self, settings):
    """ Set the settings for this tab """
    # Clear the list boxes
    self.tkSelectedVehicleListbox.delete(0,tk.END)
    self.tkSelectedLocationListbox.delete(0,tk.END)
    # Then load them
    for car in settings['cars']:
        self.tkSelectedVehicleListbox.insert(tk.END, car)
    for track in settings['tracks']:
        self.tkSelectedLocationListbox.insert(tk.END, track)


if __name__ == '__main__':
  # To run this tab by itself for development
  _main = True
  root = tk.Tk()
  tabModSelection = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabModSelection.grid()

  o_tab = Tab(tabModSelection)
  root.mainloop()

  o_tab.getSettings()


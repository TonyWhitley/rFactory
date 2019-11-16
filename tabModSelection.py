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
    self.tkVehicleListbox.grid()
    #
    tkVehicleScrollbar = tk.Scrollbar(tkFrame_vehicles, orient="vertical")
    tkVehicleScrollbar.config(command=self.tkVehicleListbox.yview)
    tkVehicleScrollbar.grid(column=1, row=0, sticky='ns')

    for __, _v in vehicles:
        self.tkVehicleListbox.insert(tk.END, _v)

    self.tkVehicleListbox.activate(1)
    if _main:
      self.tkVehicleListbox.bind("<Double-Button-1>", self.ok) # Double click selects the server

    #############################################
    tkFrame_vehicles_button = tk.LabelFrame(parentFrame, text='Copy', padx=xPadding)
    tkFrame_vehicles_button.grid(column=1, row=0, sticky='nsew')
    tk.Button(tkFrame_vehicles_button, text="=>", command=self.copy_vehicle).grid(pady=50)

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
    self.tkLocationListbox.grid()
    #
    tkLocationScrollbar = tk.Scrollbar(tkFrame_locations, orient="vertical")
    tkLocationScrollbar.config(command=self.tkLocationListbox.yview)
    tkLocationScrollbar.grid(column=1, row=0, sticky='ns')

    for __, _v in locations:
        self.tkLocationListbox.insert(tk.END, _v)

    self.tkLocationListbox.activate(1)
    if _main:
      self.tkLocationListbox.bind("<Double-Button-1>", self.ok) # Double click selects the server

    #############################################
    tkFrame_Locations_button = tk.LabelFrame(parentFrame, text='Copy', padx=xPadding)
    tkFrame_Locations_button.grid(column=3, row=0, sticky='nsew')
    tk.Button(tkFrame_Locations_button, text="=>", command=self.copy_location).grid(pady=50)

  def ok(self, __):
    now = self.tkVehicleListbox.get(tk.ACTIVE)
    self.getSettings()
    self.current = now

  def copy_vehicle(self):
      """ Copy selected to selection window """
      vehicles = [self.tkVehicleListbox.get(i) for i in self.tkVehicleListbox.curselection()]
      pass

  def copy_location(self):
      """ Copy selected to selection window """
      locations = [self.tkLocationListbox.get(i) for i in self.tkLocationListbox.curselection()]
      pass

  def getSettings(self):
    """ Return the settings for this tab """
    _descriptiveName = self.tkVehicleListbox.get(tk.ACTIVE)
    # Just the descriptive name for the server, get the password from favourites file
    return _descriptiveName

  def setSettings(self, settings):
    """ Set the settings for this tab """
    # Need to ID the server in the listbox and activate it.
    _listbox = self.tkVehicleListbox.get(0, tk.END)
    _item = _listbox.index(settings)
    try:
      self.tkVehicleListbox.activate(_item)
      self.tkVehicleListbox.see(_item) # Makes sure the given list index is visible.
      self.tkVehicleListbox.selection_set(_item) # Highlights it
    except:
      pass # value error
    pass


if __name__ == '__main__':
  # To run this tab by itself for development
  _main = True
  root = tk.Tk()
  tabModSelection = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabModSelection.grid()

  o_tab = Tab(tabModSelection)
  root.mainloop()

  o_tab.getSettings()


# Python 3
import json
import os
import tkinter as tk
from tkinter import ttk

from data.rFactoryConfig import favouriteServersFilesFolder,favouriteServersFilesExtension
from data.utils import readFile, writeFile

_main = False # True if this is running standalone

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    self.tkListbox = tk.Listbox(parentFrame,
                           selectmode=tk.SINGLE)
    self.tkListbox.grid(column=1, row=1, columnspan=3)
    self.settings = {}
    self.vars = {}

    filename =  os.path.join(favouriteServersFilesFolder, 'favouriteServers'+favouriteServersFilesExtension)

    _text = readFile(filename)
    try:
      self.settings = json.loads(''.join(_text))
    except: # No favourites file, create one
      self.settings = {'Server' : 'Password'}
      _text = json.dumps(self.settings, sort_keys=True, indent=4)
      writeFile(filename, _text)

    for server in self.settings:
      if server != 'server':
        self.tkListbox.insert(tk.END, server)

    self.tkListbox.activate(1)
    if _main:
      self.tkListbox.bind("<Double-Button-1>", self.ok) # Double click selects the server

  def getPassword(self, serverName):
    return self.settings[serverName]
  
  def ok(self, __):
    now = self.tkListbox.get(tk.ACTIVE)
    self.getSettings()
    self.current = now


  def getSettings(self):
    """ Return the settings for this tab """
    value = self.tkListbox.get(tk.ACTIVE)
    result = value
    # self.settings[value]  # Server, password
    # No, just the server name, get the password from favourites file
    return result

  def setSettings(self, settings):
    """ Set the settings for this tab """
    # Need to ID the server in the listbox and activate it.
    for _v in settings:
      try:
        self.tkListbox.activate(0)
      except:
        pass # value error
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  _main = True
  root = tk.Tk()
  tabFavouriteServers = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabFavouriteServers.grid()
    
  o_tab = Tab(tabFavouriteServers)
  root.mainloop()

  o_tab.getSettings()


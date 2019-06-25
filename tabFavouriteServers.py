# Python 3
import json
import os
import sys
import tkinter as tk
from tkinter import ttk

rF2_serverNotify_path = r'..\rF2_serverNotify\steps'
sys.path.append(rF2_serverNotify_path)
from rF2_serverNotify import Servers

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
      self.settings = {'Descriptive name': ('Server name', 'Password')}
      _text = json.dumps(self.settings, sort_keys=True, indent=4)
      writeFile(filename, _text)

    for descriptiveName, address in self.settings.items():
      if descriptiveName != 'Descriptive name': # that's just a comment in the data file
        self.tkListbox.insert(tk.END, descriptiveName)
        #player_count,max_players,password_protected = getServerInfo(address[0], retries=1)
        pass

    self.tkListbox.activate(1)
    if _main:
      self.tkListbox.bind("<Double-Button-1>", self.ok) # Double click selects the server

  def getPassword(self, serverName):
    for k,v in self.settings.items():
      if v[0] == serverName:
        return v[1]
    return ''
  
  def ok(self, __):
    now = self.tkListbox.get(tk.ACTIVE)
    self.getSettings()
    self.current = now


  def getSettings(self):
    """ Return the settings for this tab """
    _descriptiveName = self.tkListbox.get(tk.ACTIVE)
    # Just the descriptive name for the server, get the password from favourites file
    return _descriptiveName

  def setSettings(self, settings):
    """ Set the settings for this tab """
    # Need to ID the server in the listbox and activate it.
    _listbox = self.tkListbox.get(0, tk.END)
    _item = _listbox.index(settings)
    try:
      self.tkListbox.activate(_item)
      self.tkListbox.see(_item) # Makes sure the given list index is visible.
      self.tkListbox.selection_set(_item) # Highlights it
    except:
      pass # value error
    pass

def getServerInfo(serverName):
  s_o = Servers()
  address = s_o.readSpecificServer(serverName)
  if address[0] != 'ServerNotFound':
    info,players = s_o.readServerInfo(address)
    if info:
      return(info['player_count'],info['max_players'],info['password_protected'])
  # else
  return(0,0,0)

if __name__ == '__main__':
  # To run this tab by itself for development
  _main = True
  root = tk.Tk()
  tabFavouriteServers = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabFavouriteServers.grid()
    
  o_tab = Tab(tabFavouriteServers)
  root.mainloop()

  o_tab.getSettings()


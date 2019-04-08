# Python 3
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog

# Tabs
import tabCar
import tabTrack
import tabOpponents
import tabFavouriteServers
import tabConditions
import tabSessions
import tabOptions
import tabServer
import tabScenarios
import tabJsonEditor

from data.rFactoryConfig import scenarioFilesFolder,scenarioFilesExtension
from data.utils import readFile, writeFile

root = None
tabs = None
o_tabs = None

settings = {}
filename =  os.path.join(scenarioFilesFolder, 'lastScenario'+scenarioFilesExtension)

class TabSettings:
  def __init__(self):
    pass

  def setAllSettings(self, settings):
    """ Set the settings for each tab """
    global tabs, o_tabs
    if tabs:
      for name, tab in tabs:
        try:
          o_tabs[name].setSettings(settings=settings[name])
        except:
          print('No Scenario data to set up tab %s' % name)

  def getAllSettings(self):
    """ Get the settings from each tab """
    global tabs, o_tabs, settings
    for name, tab in tabs:
      settings[name] = o_tabs[name].getSettings()
    return settings

  def getServerPassword(self):
    #Special case: get server password
    _server = settings['Favourite Servers']
    return o_tabs['Favourite Servers'].getPassword(_server)

def setMenubar(menubar):

    # create a pulldown menu, and add it to the menu bar
    #filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_command(label="Open scenario ", command=openScenario)
    menubar.add_separator()
    menubar.add_command(label="Save scenario", command=saveScenario, accelerator='Ctrl+S')
    menubar.master.bind_all("<Control-s>", saveScenario)
    menubar.add_command(label="Save scenario as...", command=saveScenarioAs)
    menubar.add_separator()
    menubar.add_command(label="Exit", command=menubar.master.quit)
    #menubar.add_cascade(label="File", menu=filemenu)

def openScenario():
  global filename
  print('openScenario')
 
  #root = tk.Tk()
  filename =  filedialog.askopenfilename(initialdir = scenarioFilesFolder,title = "Select file",filetypes = (("rFactory Scenario files","*%s" % scenarioFilesExtension),("all files","*.*")))
  _text = readFile(filename)
  settings = json.loads(''.join(_text))
  print(settings)
  _tso = TabSettings()
  _ = _tso.setAllSettings(settings)

def openDefaultScenario():
  global filename

  filename =  os.path.join(scenarioFilesFolder, 'lastScenario'+scenarioFilesExtension)
  _text = readFile(filename)
  if os.path.exists(filename):
    settings = json.loads(''.join(_text))
    print(settings)
    _tso = TabSettings()
    _ = _tso.setAllSettings(settings)
    return

  #else there is no default settings file???

def saveScenarioAs():
  global filename

  filename =  filedialog.asksaveasfilename(initialdir = scenarioFilesFolder,title = "Select file",filetypes = (("rFactory Scenario files","*%s" % scenarioFilesExtension),("all files","*.*")))
  if not filename.endswith(scenarioFilesExtension):
    filename += scenarioFilesExtension
  print('saveScenarioAs "%s%s"' % (filename, scenarioFilesExtension))
  saveScenario()

def saveScenario():
  global filename

  print('saveScenario')
  _tso = TabSettings()
  _ = _tso.getAllSettings()
  _text = json.dumps(settings, sort_keys=True, indent=4)
  writeFile(filename, _text)

def saveDefaultScenario():
  global filename

  filename =  os.path.join(scenarioFilesFolder, 'lastScenario'+scenarioFilesExtension)
  _tso = TabSettings()
  _ = _tso.getAllSettings()
  _text = json.dumps(settings, sort_keys=True, indent=4)
  writeFile(filename, _text)

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    root = parentFrame
    tkLabelScenarios = tk.Label(parentFrame, 
                                text='Here a list of scenario files to load plus "Save as..."')
    tkLabelScenarios.grid(column=4, row=3)

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Scenario - what does that mean? Scenario sets all tab settings']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    # Meaningless for this tab
    pass

def dummy():
  pass

def setTabs(_tabs, _o_tabs):
  """
  Hack to pass in tab names, modules and objects
  """
  global tabs, o_tabs
  tabs = _tabs
  o_tabs = _o_tabs

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabScenarios = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabScenarios.grid()

  menubar = tk.Menu(tabScenarios)

  helpmenu = tk.Menu(menubar, tearoff=0)
  helpmenu.add_command(label="About", command=dummy)
  menubar.add_cascade(label="Help", menu=helpmenu)

  _tso = TabSettings()

  # display the menu
  #???? menubar.config(menu=menubar)
    
  o_tab = Tab(tabScenarios)
  setMenubar(menubar)

  ##Menu(menubar)
  # display the menu
  root.config(menu=menubar)

  root.mainloop()

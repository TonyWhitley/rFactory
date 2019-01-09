# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Added a bit of class. Geddit?
# First tab - Cars - incorporated.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font 
# Tabs
import tabCar
import tabTrack
import tabOpponents
import tabConditions
import tabSessions
import tabOptions
import tabServer
import tabScenarios
import tabJsonEditor

from executeRF2 import runRF2
from trawl_rF2_datafiles import trawl_for_new_rF2_datafiles

BUILD_REVISION = 42 # The git commit count
versionStr = 'rFactory V0.1.%d' % BUILD_REVISION
versionDate = '2019-01-09'
def about():
  messagebox.showinfo(
            'About rFactory',
            '%s  %s\nby Tony Whitley' % (versionStr, versionDate)
        )



class Menu:
  def __init__(self, 
               menubar, 
               menu2tab=None):
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

class MainWindow:
  """ The main app window innit """
  handle = None
  def __init__(self):
    self.handle = tk.Tk()
    #self.handle.geometry('500x300')
    self.width_of_window = 500
    self.height_of_window = 300
    self.handle.title('rFactory')
    self.handle.columnconfigure(0, weight=1, pad=50)
    self.handle.columnconfigure(1, weight=1, pad=50)
    self.handle.columnconfigure(2, weight=1)
    self.handle.rowconfigure(0, weight=1, pad=50)
    self.handle.rowconfigure(1, weight=1, pad=50)
    #self.handle.rowconfigure(2, weight=1)
    #self.handle.rowconfigure(3, weight=1)
    #self.handle.rowconfigure(4, weight=1)
    self.handle.grid()
  def setSize(self, width, height):
    """ Set the size of the window """
    self.width_of_window = width # The width of a GUI window. 
                                 # You can change this value to suit your preference

    self.height_of_window = height # The height of a GUI window. 
                                   # You can change this value to suit your preference

  def centreWindow(self):
    """ Fetch the monitor size and create the x & y coordinate """
    screen_width = self.handle.winfo_screenwidth() # this is fetching the monitor 
                                                   # maximum width (typical monitors are 1920x1080)
    screen_height = self.handle.winfo_screenheight() # this is fetching the monitor maxium height
    x_coordinate = (screen_width/2) - (self.width_of_window/2) # This is getting the correct 
                                                               # x coordinate position for the GUI
    y_coordinate = (screen_height/2) - (self.height_of_window/2)# This is getting the correct y 
                                                                # coordinate position for the GUI

    # Initialise the GUI's position 
    self.handle.geometry("%dx%d+%d+%d" % 
                         (self.width_of_window, 
                          self.height_of_window, 
                          x_coordinate, 
                          y_coordinate)) # setting the position of the main window 
 
# The tabs

class Tabs:
  """ The tabs in the main window """
  tabs = {}   # the tab Frames
  o_tabs = {} # the Tab objects
  def __init__(self, parentFrame):
    self.tabNames = [ \
      ['Car', tabCar],
      ['Track', tabTrack],
      ['Opponents', tabOpponents],
      ['Conditions', tabConditions],
      ['Sessions', tabSessions],
      ['Options', tabOptions],
      ['Server', tabServer],
      ['Scenarios', tabScenarios],
      ['JSON editor', tabJsonEditor]
      ]
    self.notebook = ttk.Notebook(parentFrame)

    """
    # Set style of tab labels
    # but then disabled Tabs aren't greyed out
    style = ttk.Style()
    style.theme_create( "MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
            "TNotebook.Tab": {"configure": {"padding": [10, 5] },}})

    style.theme_use("MyStyle") 
    """

    tabHeight = 300
    tabWidth = 400
    for name, tab in self.tabNames:
      self.tabs[name] = ttk.Frame(self.notebook, height=tabHeight, width=tabWidth)
      self.tabs[name].config(relief='sunken', borderwidth=5)
      self.notebook.add(self.tabs[name], text=' %s ' % name)

      tkTabFrame = ttk.Frame(self.tabs[name])
      self.o_tabs[name] = tab.Tab(tkTabFrame)
      tkTabFrame.grid(column=4, row=3)

    self.notebook.grid()

  def disableTab(self, tabName):
    for tabId, name in enumerate(self.tabNames):
      if name[0] == tabName:
        self.notebook.tab(tabId, state='disabled')
        return
    # error unknown tabName
  def enableTab(self, tabName):
    for tabId, name in enumerate(self.tabNames):
      if name[0] == tabName:
        self.notebook.tab(tabId, state='normal')
        return
    # error unknown tabName
  def selectTab(self, tabName):
    for tabId, name in enumerate(self.tabNames):
      if name[0] == tabName:
        self.notebook.select(tabId)
        return
    # error unknown tabName
  def getSettings(self):
    """ Get the settings from each tab """
    settings = []
    for name, _ in self.tabNames:
      settings.append([name, self.o_tabs[name].getSettings()])
    return settings

  def _testSetSettings(self):
    """ Set the settings from each tab """
    settings = ['0','1','2','3','4','5','6','7','8','9']
    for name, _ in self.tabNames:
      self.o_tabs[name].setSettings(settings=settings)

class Menus:
  """ The sub-menus for tabs in the main window """
  menus = {}  # the Menu objects
  def __init__(self, parentFrame):
    self.menuNames = [ \
      #['Car', tabCar],
      #['Track', tabTrack],
      #['Opponents', tabOpponents],
      #['Conditions', tabConditions],
      #['Sessions', tabSessions],
      #['Options', tabOptions],
      #['Server', tabServer],
      #['Scenarios', tabScenarios],
      ['JSON editor', tabJsonEditor]
      ]
    menubar = tk.Menu(parentFrame)

    for menuLabel, o_menu in self.menuNames:
      _menu = tk.Menu(menubar, tearoff=0)
      menubar.add_cascade(label=menuLabel, menu=_menu)
      o_menu.setMenubar(_menu)
    Menu(menubar)
    # display the menu
    parentFrame.config(menu=menubar)

# The GO buttons
class GoButtons:
  """ 
  The big buttons that 
  * switch on/offline
  * run rFactor 2
  * quit 
  """
  def __init__(self, parentFrame):
    _goFrame = ttk.Frame(parentFrame)
    _goFrame.grid(column=1, row=0, sticky='w')
    # Draw the buttons
    buttonFont = font.Font(weight='bold', size=10)

    self.tkButtonOnline = tk.Button(
        _goFrame,
        text="Online",
        width=20,
        height=2,
        background='orange',
        font=buttonFont,
        command=self.online)
    self.tkButtonOnline.grid(column=2, row=0, pady=5)

    self.tkButtonOffline = tk.Button(
        _goFrame,
        text="Offline",
        width=20,
        height=2,
        background='orange',
        font=buttonFont,
        command=self.offline)
    self.tkButtonOffline.grid(column=2, row=1, pady=5)

    self.tkButtonReplay = tk.Button(
        _goFrame,
        text="Replay",
        width=20,
        height=2,
        background='orange',
        font=buttonFont,
        command=self.replay)
    self.tkButtonReplay.grid(column=2, row=2, pady=5)

    self.tkButtonRun = tk.Button(
        _goFrame,
        text="Run rFactor 2",
        width=20,
        height=2,
        background='green',
        font=buttonFont,
        command=self.run)
    self.tkButtonRun.grid(column=2, row=3, pady=25)

    self.tkButtonQuit = tk.Button(
        _goFrame,
        text="Quit",
        width=20,
        background='red',
        command=self._quit)
    self.tkButtonQuit.grid(column=2, row=4, pady=25)

  def online(self):
    """ The Online button pressed """
    # Server defines track etc. but if user enters it it can be used
    # to adjust graphics details.
    #tabs.disableTab('Track')
    #tabs.disableTab('Opponents')
    #tabs.disableTab('Conditions')
    tabs.disableTab('Sessions')
    tabs.enableTab('Server')
    self.tkButtonOnline.configure(relief=tk.SUNKEN) #, bg='green')
    self.tkButtonOffline.configure(relief=tk.RAISED) #, bg='red')
    self.tkButtonReplay.configure(relief=tk.RAISED) #, bg='red')

  def offline(self):
    """ The Offline button pressed """
    tabs.enableTab('Track')
    tabs.enableTab('Opponents')
    tabs.enableTab('Conditions')
    tabs.enableTab('Sessions')
    tabs.disableTab('Server')
    self.tkButtonOnline.configure(relief=tk.RAISED) #, bg='red')
    self.tkButtonOffline.configure(relief=tk.SUNKEN) #, bg='green')
    self.tkButtonReplay.configure(relief=tk.RAISED) #, bg='red')

  def replay(self):
    """ The Replay button pressed """
    tabs.enableTab('Track')
    tabs.enableTab('Opponents')
    tabs.enableTab('Conditions')
    tabs.enableTab('Sessions')
    tabs.disableTab('Server')
    self.tkButtonOnline.configure(relief=tk.RAISED) #, bg='red')
    self.tkButtonOffline.configure(relief=tk.RAISED) #, bg='green')
    self.tkButtonReplay.configure(relief=tk.SUNKEN) #, bg='red')

  def run(self):
    """ The Run rFactor 2 button has been pressed """
    self.tkButtonRun.flash() # Flash it
    __settings = tabs.getSettings()

    print('\nDEBUG')
    if self.tkButtonOnline['relief'] == tk.SUNKEN: # Online is pressed
      print('Online')
      runRF2('Online', __settings)
    if self.tkButtonOffline['relief'] == tk.SUNKEN: # Offline is pressed
      print('Offline')
      runRF2('Offline', __settings)
    else:
      print('Replay')
      runRF2('Replay', __settings)
    for tab in __settings:
      print(tab[0], tab[1])

  def _quit(self):
    mainWindow.handle.destroy()


if __name__ == "__main__":
  mainWindow = MainWindow()
  mainWindow.setSize(width=1200, height=800)
  mainWindow.centreWindow()
 
  menubar = tk.Menu(mainWindow.handle)
  # display the menus
  Menus(mainWindow.handle)

  tabs = Tabs(mainWindow.handle)
  tabs._testSetSettings()

  goButtons = GoButtons(mainWindow.handle)

  # Set initial tab state
  tabs.selectTab('Cars')
  goButtons.offline()

  # Check if there are any new car/track files
  trawl_for_new_rF2_datafiles(mainWindow)

  mainWindow.handle.mainloop()

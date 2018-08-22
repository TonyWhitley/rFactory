# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Added a bit of class. Geddit?
# First tab - Cars - incorporated.

import tkinter as tk
from tkinter import ttk
 
# Tabs
import carSelection

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
  tabs = {}
  def __init__(self, parentFrame):
    self.tabNames = [ \
      'Car',
      'Track',
      'Opponents',
      'Conditions',
      'Sessions',
      'Options',
      'Server',
      'Scenarios'
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
    for name in self.tabNames:
      self.tabs[name] = ttk.Frame(self.notebook, height=tabHeight, width=tabWidth)
      self.tabs[name].config(relief='sunken', borderwidth=5)
      self.notebook.add(self.tabs[name], text=' %s ' % name)
    # Works notebook.add(....., text=' Conditions ', state='disabled')
    # Doesn't notebook.tab(notebook.index(' Options '), state='disabled')
    self.notebook.grid()

  def disableTab(self, tabName):
    for tabId, name in enumerate(self.tabNames):
      if name == tabName:
        self.notebook.tab(tabId, state='disabled')
        return
    # error unknown tabName
  def enableTab(self, tabName):
    for tabId, name in enumerate(self.tabNames):
      if name == tabName:
        self.notebook.tab(tabId, state='normal')
        return
    # error unknown tabName
  def selectTab(self, tabName):
    for tabId, name in enumerate(self.tabNames):
      if name == tabName:
        self.notebook.select(tabId)
        return
    # error unknown tabName


# The GO buttons

def online():
  tabs.disableTab('Track')
  tabs.disableTab('Opponents')
  tabs.disableTab('Conditions')
  tabs.disableTab('Sessions')
  tabs.enableTab('Server')

def offline():
  tabs.enableTab('Track')
  tabs.enableTab('Opponents')
  tabs.enableTab('Conditions')
  tabs.enableTab('Sessions')
  tabs.disableTab('Server')

def run():
  pass

def _quit():
  #global mainWindow
  mainWindow.handle.destroy()

def goButtons(_goFrame):
  """ Draw the buttons that select On/Off line and run rFactor """
  tkButtonOnline = tk.Button(
      _goFrame,
      text="Online",
      width=20,
      height=2,
      command=online)
  tkButtonOnline.grid(column=2, row=0, pady=5)

  tkButtonOffline = tk.Button(
      _goFrame,
      text="Offline",
      width=20,
      height=2,
      command=offline)
  tkButtonOffline.grid(column=2, row=1, pady=5)

  tkButtonRun = tk.Button(
      _goFrame,
      text="Run rFactor 2",
      width=20,
      height=2,
      command=run)
  tkButtonRun.grid(column=2, row=2, pady=25)

  tkButtonQuit = tk.Button(
      _goFrame,
      text="Quit",
      width=20,
      command=_quit)
  tkButtonQuit.grid(column=2, row=3, pady=25)

if __name__ == "__main__":
  mainWindow = MainWindow()
  mainWindow.setSize(width=1000, height=400)
  mainWindow.centreWindow()
 
  #tkLabelTop = tk.Label(mainWindow.handle, text=" Here we are ")
  #tkLabelTop.grid()

  tabs = Tabs(mainWindow.handle)

  goFrame = ttk.Frame(mainWindow.handle)
  goButtons(goFrame)
  goFrame.grid(column=1, row=0, sticky='w')


  tkLabelScenarios = tk.Label(tabs.tabs['Scenarios'], 
                              text='Here a list of scenario files plus "Save as..."')
  tkLabelScenarios.grid(column=4, row=3)

  tkTabFrameCars = ttk.Frame(tabs.tabs['Car'])
  carSelection.tab(tkTabFrameCars)
  tkTabFrameCars.grid(column=4, row=3)

  tkLabelTracks = tk.Label(tabs.tabs['Track'], 
                           text='Here a table of tracks that can be filtered and sorted by \
type/country/continent/year/decade/modder/star rating')
  tkLabelTracks.grid(column=4, row=3)

  tkLabelServer = tk.Label(tabs.tabs['Server'], 
                           text='Here a list of servers plus "Add server" ')
  tkLabelServer.grid(column=4, row=3)

  # Set initial tab state
  tabs.selectTab('Cars')
  offline()

  tk.mainloop()

# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Added a bit of class. Geddit?

import tkinter as tk
from tkinter import ttk
 
import platform


class MainWindow:
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
    self.width_of_window = width # The width of a GUI window. You can change this value to suit your preference

    self.height_of_window = height # The height of a GUI window. You can change this value to suit your preference

  def centreWindow(self):
    # Fetch the monitor size and create the x & y coordinate 
    screen_width = self.handle.winfo_screenwidth() # this is fetching the mointor maximum width (typical mointors are 1920x1080)
    screen_height = self.handle.winfo_screenheight() # this is fetching the mointor maxium height
    x_coordinate = (screen_width/2) - (self.width_of_window/2) # This is getting the correct x coordinate position for the GUI
    y_coordinate = (screen_height/2) - (self.height_of_window/2)# This is getting the correct y coordinate position for the GUI

    # Initialise the GUI's position 
    self.handle.geometry("%dx%d+%d+%d" % (self.width_of_window, self.height_of_window, x_coordinate, y_coordinate)) # setting the position of the main window 
 
# The tabs

class Tabs:
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

def quit():
    #global mainWindow
    mainWindow.handle.destroy()

def goButtons(goFrame):
  tkButtonOnline = tk.Button(
      goFrame,
      text="Online",
      width=20,
      height=2,
      command=online)
  tkButtonOnline.grid(column=2, row=0, pady=5)

  tkButtonOffline = tk.Button(
      goFrame,
      text="Offline",
      width=20,
      height=2,
      command=offline)
  tkButtonOffline.grid(column=2, row=1, pady=5)

  tkButtonRun = tk.Button(
      goFrame,
      text="Run rFactor 2",
      width=20,
      height=2,
      command=run)
  tkButtonRun.grid(column=2, row=2, pady=25)

  tkButtonQuit = tk.Button(
      goFrame,
      text="Quit",
      width=20,
      command=quit)
  tkButtonQuit.grid(column=2, row=3, pady=25)

if __name__ == "__main__":
  mainWindow = MainWindow()
  mainWindow.setSize(width=800, height=600)
  mainWindow.centreWindow()
 
  #tkLabelTop = tk.Label(mainWindow.handle, text=" Here we are ")
  #tkLabelTop.grid()

  tabs = Tabs(mainWindow.handle)
  tabs.selectTab('Options')

  goFrame = ttk.Frame(mainWindow.handle)
  goButtons(goFrame)
  goFrame.grid(column=1, row=0, sticky='w')


  tkLabelScenarios = tk.Label(tabs.tabs['Scenarios'], text='Here a list of scenario files plus "Save as..."')
  tkLabelScenarios.grid(column=4, row=3)

  tkLabelCars = tk.Label(tabs.tabs['Car'], text='Here a table of cars that can be filtered and sorted by type/year/decade/modder/star rating')
  tkLabelCars.grid(column=4, row=3)

  tkLabelTracks = tk.Label(tabs.tabs['Track'], text='Here a table of tracks that can be filtered and sorted by type/country/continent/year/decade/modder/star rating')
  tkLabelTracks.grid(column=4, row=3)

  tkLabelServer = tk.Label(tabs.tabs['Server'], text='Here a list of servers plus "Add server" ')
  tkLabelServer.grid(column=4, row=3)

  # 101 stuff

  if 0:
  
    tkDummyButton = tk.Button(
        tabs.tabs['Car'],
        text="Dummy Button")
    tkDummyButton.grid(column=4, row=3)
   
    #tkLabel = tk.Label(tabs.tabs['Car'], text=" Hello Python!")
    #tkLabel.grid(column=4, row=3)
 
    strVersion = "running Python version " + platform.python_version()
    #tkLabelVersion = tk.Label(tabs.tabs['Track'], text=strVersion)
    #tkLabelVersion.grid()
    strPlatform = "Platform: " + platform.platform()
    #tkLabelPlatform = tk.Label(tabs.tabs['Track'], text=strPlatform)
    #tkLabelPlatform.grid(column=2, row=3)
 
    tkLabel5 = tk.Label(tabs.tabs['Options'], text=" Hello World!")
    tkLabel5.grid(column=4, row=3)
    tkLabel5.columnconfigure(0, weight=1)
    tkLabel5.columnconfigure(1, weight=1)
    tkLabel5.columnconfigure(2, weight=1)

    button = tk.Button(tabs.tabs['Options'], text='Ooh! It\'s a button!')
    button.grid(column=5, row=2, sticky='e')

  tk.mainloop()
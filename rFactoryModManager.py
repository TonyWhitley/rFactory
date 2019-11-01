import os
from subprocess import call, Popen
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as font

from rFactory import MainWindow, Tabs
import tabScenarios
from data.trawl_rF2_datafiles import trawl_for_new_rF2_datafiles
from data.rFactoryData import getSingleCarData, getSingleTrackData
from data.rFactoryConfig import modMakerFilesFolder, modMakerFilesExtension
from data.utils import readFile, readTextFile, writeFile, bundleFolder
from lib.tkToolTip import Tooltip as Tooltip
# Tabs
import tabCar
import tabTrack

BUILD_REVISION = 114 # The git commit count
versionStr = 'rFactoryModManager V0.1.%d' % BUILD_REVISION
versionDate = '2019-09-30'

class Tab:
  settings = list()
  def __init__(self, parentFrame):
    """ Dummy tab to get/set settings """
    """ Put this into the parent frame """
    self.goButtons = GoButtons(parentFrame.handle)

  def getSettings(self):
        """ Return the settings for this tab """
        return [self.goButtons.tkStrVarModMakerFile.get()]

  def setSettings(self, settings):
        """ Set the settings for this tab """
        self.goButtons.modmaker_file = os.path.join(os.getcwd(),
                               modMakerFilesFolder,settings[-1])
        self.goButtons.tkStrVarModMakerFile.set(os.path.basename(settings[-1]))

def about():
  messagebox.askokcancel(
            'About rFactoryModManager',
            '%s  %s\nby Tony Whitley' % (versionStr, versionDate)
        )

def faq():
  _faq = readTextFile(bundleFolder('rFactoryModManagerFaq.txt'))
  messagebox.askokcancel(
            'rFactoryModManager FAQ',
            _faq
        )

class Menu:
  def __init__(self,
               menubar,
               menu2tab=None):
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="FAQ", command=faq)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

class Menus:
  """ The sub-menus for tabs in the main window """
  menus = {}  # the Menu objects
  def __init__(self, parentFrame, menuNames=[]):
    self.menuNames = menuNames
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
  * create ModMaker.bat data files
  * run rFactor 2 using ModMaker.bat
  * quit
  """
  modmaker_file = os.path.join(os.getcwd(),
                               modMakerFilesFolder,
                               'sample.modfile.txt')
  def __init__(self, parentFrame):
    self.tkStrVarModMakerFile = tk.StringVar()
    self.tkStrVarModMakerFile.set(os.path.basename(self.modmaker_file))
    _goFrame = ttk.Frame(parentFrame)
    _goFrame.grid(column=13, row=0, sticky='w')
    # Draw the buttons
    buttonFont = font.Font(weight='bold', size=10)
    __gbc = 2 # Go Buttons Column

    tkLabel = tk.Label(_goFrame,
                       font=buttonFont,
                       text='Current ModMaker file')
    tkLabel.grid(column=__gbc, row=0)

    tkLabel = tk.Label(_goFrame,
                       font=buttonFont,
                       relief=tk.SOLID,
                       padx=5,
                       pady=5,
                       textvariable=self.tkStrVarModMakerFile)
    tkLabel.grid(column=__gbc, row=1)

    self.tkButtonselectFile = tk.Button(
        _goFrame,
        text="Select ModMaker.bat\ndata file",
        width=20,
        height=2,
        background='orange',
        font=buttonFont,
        command=self.selectFile)
    self.tkButtonselectFile.grid(column=__gbc, row=2, pady=5)

    self.tkButtoncreateFile = tk.Button(
        _goFrame,
        text="Create ModMaker.bat\ndata file",
        width=20,
        height=2,
        background='orange',
        font=buttonFont,
        command=self.createFile)
    self.tkButtoncreateFile.grid(column=__gbc, row=3, pady=5)
    Tooltip(self.tkButtoncreateFile,
            text='Select multiple cars and tracks first')

    self.tkButtonRun = tk.Button(
        _goFrame,
        text="Run rFactor 2",
        width=20,
        height=2,
        background='green',
        font=buttonFont,
        command=self.run)
    self.tkButtonRun.grid(column=__gbc, row=4, pady=25)

    self.tkButtonQuit = tk.Button(
        _goFrame,
        text="Quit",
        width=20,
        background='red',
        command=self._quit)
    self.tkButtonQuit.grid(column=__gbc, row=6, pady=25)

  def selectFile(self):
    """ The Select File button pressed """
    _filepath = filedialog.askopenfilename(
        title = 'Select ModMaker file',
        initialdir=modMakerFilesFolder,
        defaultextension='.txt',
        filetypes=[('Modmaker files', 'txt')])
    if _filepath:
        self.modmaker_file = _filepath
        self.tkStrVarModMakerFile.set(os.path.basename(_filepath))
        tabScenarios.saveDefaultScenario()

  def createFile(self):
    """ The Create File button pressed """
    _cars = tabs.o_tabs['Car'].get_selection()
    car_list = []
    for _car in _cars:
        data = getSingleCarData(id=_car[-1], tags=['originalFolder'])
        car_list.append('Vehicle='+data['originalFolder'].split('\\')[2]+'\n')
    car_list=list(set(car_list))    # dedupe the list (in case)
    print(car_list)

    _tracks = tabs.o_tabs['Track'].get_selection()
    track_list = []
    for _track in _tracks:
        data = getSingleTrackData(id=_track[-1], tags=['originalFolder'])
        track_list.append('Location='+data['originalFolder'].split('\\')[2]+'\n')
    track_list=list(set(track_list))    # dedupe the list (e.g. F1_1988_Tracks)
    print(track_list)

    _filepath = filedialog.asksaveasfilename(
                                 title='Save ModMaker file as...',
                                 initialdir=modMakerFilesFolder,
                                 initialfile=self.tkStrVarModMakerFile.get(),
                                 defaultextension='.txt',
                                 filetypes=[('Modmaker files', 'txt')])
    if not _filepath:
        return

    self.modmaker_file = _filepath
    self.tkStrVarModMakerFile.set(os.path.basename(_filepath))
    # May have more than one .ext
    # e.g.sample.modfile.txt
    name = 'Name=%s\n\n' % os.path.basename(_filepath).split('.')[0]
    text = ['# Created by rFactoryModManager\n\n']
    text.append(name)
    text += car_list
    text.append('\n')
    text += track_list

    writeFile(_filepath, text)
    messagebox.askokcancel(
            'File %s written' % _filepath,
            '%s' % text)

  def run(self):
    """ The Run rFactor 2 button has been pressed """
    self.tkButtonRun.flash() # Flash it

    mainWindow.iconify()
    _cmd = bundleFolder('ModMaker.bat') + ' ' + self.modmaker_file
    call(_cmd)
    """
    this doesn't work
    try:
        subprocess.Popen(_cmd)
    except:
        try:  # again as a shell command
            subprocess.Popen(_cmd, shell=True)
        except:
            print("Couldn't execute '%s'" % _cmd)
    """

    mainWindow.deiconify()
    pass

  def _quit(self):
    mainWindow.handle.destroy()

if __name__ == "__main__":

  tabNames = [ \
      ['Car', tabCar],
      ['Track', tabTrack],
      ]

  mainWindow = MainWindow('rFactoryModManager')
  mainWindow.setSize(width=1200, height=800)
  mainWindow.centreWindow()

  # Check if there are any new car/track files
  trawl_for_new_rF2_datafiles(mainWindow)

  os.makedirs(modMakerFilesFolder, exist_ok=True)

  menubar = tk.Menu(mainWindow.handle)
  # display the menus
  Menus(mainWindow.handle)

  tabs = Tabs(mainWindow.handle, tabNames)
  tabs.dummyTabs(mainWindow, [['ModManagerOptions', Tab]])

  tabScenarios.setTabs(tabs.tabNames, tabs.o_tabs)
  tabScenarios.openDefaultScenario()
  #tabs._testSetSettings()

  #goButtons = GoButtons(mainWindow.handle)

  # Set initial tab state
  tabs.selectTab('Cars')

  mainWindow.handle.mainloop()

"""
Options Tab for running ModMaker
Not used as yet
"""
# Python 3
import tkinter as tk
from tkinter import ttk

from lib.tkToolTip import Tooltip
wraplength = 100

# But we don't want an actual tab...
class Tab:
  settings = list()
  def __init__(self, parentFrame):
    """ Dummy tab to get/set settings """
    """ Put this into the parent frame """
    pass
  def getSettings(self):
        """ Return the settings for this tab """
        return self.settings # filters too?  Probably not

  def setSettings(self, settings):
        """ Set the settings for this tab """
        carID = settings[-1]


#########################
# The tab's public class:
#########################
class _Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabel_Options = tk.Label(parentFrame,
                                text='Here a set of options for configuring rFactor')
    tkLabel_Options.grid(column=1, row=1, columnspan=3)
    self.settings = {}
    self.vars = {}
    _tkCheckbuttons = {}
    _tkRadiobuttons = {}

    xPadding = 10
    ####################################################
    tkFrame_Co_programs = tk.LabelFrame(parentFrame, text='Other programs to run with rF2', padx=xPadding)
    tkFrame_Co_programs.grid(column=3, row=4, sticky='ew')

    self._createVar('CrewChief', False)
    _tkCheckbuttons['CrewChief'] = tk.Checkbutton(tkFrame_Co_programs,
                                             text='Crew Chief',
                                             variable=self.vars['CrewChief'])
    Tooltip(_tkCheckbuttons['CrewChief'],
            text='Spotter and voice control',
            wraplength=wraplength)

    self._createVar('Discord', False)
    _tkCheckbuttons['Discord'] = tk.Checkbutton(tkFrame_Co_programs,
                                           text='Discord (voice)',
                                           variable=self.vars['Discord'])
    Tooltip(_tkCheckbuttons['Discord'],
            text='Voice chat between drivers',
            wraplength=wraplength)

    self._createVar('TeamSpeak', False)
    _tkCheckbuttons['TeamSpeak'] = tk.Checkbutton(tkFrame_Co_programs,
                                             text='TeamSpeak',
                                             variable=self.vars['TeamSpeak'])
    Tooltip(_tkCheckbuttons['TeamSpeak'],
            text='Voice chat between drivers',
            wraplength=wraplength)

    _tkCheckbuttons['CrewChief'].grid(sticky='w')
    _tkCheckbuttons['Discord'].grid(sticky='w')
    _tkCheckbuttons['TeamSpeak'].grid(sticky='w')

    ####################################################
    tkFrame_debug = tk.LabelFrame(parentFrame, text='Debug', padx=xPadding)
    tkFrame_debug.grid(column=3, row=5, sticky='ew')

    self._createVar('DummyRF2', True)
    _tkCheckbuttons['Dummy_rF2'] = tk.Checkbutton(tkFrame_debug,
      text='Run dummy rF2\nprogram that accesses\nthe same data files and\ndumps what rF2\nwould do with it',
      variable=self.vars['DummyRF2'])

    self._createVar('RunCoPrograms', True)
    _tkCheckbuttons['RunCoPrograms'] = tk.Checkbutton(tkFrame_debug,
      text='Run co-programs with dummy rF2',
      variable=self.vars['RunCoPrograms'])

    _tkCheckbuttons['Dummy_rF2'].grid(sticky='w')
    _tkCheckbuttons['RunCoPrograms'].grid(sticky='w')

  def _createVar(self, name, value):
    self.vars[name] = tk.StringVar(name=name)
    self.vars[name].set(value)

  def getSettings(self):
    """ Return the settings for this tab """
    for _v in self.vars:
      self.settings[self.vars[_v]._name] = self.vars[_v].get()
    result = self.settings
    return result

  def setSettings(self, settings):
    """ Set the settings for this tab """
    for _v in settings:
      try:
        self.vars[_v].set(settings[_v])
      except:
        pass # value error
    pass

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabOptions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabOptions.grid()

  o_tab = Tab(tabOptions)
  root.mainloop()

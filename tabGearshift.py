
import sys
# Python 3
import tkinter as tk
from tkinter import ttk

from lib.tkToolTip import Tooltip

sys.path.append('gearshift')
import mockMemoryMap
from Gearshift import main as gearshiftMain

wraplength = 100

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabel_Options = tk.Label(parentFrame,
                                text='Realistic Gearshift')
    tkLabel_Options.grid(column=1, row=1, columnspan=3)
    self.settings = {}
    self.vars = {}
    _tkCheckbuttons = {}
    _tkRadiobuttons = {}

    controls_o, graunch_o = gearshiftMain()
    maxRevs=10000
    maxFwdGears=6
    instructions = 'blah blah'
    o_gui = mockMemoryMap.live(parentFrame,
                 graunch_o,                 # to read Graunch status
                 controls_o,                # to read whether state machine is active
                 maxRevs,
                 maxFwdGears,
                 instructions=instructions  # Text
                 )

    xPadding = 10

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

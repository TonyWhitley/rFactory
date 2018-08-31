import os
import sys

# Python 3
import tkinter as tk
from tkinter import ttk

if os.path.exists('../ScriptedJsonEditor/ScriptedJsonEditor'):
  sys.path.append('../ScriptedJsonEditor/ScriptedJsonEditor')
  from GUI import Tab as _Tab, JobFrames

  class Tab(_Tab):
    def __init__(self, parentFrame):
      x = _Tab(parentFrame, cwd='../ScriptedJsonEditor/ScriptedJsonEditor')

      tkLabelframe_jobSettings = x.tkLabelframe_jobSettings

      o_tab = JobFrames(tkLabelframe_jobSettings)

      o_tab.set_checkbutton('G25_jobs', 'Monitor', 1)
      assert o_tab.get_checkbutton('G25_jobs', 'Monitor') == 1
else:
  class Tab:
    def __init__(self, parentFrame):
      """ Put this into the parent frame """
      tkLabelServer = tk.Label(parentFrame, 
                                  text='ScriptedJsonEditor module not present')
      tkLabelServer.grid(column=4, row=3)
    def getSettings(self):
      """ Return the settings for this tab """
      return ['Server', 'password']

    def setSettings(self, settings):
      """ Set the settings for this tab """
      pass

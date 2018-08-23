# Python 3
import tkinter as tk
from tkinter import ttk

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabelConditions = tk.Label(parentFrame, 
                                text='Here a set of options including overall settings like wet, dark.\nIf it is not going to be wet then no need for raindrops...')
    tkLabelConditions.grid(column=4, row=3)

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Conditions']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabConditions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabConditions.grid()
    
  tab(tabConditions)
  root.mainloop()

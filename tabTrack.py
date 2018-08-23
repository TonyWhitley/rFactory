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
    tkLabelTrack = tk.Label(parentFrame, 
                                text='Here a table of tracks that can be filtered and sorted by \
type/country/continent/year/decade/modder/star rating\nSimilar to Car tab')
    tkLabelTrack.grid(column=4, row=3)

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Track details']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabTrack = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabTrack.grid()
    
  tab(tabTrack)
  root.mainloop()

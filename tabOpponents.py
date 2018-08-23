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
    tkLabelOpponents = tk.Label(parentFrame, 
                                text='Here a table of cars that can be filtered and sorted by \
  Manufacturer/type/year/decade/modder/star rating\nAlso number of AI and AI strength factor')
    tkLabelOpponents.grid(column=4, row=3)

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Opponents']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabOpponents = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabOpponents.grid()
    
  tab(tabOpponents)
  root.mainloop()

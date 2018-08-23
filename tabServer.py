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
    tkLabelServer = tk.Label(parentFrame, 
                                text='Here a list of servers plus "Add server"')
    tkLabelServer.grid(column=4, row=3)

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Server', 'password']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':

  root = tk.Tk()
  tabServer = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabServer.grid()
    
  tab(tabServer)
  root.mainloop()

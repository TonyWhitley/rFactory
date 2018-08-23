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
    tkLabelScenarios = tk.Label(parentFrame, 
                                text='Here a list of scenario files to load plus "Save as..."')
    tkLabelScenarios.grid(column=4, row=3)

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Scenario - what does that mean? Scenario sets all tab settings']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    # Meaningless for this tab
    pass

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabScenarios = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabScenarios.grid()
    
  o_tab = Tab(tabScenarios)
  root.mainloop()

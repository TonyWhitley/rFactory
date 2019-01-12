# Python 3
import tkinter as tk
from tkinter import ttk, filedialog

from data.rFactoryConfig import scenarioFilesFolder,scenarioFilesExtension

root = None

def setMenubar(menubar):

    # create a pulldown menu, and add it to the menu bar
    #filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_command(label="Open scenario ", command=openScenario)
    menubar.add_separator()
    menubar.add_command(label="Save scenario", command=saveScenario, accelerator='Ctrl+S')
    menubar.master.bind_all("<Control-s>", saveScenario)
    menubar.add_command(label="Save scenario as...", command=saveScenarioAs)
    menubar.add_separator()
    menubar.add_command(label="Exit", command=menubar.master.quit)
    #menubar.add_cascade(label="File", menu=filemenu)

def openScenario():
  print('openScenario')
 
  #root = tk.Tk()
  filename =  filedialog.askopenfilename(initialdir = scenarioFilesFolder,title = "Select file",filetypes = (("rFactory Scenario files","*%s" % scenarioFilesExtension),("all files","*.*")))

def saveScenario():
  print('saveScenario')
def saveScenarioAs():
  filename =  filedialog.asksaveasfilename(initialdir = scenarioFilesFolder,title = "Select file",filetypes = (("rFactory Scenario files","*%s" % scenarioFilesExtension),("all files","*.*")))
  print('saveScenarioAs "%s%s"' % (filename, scenarioFilesExtension))

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    root = parentFrame
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

def dummy():
  pass

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabScenarios = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabScenarios.grid()

  menubar = tk.Menu(root)

  helpmenu = tk.Menu(menubar, tearoff=0)
  helpmenu.add_command(label="About", command=dummy)
  menubar.add_cascade(label="Help", menu=helpmenu)

  # display the menu
  #???? menubar.config(menu=menubar)
    
  o_tab = Tab(tabScenarios)
  setMenubar(menubar)

  root.mainloop()

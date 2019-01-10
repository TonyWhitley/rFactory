# Python 3
import tkinter as tk
from tkinter import ttk
from lib.tkToolTip import Tooltip

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabelConditions = tk.Label(parentFrame, 
                                text='This could be used to display the hierarchy of jobs and job definitions')
    tkLabelConditions.grid(column=1, row=1)
    
    tree = ttk.Treeview(parentFrame, columns=('size', 'modified'))
    tree['columns'] = ('size', 'modified', 'owner')
    tree.grid(column=1, row=2)

    # Inserted at the root, program chooses id:

    wraplength = 100
    tree.insert('', 'end', 'widgets', text='Widget Tour', values=('5KB Friday James'), open=True)
    Tooltip(tree, text='Tooltip...', wraplength=wraplength)
 
    # Same thing, but inserted as first child:
    tree.insert('', 0, 'gallery', text='Applications', values=('45KB Thursday Tony'))

    # Treeview chooses the id:
    id = tree.insert('', 'end', text='Tutorial', values=('15KB Yesterday mark'), open=True)

    # Inserted underneath an existing node:
    tree.insert('widgets', 'end', text='Canvas', values=('50KB Yesterday Leaf'))
    tree.insert(id, 'end', text='Tree', values=('90KB Yesterday Leaf2'))

    tree.set('widgets', 'size', '12KB')
    size = tree.set('widgets', 'size')
    tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))

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
    
  o_tab = Tab(tabConditions)
  root.mainloop()



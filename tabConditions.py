# Python 3
import tkinter as tk
from tkinter import ttk


def tab(parentFrame):
  """ Put this into the parent frame """
  pass
  tkLabelConditions = tk.Label(parentFrame, 
                              text='Here a set of options including overall settings like wet, dark.\nIf it is not going to be wet then no need for raindrops...')
  tkLabelConditions.grid(column=4, row=3)

if __name__ == '__main__':

  root = tk.Tk()
  tabConditions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabConditions.grid()
    
  tab(tabConditions)
  root.mainloop()

# Python 3
import tkinter as tk
from tkinter import ttk


def tab(parentFrame):
  """ Put this into the parent frame """
  pass
  tkLabelScenarios = tk.Label(parentFrame, 
                              text='Here a list of scenario files plus "Save as..."')
  tkLabelScenarios.grid(column=4, row=3)

if __name__ == '__main__':

  root = tk.Tk()
  tabScenarios = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabScenarios.grid()
    
  tab(tabScenarios)
  root.mainloop()

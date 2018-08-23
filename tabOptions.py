# Python 3
import tkinter as tk
from tkinter import ttk


def tab(parentFrame):
  """ Put this into the parent frame """
  pass
  tkLabelOptions = tk.Label(parentFrame, 
                              text='Here a set of options including Gearbox model, vehicle damage,\
time multiplier, Main AI strength factor, VR/Monitor')
  tkLabelOptions.grid(column=4, row=3)

if __name__ == '__main__':

  root = tk.Tk()
  tabOptions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabOptions.grid()
    
  tab(tabOptions)
  root.mainloop()

# Python 3
import tkinter as tk
from tkinter import ttk


def tab(parentFrame):
  """ Put this into the parent frame """
  pass
  tkLabelSessions = tk.Label(parentFrame, 
                              text='Practice, qually, warm up')
  tkLabelSessions.grid(column=4, row=3)

if __name__ == '__main__':

  root = tk.Tk()
  tabSessions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabSessions.grid()
    
  tab(tabSessions)
  root.mainloop()

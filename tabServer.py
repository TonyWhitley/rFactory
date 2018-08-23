# Python 3
import tkinter as tk
from tkinter import ttk


def tab(parentFrame):
  """ Put this into the parent frame """
  pass
  tkLabelServer = tk.Label(parentFrame, 
                              text='Here a list of servers plus "Add server"')
  tkLabelServer.grid(column=4, row=3)

if __name__ == '__main__':

  root = tk.Tk()
  tabServer = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabServer.grid()
    
  tab(tabServer)
  root.mainloop()

"""
Given the name of a server, mark (or unmark) it as favourite, store its password.
"""
# Python 3
import os
import tkinter as tk
from tkinter import ttk

from data.rFactoryConfig import rF2root,carTags,dataFilesExtension
from data.utils import writeFile

############################
# The Editor's public class:
############################
class Editor:
  def __init__(self, parentFrame, serverName, favourite, password):
    """ Put this into the parent frame """
    self.tkEditor = tk.Message(parentFrame, aspect=500)
    self.parentFrame = parentFrame

    self.labelServer = tk.Label(self.tkEditor, text=serverName)
    self.labelServer.grid(column=0, row=0, sticky='e')

    # Favourite checkbutton
    self.favourite = tk.IntVar()
    self.favourite.set(favourite)
    self.checkbutton = tk.Checkbutton(self.tkEditor, text='Favourite', variable=self.favourite)
    self.checkbutton.grid(column=1, row=0)

    # Password entry (plaintext, not asterisked)
    self.labelPassword = tk.Label(self.tkEditor, text='Password')
    self.labelPassword.grid(column=0, row=1, sticky='e')
    self.entryPassword = tk.Entry(self.tkEditor)
    self.entryPassword.grid(column=1, row=1, ipadx=20, pady=5, ipady=2)
    self.entryPassword.insert(0, password)

    # Show users?
    self.numFields = 2
    """
    self.tkEditor.columnconfigure(1, weight=1)

    self.numFields = len(fields)
    self.label = [0] * self.numFields
    self.entry = [0] * self.numFields
    for i, field in enumerate(fields):
      self.label[i] = tk.Label(self.tkEditor, text=field)
      self.label[i].grid(column=0, row=i, sticky='e')
      self.entry[i] = tk.Entry(self.tkEditor)
      self.entry[i].grid(column=1, row=i, ipadx=80, pady=5, ipady=2)
      self.entry[i].insert(0, data[field])
    """

    # Insert a blank line
    blank = tk.Label(self.tkEditor, text='')
    blank.grid(column=0, row=self.numFields, sticky='e')
    
    # Then the action buttons
    saveButton = tk.Button(self.tkEditor, text='Save', command=self.savePressed)
    cancelButton = tk.Button(self.tkEditor, text='Cancel', command=self.cancelPressed)

    saveButton.grid(column=0, row=self.numFields+1)
    cancelButton.grid(column=2, row=self.numFields+1)
    self.tkEditor.grid(ipadx=10, ipady=10)

  def savePressed(self):
    # Write the data to a file named by the unique ID field
    print(self.favourite.get())
    print(self.entryPassword.get())

    #_filepath = os.path.join(self.DatafilesFolder, _filename+dataFilesExtension)

    #writeFile(_filepath, text)
    self.cancelPressed()  # to close the window

  def cancelPressed(self):
    self.tkEditor.destroy()
    self.parentFrame.destroy()

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabServerFavourites = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  root.title('Editor')
  tabServerFavourites.grid()
    
  edit = 'password'

  if edit == 'favourite':
    o_tab = Editor(tabServerFavourites, 'Server 1', 1, '')

  elif edit == 'password':
    o_tab = Editor(tabServerFavourites, 'Server 2', 1, 'password')

  elif edit == 'notFavourite':
    o_tab = Editor(tabServerFavourites, 'Server 3', 0, '')

  root.mainloop()


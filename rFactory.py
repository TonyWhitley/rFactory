# Much hacking about to understand how tkinter can provide the GUI that's needed.

import tkinter as tk
from tkinter import ttk
 
import platform
 
def quit():
    global mainWindow
    mainWindow.destroy()
 
mainWindow = tk.Tk()
mainWindow.geometry('500x300')
mainWindow.title('rFactory')
mainWindow.columnconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=1)
mainWindow.columnconfigure(2, weight=1)
mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=1)
mainWindow.rowconfigure(2, weight=1)
mainWindow.rowconfigure(3, weight=1)
mainWindow.rowconfigure(4, weight=1)
 
tkLabelTop = tk.Label(mainWindow, text=" Here we are ")
tkLabelTop.grid()

"""
# Set style of tab labels
# but then disabled Tabs aren't greyed out
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [10, 5] },}})

style.theme_use("MyStyle") 
"""

notebook = ttk.Notebook(mainWindow)
tabNames = [ \
  'Car',
  'Track',
  'Opponents',
  'Conditions',
  'Sessions',
  'Options',
  'Scenarios'
]

tabHeight = 300
tabWidth = 400
tabs = {}
for name in tabNames:
  tabs[name] = ttk.Frame(notebook, height=tabHeight, width=tabWidth)
  tabs[name].config(relief='sunken', borderwidth=5)
  notebook.add(tabs[name], text=' %s ' % name)
#Works notebook.add(....., text=' Conditions ', state='disabled')
#notebook.tab(notebook.index(' Options '), state='disabled')

# tbd: names to tab_ids
notebook.tab(2, state='disabled')
notebook.tab(3, state='disabled')
notebook.select(5)


# Nah, not working
#tab6 = ttk.Notebook(frame5)
#frame61 = ttk.Frame(tab6)
#button = ttk.Button(tab6, SystemExit='Ooh! It\'s a button!')
#button.grid()
#notebook.add(frame61, text='Gearbox model')
tkLabel5 = tk.Label(tabs['Options'], text=" Hello World!")
tkLabel5.grid(column=4, row=3)
tkLabel5.columnconfigure(0, weight=1)
tkLabel5.columnconfigure(1, weight=1)
tkLabel5.columnconfigure(2, weight=1)

button = tk.Button(tabs['Options'], text='Ooh! It\'s a button!')
button.grid(column=5, row=2, sticky='e')


def online():
  pass

def offline():
  pass

def run():
  pass

notebook.grid()
 
tkButtonOnline = tk.Button(
    mainWindow,
    text="Online",
    width=20,
    height=2,
    command=online)
tkButtonOnline.grid(column=2, row=0)

tkButtonOffline = tk.Button(
    mainWindow,
    text="Offline",
    width=20,
    height=2,
    command=offline)
tkButtonOffline.grid(column=2, row=1)

tkButtonRun = tk.Button(
    mainWindow,
    text="Run rFactor 2",
    width=20,
    height=2,
    command=run)
tkButtonRun.grid(column=2, row=2)

tkButtonQuit = tk.Button(
    mainWindow,
    text="Quit",
    command=quit)
tkButtonQuit.grid(column=2, row=3)
  
tkDummyButton = tk.Button(
    tabs['Car'],
    text="Dummy Button")
tkDummyButton.grid(column=4, row=3)
   
tkLabel = tk.Label(tabs['Car'], text=" Hello Python!")
tkLabel.grid(column=4, row=3)
 
strVersion = "running Python version " + platform.python_version()
tkLabelVersion = tk.Label(tabs['Track'], text=strVersion)
tkLabelVersion.grid()
strPlatform = "Platform: " + platform.platform()
tkLabelPlatform = tk.Label(tabs['Track'], text=strPlatform)
tkLabelPlatform.grid(column=2, row=3)
 
width_of_window = 650 # The width of a GUI window. You can change this value to suit your preference

height_of_window = 480 # The height of a GUI window. You can change this value to suit your preference

# Fetch the monitor size and create the x & y coordinate 

screen_width = mainWindow.winfo_screenwidth() # this is fetching the mointor maximum width (typical mointors are 1920x1080)

screen_height = mainWindow.winfo_screenheight() # this is fetching the mointor maxium height

x_coordinate = (screen_width/2) - (width_of_window/2) # This is getting the correct x coordinate position for the GUI

y_coordinate = (screen_height/2) - (height_of_window/2)# This is getting the correct y coordinate position for the GUI

# Initialise the GUI's position 

mainWindow.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate)) # setting the position of the main window 

tk.mainloop()
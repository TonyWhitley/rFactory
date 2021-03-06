import sys

# Python 3
import tkinter as tk
from tkinter import ttk

from data.rFactoryConfig import player, rF2root

# tabGraphics (or something) needs all this magic to run ScriptedJsonEditor
# It also needs an API
# * run Jobs
# * backup and restore player.json  for 'Racing vs. replay only' option.

if getattr(sys, 'frozen', False):
    # running in a PyInstaller bundle (exe)
    SJE_path = r'ScriptedJsonEditor'
else:
    # running live under rFactory
    SJE_path = r'ScriptedJsonEditor\ScriptedJsonEditor'
try:
    sys.path.append(SJE_path)
    from GUI import Tab as GUI_Tab
    from GUI import setMenu2tab
    from GUImenu import Menu

    menubar = None
    menu2tab = None

    def setMenubar(_menubar):
        global menubar
        global menu2tab
        menubar = _menubar

        menu2tab = setMenu2tab(
            basedir=SJE_path,
            playerID=player,
            rF2root=rF2root)
        Menu(menubar=menubar, menu2tab=menu2tab)

    class Tab(GUI_Tab):
        def __init__(self, parentFrame):
            global menu2tab
            x = GUI_Tab(parentFrame, menu2tab, goCommand=True)

            """
      tkLabelframe_jobSettings = x.tkLabelframe_jobSettings

      o_tab = JobFrames(tkLabelframe_jobSettings)

      o_tab.set_checkbutton('G25_jobs', 'Monitor', 1)
      assert o_tab.get_checkbutton('G25_jobs', 'Monitor') == 1
      """

except ImportError as e:  # expected error if ScriptedJsonEditor is not present
    try:
        # but if that's not the error...
        assert (e.name == 'GUI' or e.name == 'GUImenu')

        def setMenubar(_menubar):
            pass

        class Tab:
            def __init__(self, parentFrame):
                """ Put this into the parent frame """
                tkLabelServer = tk.Label(
                    parentFrame, text='ScriptedJsonEditor module not present')
                tkLabelServer.grid(column=4, row=3)

            def getSettings(self):
                """ Return the settings for this tab """
                return ['Server name', 'Password']

            def setSettings(self, settings):
                """ Set the settings for this tab """
                pass

    # unexpected error (e.g ScriptedJsonEditor imports a lib not in rFactory's
    # env)
    except BaseException:
        raise e  # crash

if __name__ == '__main__':
    # To run this tab by itself for development
    root = tk.Tk()
    tabJson = ttk.Frame(
        root,
        width=1200,
        height=1200,
        relief='sunken',
        borderwidth=5)
    tabJson.grid()

    menubar = tk.Menu(root)

    menuLabel = 'JSON editor'
    # This makes a second copy of the menus
    #_menu = tk.Menu(menubar, tearoff=0)
    #menubar.add_cascade(label=menuLabel, menu=_menu)
    # setMenubar(_menu)
    menu2tab = setMenu2tab(SJE_path)
    Menu(menubar=menubar, menu2tab=menu2tab)
    # display the menu
    root.config(menu=menubar)

    o_tab = Tab(tabJson)

    root.mainloop()

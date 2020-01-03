# Python 3
import tkinter as tk
from tkinter import ttk

#########################
# The tab's public class:
#########################


class Tab:
    def __init__(self, parentFrame):
        """ Put this into the parent frame """
        pass
        tkLabelSessions = tk.Label(parentFrame,
                                   text='Practice, qually, warm up')
        tkLabelSessions.grid(column=4, row=3)

    def getSettings(self):
        """ Return the settings for this tab """
        return ['Sessions']

    def setSettings(self, settings):
        """ Set the settings for this tab """
        pass


if __name__ == '__main__':
    # To run this tab by itself for development
    root = tk.Tk()
    tabSessions = ttk.Frame(
        root,
        width=1200,
        height=1200,
        relief='sunken',
        borderwidth=5)
    tabSessions.grid()

    o_tab = Tab(tabSessions)
    root.mainloop()

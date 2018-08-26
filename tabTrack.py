# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Python 3

import tkinter as tk
from tkinter import ttk

from MC_table import Multicolumn_Listbox
from rFactoryConfig import config_tabTrack
from data import getAllTrackData
import carNtrackEditor

NOFILTER = '---' # String for not filtering

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    self.parentFrame = parentFrame
    self.settings = None #PyLint
    #tabTrack.trackColumns = ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating', 'Track DB file (hidden)']
    o_trackData = self.__TrackData()
    trackData = o_trackData.fetchData()


    self.mc = Multicolumn_Listbox(parentFrame, 
                             config_tabTrack['trackColumns'], 
                             stripped_rows=("white","#f2f2f2"), 
                             command=self.__on_select, 
                             right_click_command=self.__on_right_click,
                             adjust_heading_to_content=False, 
                             cell_anchor="center")

    # calculate the column widths to fit the headings and the data
    colWidths = []
    for col in config_tabTrack['trackColumns']:
      colWidths.append(len(col))
    for row in trackData:
      for col, column in enumerate(row):
        if len(column) > colWidths[col]:
          colWidths[col] = len(column)
      for col, column in enumerate(row):
        self.mc.configure_column(col, width=colWidths[col]*7+6)
    self.mc.configure_column(len(config_tabTrack['trackColumns'])-1, width=0, minwidth=0)
    # Justify the data in the first three columns
    self.mc.configure_column(0, anchor='w')
    self.mc.configure_column(1, anchor='w')
    self.mc.configure_column(2, anchor='w')
    self.mc.interior.grid(column=0, row=1, pady=2, columnspan=len(config_tabTrack['trackColumns']))

    #tabTrack.trackFilters = ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
    o_filter = self.__Filter(parentFrame, config_tabTrack['trackColumns'], colWidths, o_trackData, self.mc)
    col = 0
    for _filter in config_tabTrack['trackFilters']:
      o_filter.makeFilter(_filter, trackData, col)
      col += 1
   
    o_filter.filterUpdate(None) # Initial dummy filter to load data into table

    self.mc.select_row(0)

  def getSettings(self):
    """ Return the settings for this tab """
    return self.settings # filters too?  Probably not

  def setSettings(self, settings):
    """ Set the settings for this tab """
    trackID = settings[-1]
    i = 2 # the row for trackID 
    self.mc.deselect_all()  # clear what is selected.
    self.mc.select_row(i)
  
  def __on_select(self, data):
    self.settings = data
    print('DEBUG')
    print("called command when row is selected")
    print(data)
    print("\n")

  def __on_right_click(self, data):
    # don't change data   self.settings = data
    print('DEBUG')
    print("called command when row is right clicked")
    print(data)
    print("\n")

    top = tk.Toplevel(self.parentFrame)
    top.title("Track editor")

    fields = config_tabTrack['trackColumns']
    o_tab = carNtrackEditor.Editor(top, fields, data, command=self.answer)
    """
    t = 'Editor data: '
    for w in data:
      t += ' ' + str(w)
    msg = tk.Message(top, text=t, width=500)
    msg.pack()

    button = tk.Button(top, text="Dismiss", command=top.destroy)
    button.pack()
    """
  def answer(self, data):
    print('The response is')
    print(data)

  class __TrackData:
    """ Fetch and filter the track data """
    def __init__(self):
      self.dummyData = [
        ]
      self.data = None  # Pylint
      self.filteredData = None
    def fetchData(self):
      """ Fetch the raw data from wherever """
      self.data = getAllTrackData(tags=config_tabTrack['trackColumns'], maxWidth=27)
      #self.dummyData.copy() # dummy data for now
      print('DEBUG')
      for row in self.dummyData:
        print(len(row), row)
      return self.data
    def filterData(self, filters):
      """ filters is a list of column number,text pairs """
      _data = self.data.copy()
      for _filter in filters:
        _data = [elem for elem in _data if elem[_filter[0]] == _filter[1]() or _filter[1]() == NOFILTER]
      self.filteredData = _data
      return self.filteredData
    def setSelection(self, settings):
      """ Match settings to self.data, set table selection to that row """
      # tbd
      pass

  class __Filter:
    """ Filter combobox in frame """
    def __init__(self, mainWindow, columns, colWidths, o_trackData, mc):
      self.columns = columns
      self.colWidths = colWidths
      self.mainWindow = mainWindow
      self.o_trackData = o_trackData
      self.mc = mc
      self.filters = []
    def makeFilter(self, name, trackData, col):
      _column = self.columns.index(name)
      tkFilterText = tk.LabelFrame(self.mainWindow, text=name)
      tkFilterText.grid(column=col, row=0, pady=0)

      s = set()
      for item in trackData:
        s.add(item[_column])
      vals = [NOFILTER] + sorted(list(s))
      #modderFilter = tk.StringVar()
      tkComboFilter = ttk.Combobox(
          tkFilterText,
          #textvariable=modderFilter,
          width=self.colWidths[_column],
          height=len(vals))
      tkComboFilter['values'] = vals
      tkComboFilter.grid(column=1, row=0, pady=5)
      tkComboFilter.current(0)
      tkComboFilter.bind("<<ComboboxSelected>>", self.filterUpdate)
      self.filters.append([_column, tkComboFilter.get])
    
    def filterUpdate(self, event):
      """ Callback function when combobox changes """
      trackData = self.o_trackData.filterData(self.filters)
      self.mc.table_data = trackData
      self.mc.select_row(0)

    def resetFilters(self):
      """ Reset all the filters to --- """
      #tbd
      self.mc.select_row(0)

    def setFilters(self, settings):
      """ Set all the filters to settings """
      #tbd
      self.mc.select_row(0)


if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabTrack = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabTrack.grid()
    
  o_tab = Tab(tabTrack)

  root.mainloop()

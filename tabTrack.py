# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Python 3

import tkinter as tk
from tkinter import ttk

from MC_table import Multicolumn_Listbox
from rFactoryConfig import config_tabTrack, TrackDatafilesFolder
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
    for __, row in trackData.items():
      for col, column in enumerate(row):
        if len(row[column]) > colWidths[col]:
          colWidths[col] = len(row[column])
      for col, column in enumerate(row):
        self.mc.configure_column(col, width=colWidths[col]*7+6)
    # Hide the final column (contains DB file ID):
    self.mc.configure_column(len(config_tabTrack['trackColumns'])-1, width=0, minwidth=0)
    # Justify the data in the first three columns
    self.mc.configure_column(0, anchor='e')
    self.mc.configure_column(1, anchor='w')
    self.mc.configure_column(2, anchor='w')
    self.mc.interior.grid(column=0, row=1, pady=2, columnspan=len(config_tabTrack['trackColumns']))

    o_filter = self.__Filter(parentFrame, config_tabTrack['trackColumns'], colWidths, o_trackData, self.mc)
    for _filter in config_tabTrack['trackFilters']:
      o_filter.makeFilter(_filter, trackData)
   
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
    o_tab = carNtrackEditor.Editor(top, fields, data, DatafilesFolder=TrackDatafilesFolder, command=self.answer)
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
      self.data = None  # Pylint
      self.filteredData = None
    def fetchData(self):
      """ Fetch the raw data from wherever """
      self.data = getAllTrackData(tags=config_tabTrack['trackColumns'], maxWidth=20)
      return self.data
    def filterData(self, filters):
      """ 
      Filter items of the data dict that match all of the filter combobox selections.
      filters is a list of column name, comboBox text() function pairs """
      _data = []
      for _item, _values in self.data.items():
        _data.append(_values.items())

      self.filteredData = []
      for __, _row in self.data.items():
        _match = True
        for _filter in filters:
          if _row[_filter[0]] != _filter[1]() and _filter[1]() != NOFILTER:
            _match = False
            continue
        if _match:
          _r = []
          for colName in config_tabTrack['trackColumns']:
            _r.append(_row[colName])
          self.filteredData.append(_r)

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
    def makeFilter(self, filterName, trackData):
      tkFilterText = tk.LabelFrame(self.mainWindow, text=filterName)
      _col = self.columns.index(filterName)
      tkFilterText.grid(column=_col, row=0, pady=0)

      s = set()
      for __, item in trackData.items():
        s.add(item[filterName])
      vals = [NOFILTER] + sorted(list(s))
      #modderFilter = tk.StringVar()
      tkComboFilter = ttk.Combobox(
          tkFilterText,
          #textvariable=modderFilter,
          #height=len(vals),
          height=10,
          width=self.colWidths[_col])
      tkComboFilter['values'] = vals
      tkComboFilter.grid(column=1, row=0, pady=5)
      tkComboFilter.current(0)
      tkComboFilter.bind("<<ComboboxSelected>>", self.filterUpdate)
      self.filters.append([filterName, tkComboFilter.get])
    
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

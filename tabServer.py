# Python 3

import os
import tkinter as tk
from tkinter import ttk

from MC_table import Multicolumn_Listbox
from rFactoryConfig import config_tabServer, serverTags
##from data import getAllServerData, getSingleServerData
##import serverEditor

rF2_serverNotify_path = r'..\rF2_serverNotify\steps'
if os.path.exists(rF2_serverNotify_path):
  #sys.path.append(rF2_serverNotify_path)
  os.chdir(rF2_serverNotify_path)
  import rF2_serverNotify

NOFILTER = '---' # String for not filtering

dummyData = {
  'server 1': {'Favourite': 'N', 'Server Name': 'server 1', 'Track Name': 'Track 1', 'Humans': '3', 'Maybe': '0', 'AI': '0', 'Max': '20', 'Password': 'Y', 'Version': '11112', 'blank':''},
  'server 2': {'Favourite': 'N', 'Server Name': 'server 2', 'Track Name': 'Track 2', 'Humans': '3', 'Maybe': '0', 'AI': '0', 'Max': '20', 'Password': '', 'Version': '11112', 'blank':''},
  'server 3': {'Favourite': 'N', 'Server Name': 'server 3', 'Track Name': 'Track 3', 'Humans': '0', 'Maybe': '0', 'AI': '5', 'Max': '20', 'Password': 'N', 'Version': '11112', 'blank':''},
  'server 4': {'Favourite': 'N', 'Server Name': 'server 4', 'Track Name': 'Track 4', 'Humans': '0', 'Maybe': '5', 'AI': '0', 'Max': '20', 'Password': 'Y', 'Version': '11112', 'blank':''}
  }

dummyFavourites = {
  'server 1': 'password',
  'server 3': '',
  'server 4': 'XYZZY',
  }

def getAllServerData(tags, maxWidth):
  _serverData = {}
  serverObj = rF2_serverNotify.readServersFile()
  for server in serverObj.getServerNames():
    status, humans, AI, probables, info = serverObj.getPlayerCounts(server) 
    if status == 'OK':
      _entry = {}
      _entry['Favourite'] = 'N'
      _entry['Server Name'] = server
      _entry['Track Name'] = info['map']
      _entry['Humans'] = str(humans)
      _entry['Maybe'] = str(probables)
      _entry['AI'] = str(AI)
      _entry['Max'] = str(info['max_players'])
      _entry['Password'] = str(info['password_protected'])
      _entry['Version'] = info['version']
      _entry['blank'] = ''
      if _entry['Server Name'] in dummyFavourites:
        _entry['_serverData'] = 'Y'
        # _entry['Password'] = dummyFavourites[v['Server Name']]
      _serverData[server] = _entry

  return _serverData

def getSingleServerData(id, tags):
  pass

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    self.parentFrame = parentFrame
    self.settings = None #PyLint
    o_serverData = self.__ServerData()
    serverData = o_serverData.fetchData()


    self.mc = Multicolumn_Listbox(parentFrame, 
                             config_tabServer['serverColumns'], 
                             stripped_rows=("white","#f2f2f2"), 
                             command=self.__on_select, 
                             right_click_command=self.__on_right_click,
                             adjust_heading_to_content=False, 
                             cell_anchor="center")

    # calculate the column widths to fit the headings and the data
    colWidths = []
    for col in config_tabServer['serverColumns']:
      colWidths.append(len(col))
    for __, row in serverData.items():
      for col, column in enumerate(row):
        if len(row[column]) > colWidths[col]:
          colWidths[col] = len(row[column])
      for col, column in enumerate(row):
        self.mc.configure_column(col, width=colWidths[col]*7+6)
    self.mc.configure_column(len(config_tabServer['serverColumns'])-1, width=0, minwidth=0)
    # Justify the data in the first three columns
    self.mc.configure_column(0, anchor='e')
    self.mc.configure_column(1, anchor='w')
    self.mc.configure_column(2, anchor='w')
    self.mc.interior.grid(column=0, row=1, pady=2, columnspan=len(config_tabServer['serverColumns']))

    o_filter = self.__Filter(parentFrame, config_tabServer['serverColumns'], colWidths, o_serverData, self.mc)
    for _filter in config_tabServer['serverFilters']:
      o_filter.makeFilter(_filter, serverData)
   
    o_filter.filterUpdate(None) # Initial dummy filter to load data into table

    self.mc.select_row(0)

  def getSettings(self):
    """ Return the settings for this tab """
    return self.settings # filters too?  Probably not

  def setSettings(self, settings):
    """ Set the settings for this tab """
    serverID = settings[-1]
    i = 2 # the row for serverID 
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
    top.title("Server editor")

    fields = serverTags
    ##data = getSingleServerData(id=data[-1], tags=fields)
    ##o_tab = serverEditor.Editor(top, fields, data, DatafilesFolder=ServerDatafilesFolder)
    # Need to init the Tab again to get fresh data.


  class __ServerData:
    """ Fetch and filter the server data """
    def __init__(self):
      self.data = None  # Pylint
      self.filteredData = None
    def fetchData(self):
      """ Fetch the raw data from wherever """
      self.data = getAllServerData(tags=config_tabServer['serverColumns'], maxWidth=20)
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
          for colName in config_tabServer['serverColumns']:
            _r.append(_row[colName])
          self.filteredData.append(_r)

      return self.filteredData
    def setSelection(self, settings):
      """ Match settings to self.data, set table selection to that row """
      # tbd
      pass

  class __Filter:
    """ Filter combobox in frame """
    def __init__(self, mainWindow, columns, colWidths, o_serverData, mc):
      self.columns = columns
      self.colWidths = colWidths
      self.mainWindow = mainWindow
      self.o_serverData = o_serverData
      self.mc = mc
      self.filters = []
    def makeFilter(self, filterName, serverData):
      tkFilterText = tk.LabelFrame(self.mainWindow, text=filterName)
      _col = self.columns.index(filterName)
      tkFilterText.grid(column=_col, row=0, pady=0)

      s = set()
      for __, item in serverData.items():
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
      serverData = self.o_serverData.filterData(self.filters)
      self.mc.table_data = serverData
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
  tabServer = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabServer.grid()
    
  o_tab = Tab(tabServer)

  root.mainloop()

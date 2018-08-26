# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Python 3

import tkinter as tk
from tkinter import ttk

from MC_table import Multicolumn_Listbox
from rFactoryConfig import config_tabCar
from data import getAllCarData
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
    #tabCar.carColumns = ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating', 'Car DB file (hidden)']
    o_carData = self.__CarData()
    carData = o_carData.fetchData()


    self.mc = Multicolumn_Listbox(parentFrame, 
                             config_tabCar['carColumns'], 
                             stripped_rows=("white","#f2f2f2"), 
                             command=self.__on_select, 
                             right_click_command=self.__on_right_click,
                             adjust_heading_to_content=False, 
                             cell_anchor="center")

    # calculate the column widths to fit the headings and the data
    colWidths = []
    for col in config_tabCar['carColumns']:
      colWidths.append(len(col))
    for row in carData:
      for col, column in enumerate(row):
        if len(column) > colWidths[col]:
          colWidths[col] = len(column)
      for col, column in enumerate(row):
        self.mc.configure_column(col, width=colWidths[col]*7+6)
    self.mc.configure_column(len(config_tabCar['carColumns'])-1, width=0, minwidth=0)
    # Justify the data in the first three columns
    self.mc.configure_column(0, anchor='e')
    self.mc.configure_column(1, anchor='w')
    self.mc.configure_column(2, anchor='w')
    self.mc.interior.grid(column=0, row=1, pady=2, columnspan=len(config_tabCar['carColumns']))

    #tabCar.carFilters = ['Manufacturer', 'Model', 'Class', 'Author', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
    o_filter = self.__Filter(parentFrame, config_tabCar['carColumns'], colWidths, o_carData, self.mc)
    col = 0
    for _filter in config_tabCar['carFilters']:
      o_filter.makeFilter(_filter, carData, col)
      col += 1
   
    o_filter.filterUpdate(None) # Initial dummy filter to load data into table

    self.mc.select_row(0)

  def getSettings(self):
    """ Return the settings for this tab """
    return self.settings # filters too?  Probably not

  def setSettings(self, settings):
    """ Set the settings for this tab """
    carID = settings[-1]
    i = 2 # the row for carID 
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
    top.title("Car editor")

    fields = config_tabCar['carColumns']
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

  class __CarData:
    """ Fetch and filter the car data """
    def __init__(self):
      self.dummyData = [
          ['Ferrari',  '458', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Corvette', 'C7', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Bentley',  'Continental', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Eve',      'F1', 'F1', 'ISI', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'Historic Challenge_EVE_1968'],
          ['Spark',    'F1', 'F1', 'ISI', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'Historic Challenge_spark_1968'],
          ['Porsche',  '917K', 'Gp.C', 'Apex', 'GT', 'RWD', '1967', '1960-', '*****', 'FLAT12_917k_1971'],
          ['Lola',     'T70', 'Gp.C', 'Crossply', 'GT', 'RWD', '1974', '1970-', '***', 'car DB file'],
          ['Sauber',   'C11', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Sauber_C11'],
          ['Porsche',  '962C', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Porsche_062C'],
          ['Mazda',    '787B', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Mazda_787B'],
          ['Ferrari',  '312', 'F1', 'Chief Wiggum/Postipate', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'car DB file'],
          ['Caterham', '7', 'C7', 'MikeeCZ', 'Sports', 'RWD', '2016', '2010-', '****', 'car DB file']
        ]
      self.data = None  # Pylint
      self.filteredData = None
    def fetchData(self):
      """ Fetch the raw data from wherever """
      self.data = getAllCarData(tags=config_tabCar['carColumns'], maxWidth=20)
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
    def __init__(self, mainWindow, columns, colWidths, o_carData, mc):
      self.columns = columns
      self.colWidths = colWidths
      self.mainWindow = mainWindow
      self.o_carData = o_carData
      self.mc = mc
      self.filters = []
    def makeFilter(self, name, carData, col):
      _column = self.columns.index(name)
      tkFilterText = tk.LabelFrame(self.mainWindow, text=name)
      tkFilterText.grid(column=col, row=0, pady=0)

      s = set()
      for item in carData:
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
      carData = self.o_carData.filterData(self.filters)
      self.mc.table_data = carData
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
  tabCar = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabCar.grid()
    
  o_tab = Tab(tabCar)

  root.mainloop()

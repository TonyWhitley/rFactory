# Much hacking about to understand how tkinter can provide the GUI that's needed.
try:
    import tkinter as tk
    from tkinter import ttk
    import tkMessageBox as messagebox
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox

from MC_table import Multicolumn_Listbox

NOFILTER = '---' # String for not filtering

class CarData:
  """ Fetch and filter the car data """
  def __init__(self):
    self.dummyData = [
      ['Ferrari',  '458', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Corvette', 'C7', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Bentley',  'Continental', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Eve',      'F1', 'F1', 'S397', 'Open-wheel', 'RWD', '1967', '1960-', '*****' ],
      ['Spark',    'F1', 'F1', 'S397', 'Open-wheel', 'RWD', '1967', '1960-', '*****' ],
      ['Porsche',  '917K', 'Gp.C', 'Apex', 'GT', 'RWD', '1967', '1960-', '*****' ],
      ['Lola',     'T70', 'Gp.C', 'Crossply', 'GT', 'RWD', '1974', '1970-', '***' ],
      ['Sauber',   'C11', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Porsche',  '962C', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Mazda',    '787B', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Ferrari',  '312', 'F1', 'Chief Wiggum/Postipate', 'Open-wheel', 'RWD', '1967', '1960-', '*****' ],
      ['Caterham', '7', 'C7', 'MikeeCZ', 'Sports', 'RWD', '2016', '2010-', '****' ]
      ]
  def fetchData(self):
    """ Fetch the raw data from wherever """
    self.data = self.dummyData.copy() # dummy data for now
    print('DEBUG')
    for row in self.dummyData:
      print(len(row), row)
    return self.data
  def filterData(self, filters):
    """ filters is a list of column number,text pairs """
    _data = self.data.copy()
    for filter in filters:
      _data = [elem for elem in _data if elem[filter[0]] == filter[1]() or filter[1]() == NOFILTER]
    self.filteredData = _data
    return self.filteredData

class Filter:
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

def tab(parentFrame):
  """ Put this into the parent frame """
  carColumns = ['Manufacturer', 'Model', 'Class', 'Modder', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
  o_carData = CarData()
  carData = o_carData.fetchData()


  mc = Multicolumn_Listbox(parentFrame, carColumns, stripped_rows = ("white","#f2f2f2"), command=on_select, adjust_heading_to_content=False, cell_anchor="center")

  # calculate the column widths to fit the headings and the data
  colWidths = []
  for col in carColumns:
    colWidths.append(len(col))
  for row in carData:
    for col, column in enumerate(row):
      if len(column) > colWidths[col]:
        colWidths[col] = len(column)
  for col, column in enumerate(row):
      mc.configure_column(col, width=colWidths[col]*7+6)
  # Justify the data in the first three columns
  mc.configure_column(0, anchor='e')
  mc.configure_column(1, anchor='w')
  mc.configure_column(2, anchor='w')
  mc.interior.grid(column=0, row=1, pady=2, columnspan=len(carColumns))

  filters = ['Manufacturer', 'Model', 'Class', 'Modder', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
  o_filter = Filter(parentFrame, carColumns, colWidths, o_carData, mc)
  col = 0
  for filter in filters:
    o_filter.makeFilter(filter, carData, col)
    col += 1
   
  o_filter.filterUpdate(None) # Initial dummy filter to load data into table

  mc.select_row(0)

def on_select(data):
    print('DEBUG')
    print("called command when row is selected")
    print(data)
    print("\n")
        


if __name__ == '__main__':

    root = tk.Tk()
    carSelect = ttk.Frame(root, width=1200, height = 1200, relief='sunken', borderwidth=5)
    carSelect.grid()
    
    tab(carSelect)
    root.mainloop()


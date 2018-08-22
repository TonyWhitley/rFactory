# Much hacking about to understand how tkinter can provide the GUI that's needed.
# Combobox original code left in wrapped in """

from MC_table import Multicolumn_Listbox

NOFILTER = '---' # String for not filtering

class CarData:
  """ Fetch and filter the car data """
  def __init__(self):
    self.dummyData = [
      ['Ferrari', '458 GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Corvette', 'C7 GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Bentley', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Eve', 'F1', 'S397', 'F1', 'RWD', '1967', '1960-', '*****' ],
      ['Spark', 'F1', 'S397', 'F1', 'RWD', '1967', '1960-', '*****' ],
      ['Porsche', '917K', 'Apex', 'GT', 'RWD', '1967', '1960-', '*****' ],
      ['Lola', 'T70', 'Crossply', 'GT', 'RWD', '1974', '1970-', '***' ],
      ['Sauber', 'C11', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Porsche', '962C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Mazda', '787B', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Ferrari', '312', 'Chief Wiggum/Postipate', 'F1', 'RWD', '1967', '1960-', '*****' ],
      ['Caterham', '7', 'MikeeCZ', 'Sports', 'RWD', '2016', '2010-', '****' ]
      ]
  def fetchData(self):
    """ Fetch the raw data from wherever """
    self.data = self.dummyData.copy() # dummy data for now
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
  def __init__(self, mainWindow, columns, colWidths):
    self.columns = columns
    self.colWidths = colWidths
    self.mainWindow = mainWindow
    self.filters = []
  def makeFilter(self, name, carData, col):
    _column = self.columns.index(name)
    tkFilterText = tk.LabelFrame(self.mainWindow, text=name)
    tkFilterText.grid(column=col, row=0, pady=0)

    s = {NOFILTER}
    for item in carData:
      s.add(item[_column])
    vals = sorted(list(s))
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
    carData = o_carData.filterData(self.filters)
    mc.table_data = carData

if __name__ == '__main__':
    try:
        import tkinter as tk
        from tkinter import ttk
        import tkMessageBox as messagebox
    except ImportError:
        import tkinter as tk
        from tkinter import ttk
        from tkinter import messagebox

    root = tk.Tk()
    carSelect = ttk.Frame(root, width=1200, height = 1200, relief='sunken', borderwidth=5)
    carSelect.grid()
    
    def on_select(data):
        print("called command when row is selected")
        print(data)
        print("\n")
        
    def show_info(msg):
        messagebox.showinfo("Table Data", msg)

    """
    def filterUpdate(event=None):
      filters = [
        [2, tkComboModder.get],
        [3, tkComboType.get],
        [4, tkComboDrive.get]
        ]
      carData = o_carData.filterData(filters)
      mc.table_data = carData
      #show_info("mc.table_data(carData)")
    """


    carColumns = ['Manufacturer', 'Model', 'Modder', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
    o_carData = CarData()
    carData = o_carData.fetchData()


    mc = Multicolumn_Listbox(carSelect, carColumns, stripped_rows = ("white","#f2f2f2"), command=on_select, adjust_heading_to_content=False, cell_anchor="center")

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
    # Left justify the data in the first three columns
    mc.configure_column(0, anchor='e')
    mc.configure_column(1, anchor='w')
    mc.configure_column(2, anchor='w')
    mc.interior.grid(column=0, row=1, pady=2, columnspan=len(carColumns))

    """
    tkFilterText = tk.LabelFrame(carSelect, text="Modders")
    tkFilterText.grid(column=0, row=0, pady=5)

    s = {NOFILTER}
    for item in carData:
      s.add(item[2])
    vals = sorted(list(s))
    modderFilter = tk.StringVar()
    tkComboModder = ttk.Combobox(
      tkFilterText,
      textvariable=modderFilter,
      width=colWidths[2],
      height=len(vals))
    tkComboModder['values'] = vals
    tkComboModder.grid(column=1, row=0, pady=5)
    tkComboModder.current(0)
    tkComboModder.bind("<<ComboboxSelected>>", filterUpdate)
   
    tkTypes = tk.LabelFrame(carSelect, text="Types")
    tkTypes.grid(column=1, row=0, pady=5)

    s = {NOFILTER}
    for item in carData:
      s.add(item[3])
    vals = sorted(list(s))
    typeFilter = tk.StringVar()
    tkComboType = ttk.Combobox(
      tkTypes,
      textvariable=typeFilter,
      width=colWidths[3],
      height=len(vals))
    tkComboType['values'] = vals
    tkComboType.grid(column=0, row=0, pady=5)
    tkComboType.current(0)
    tkComboType.bind("<<ComboboxSelected>>", filterUpdate)
   
    tkDrive = tk.LabelFrame(carSelect, text="Drive")
    tkDrive.grid(column=2, row=0, pady=5)

    s = {NOFILTER}
    for item in carData:
      s.add(item[4])
    vals = sorted(list(s))
    driveFilter = tk.StringVar()
    tkComboDrive = ttk.Combobox(
      tkDrive,
      textvariable=driveFilter,
      width=colWidths[4],
      height=len(vals))
    tkComboDrive['values'] = vals
    tkComboDrive.grid(column=0, row=0, pady=5)
    tkComboDrive.current(0)
    tkComboDrive.bind("<<ComboboxSelected>>", filterUpdate)
    """

    o_filter = Filter(carSelect, carColumns, colWidths)
    o_filter.makeFilter('Manufacturer', carData, 0)
    o_filter.makeFilter('Model', carData, 1)
    o_filter.makeFilter('Modder', carData, 2)
    o_filter.makeFilter('Type', carData, 3)
    o_filter.makeFilter('Year', carData, 4)
    o_filter.makeFilter('Decade', carData, 6)
   
    o_filter.filterUpdate(None)

    mc.select_row(0)
    #show_info("mc.select_row(0)")

    root.mainloop()


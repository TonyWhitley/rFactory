from MC_table import Multicolumn_Listbox

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


    carColumns = ['Car', 'Modder', 'Type', 'F/R/4WD', 'Year', 'Decade', 'Rating']
    carData = [
      ['Ferrari 458 GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Corvette C7 GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Bentley GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****' ],
      ['Eve F1', 'S397', 'F1', 'RWD', '1967', '1960-', '*****' ],
      ['Spark F1', 'S397', 'F1', 'RWD', '1967', '1960-', '*****' ],
      ['Porsche 907', 'Unknown', 'GT', 'RWD', '1967', '1960-', '*****' ],
      ['Lola T70', 'Crossply', 'GT', 'RWD', '1974', '1970-', '***' ],
      ['Sauber C11', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Porsche 962C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Mazda 787B', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****' ],
      ['Ferrari 312', 'Chief Wiggum/Postipate', 'F1', 'RWD', '1967', '1960-', '*****' ],
      ['Caterham 7', 'MikeeCZ', 'Sports', 'RWD', '2016', '2010-', '****' ]
      ]
    mc = Multicolumn_Listbox(carSelect, carColumns, stripped_rows = ("white","#f2f2f2"), command=on_select, adjust_heading_to_content=False, cell_anchor="center")
    # calculate the column widths to fit the data
    colWidths = []
    for col in carColumns:
      colWidths.append(len(col))
    for row in carData:
      for col, column in enumerate(row):
        if len(column) > colWidths[col]:
          colWidths[col] = len(column)
    for col, column in enumerate(row):
        mc.configure_column(col, width=colWidths[col]*8)
    # Left justify the data in the first two columns
    mc.configure_column(0, anchor='w')
    mc.configure_column(1, anchor='w')
    mc.interior.grid(column=0, row=1, pady=5, columnspan=6)

    tkFilterText = tk.LabelFrame(carSelect, text="Modders")
    tkFilterText.grid(column=0, row=0, pady=5)

    s = {'---'}
    for item in carData:
      s.add(item[1])
    vals = sorted(list(s))
    modderFilter = tk.StringVar()
    tkComboModder = ttk.Combobox(
      tkFilterText,
      textvariable=modderFilter,
      width=colWidths[1],
      height=len(vals))
    tkComboModder['values'] = vals
    tkComboModder.grid(column=1, row=0, pady=5)
    tkComboModder.current(0)
   
    tkTypes = tk.LabelFrame(carSelect, text="Types")
    tkTypes.grid(column=1, row=0, pady=5)

    s = {'---'}
    for item in carData:
      s.add(item[2])
    vals = sorted(list(s))
    typeFilter = tk.StringVar()
    tkComboType = ttk.Combobox(
      tkTypes,
      textvariable=typeFilter,
      width=colWidths[2],
      height=len(vals))
    tkComboType['values'] = vals
    tkComboType.grid(column=0, row=0, pady=5)
    tkComboType.current(0)
   
    tkDrive = tk.LabelFrame(carSelect, text="Drive")
    tkDrive.grid(column=2, row=0, pady=5)

    s = {'---'}
    for item in carData:
      s.add(item[3])
    vals = sorted(list(s))
    driveFilter = tk.StringVar()
    tkComboDrive = ttk.Combobox(
      tkDrive,
      textvariable=driveFilter,
      width=colWidths[3],
      height=len(vals))
    tkComboDrive['values'] = vals
    tkComboDrive.grid(column=0, row=0, pady=5)
    tkComboDrive.current(0)
   
    mc.table_data = carData
    #show_info("mc.table_data(carData)")

    mc.select_row(0)
    #show_info("mc.select_row(0)")

    print("mc.selected_rows")
    print(mc.selected_rows)
    print("\n")
    
    print("mc.table_data")
    print(mc.table_data)
    print("\n")

    print("mc.row[0]")
    print(mc.row[0])
    print("\n")
    
    print("mc.row_data(0)")
    print(mc.row_data(0))
    print("\n")
    
    print("mc.column[1]")
    print(mc.column[1])
    print("\n")
    
    print("mc[0,1]")
    print(mc[0,1])
    print("\n")


    root.mainloop()


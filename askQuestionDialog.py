# crap. Radio buttons instead of proper yes / no / maybe buttons
import tkinter as tk
from tkinter import ttk

def ask_multiple_choice_question(parentFrame, prompt, options):
    if prompt:
        ttk.Label(parentFrame, text=prompt).pack()
    v = tk.IntVar()
    for i, option in enumerate(options):
        ttk.Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")
    ttk.Button(text="Submit", command=root.destroy).pack()
    if v.get() == 0: return None
    return options[v.get()]


if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  parentFrame = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)

  result = ask_multiple_choice_question(
      parentFrame,
      "What is your favorite color?",
      [
          "Blue!",
          "No -- Yellow!",
          "Aaaaargh!"
      ]
  )
  root.mainloop()


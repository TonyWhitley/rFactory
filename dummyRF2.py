import pprint
from tkinter import messagebox
 
def dummyRF2(settings, _password=None):
  """
  Function that accesses the same data files and dumps what rF2 would do with it
  """
  try:
    pp = pprint.pformat(settings, indent=2)
    if _password != None:
      pp += '\n\nPassword: %s' % _password
  except:
    pp = 'Error formatting settings'

  messagebox.askokcancel('Settings', pp)
  # showinfo does an annoying bleep
  return 'OK'

if __name__ == '__main__':
  settings = {'one':'setting'}
  dummyRF2(settings)
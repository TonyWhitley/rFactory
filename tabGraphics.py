# Python 3
import tkinter as tk
from tkinter import font, ttk

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabelConditions = tk.Label(parentFrame, 
                                text='Here a set of options including overall '
                                'settings like wet, dark.\nIf it is not going '
                                'to be wet then no need for raindrops...',
                                width=35,
                                wraplength=230,
                                justify=tk.LEFT)
    tkLabelConditions.grid(column=1, row=1, sticky='nw')

    self.graphicsSetup = {}
    self.vars = {}
    _tkCheckbuttons = {}
    _tkRadiobuttons = {}

    fontBold = font.Font(family='Helvetica', size=8, weight='bold', slant='italic')

    xPadding = 10
    ####################################################
    tkFrame_Conditions = tk.LabelFrame(parentFrame, text='rFactory control of graphics settings')
    tkFrame_Conditions.grid(column=1, row=2, sticky='nw', padx=xPadding)

    self._createVar('rFactoryControl', 'Full control')

    _tkRadiobuttons['Off'] = tk.Radiobutton(tkFrame_Conditions, 
                                           text='Off', 
                                           variable=self.vars['rFactoryControl'], 
                                           value='Off')
    _tkRadiobuttons['Off'].grid(sticky='w')

    _tkRadiobuttons['ReplayOnly'] = tk.Radiobutton(tkFrame_Conditions, 
                                           text='Racing vs. replay only', 
                                           variable=self.vars['rFactoryControl'], 
                                           state=tk.DISABLED,
                                           value='Replay only')
    _tkRadiobuttons['ReplayOnly'].grid(sticky='w')

    _tkRadiobuttons['FullControl'] = tk.Radiobutton(tkFrame_Conditions, 
                                           text='Full control', 
                                           variable=self.vars['rFactoryControl'], 
                                           value='Full control')
    _tkRadiobuttons['FullControl'].grid(sticky='w')

    ####################################################
    tkFrame_Conditions = tk.LabelFrame(parentFrame, text='Conditions')
    tkFrame_Conditions.grid(column=1, row=3, sticky='nw', padx=xPadding)

    self._createVar('MaybeRain', False)
    _tkCheckbuttons['MaybeRain'] = tk.Checkbutton(tkFrame_Conditions, 
      text='Rain is possible',
      variable=self.vars['MaybeRain'])

    self._createVar('NightRacing', False)
    _tkCheckbuttons['NightRacing'] = tk.Checkbutton(tkFrame_Conditions, 
      text='There will be racing in the dark',
      variable=self.vars['NightRacing'])

    _tkCheckbuttons['MaybeRain'].grid(sticky='w')
    _tkCheckbuttons['NightRacing'].grid(sticky='w')

    ####################################################
    tkFrame_GraphicsSetup = tk.LabelFrame(parentFrame, text='Graphics setup')
    tkFrame_GraphicsSetup.grid(column=2, row=1, rowspan=3, sticky='ew', padx=xPadding)

    _GraphicsCapabilityCol = 1
    self._createVar('GraphicsCapability', 5)
    
    tkLabel_GraphicsCapability = tk.Label(tkFrame_GraphicsSetup, 
                                          text='Overall\ngraphics\ncapability',
                                          font=fontBold,
                                          justify=tk.LEFT)
    tkLabel_GraphicsCapability.grid(column=_GraphicsCapabilityCol, row=1, sticky='nw')

    tkScale_GraphicsCapability = tk.Scale(tkFrame_GraphicsSetup, 
                                  from_=0, 
                                  to=10, 
                                  orient=tk.VERTICAL, 
                                  variable=self.vars['GraphicsCapability'])
    tkScale_GraphicsCapability.grid(column=_GraphicsCapabilityCol, row=2, rowspan=3, sticky='ew')

    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='Potato')
    tkLabel_Graphics_0.grid(column=_GraphicsCapabilityCol, row=2, sticky='nw')
    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsSetup, text='Ninja!')
    tkLabel_Graphics_10.grid(column=_GraphicsCapabilityCol, row=4, sticky='nw')

    _GraphicsPreferenceCol = 2
    self._createVar('GraphicsPreference', 5)
    
    tkLabel_GraphicsPreference = tk.Label(tkFrame_GraphicsSetup, 
                                          text='Graphics\npreference',
                                          font=fontBold,
                                          justify=tk.LEFT)
    tkLabel_GraphicsPreference.grid(column=_GraphicsPreferenceCol, row=1, sticky='n')
    tkScale_GraphicsPreference = tk.Scale(tkFrame_GraphicsSetup, 
                                  from_=0, 
                                  to=10, 
                                  orient=tk.VERTICAL, 
                                  variable=self.vars['GraphicsPreference'])
    tkScale_GraphicsPreference.grid(column=_GraphicsPreferenceCol, row=3, sticky='ewns')

    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsSetup, text='Frame rate')
    tkLabel_Graphics_10.grid(column=_GraphicsPreferenceCol, row=2, sticky='nw')
    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='Eye candy')
    tkLabel_Graphics_0.grid(column=_GraphicsPreferenceCol, row=4, sticky='nw')



  def _createVar(self, name, value):
    self.vars[name] = tk.StringVar(name=name)
    self.vars[name].set(value)

  def getSettings(self):
    """ Return the settings for this tab """
    for _v in self.vars:
      self.graphicsSetup[self.vars[_v]._name] = self.vars[_v].get()
    result = self.graphicsSetup
    return result

  def setSettings(self, settings):
    """ Set the settings for this tab """
    for _v in settings:
      try:
        self.vars[_v].set(settings[_v])
      except:
        pass # value error
    pass

#############################################################################
MAX_GRAPHICS_LEVEL = 10 # the number of levels of jobs of graphics settings
                        # (actually there are 11 as it starts at 0)
VR_FACTOR = 1.5         # Number representing the extra load of VR
RAIN_FACTOR = 1.1       # Number representing the extra load of rain
DARK_FACTOR = 1.1       # Number representing the extra load of darkness
EYE_CANDY_FACTOR = 20   # Number representing the extra load of eye candy preference 10
                        # [multiplier is (1 + ('GraphicsPreference'/EYE_CANDY_FACTOR)]
CARS_FACTOR = 200       # Number representing the extra load of visible cars
                        # [multiplier is (1 + (NumberOfCars/CARS_FACTOR)]
REPLAY_FACTOR = 1.5     # Number representing the extra load we're willing
                        # to accept for replays

def setGraphics(graphicsSetup,
                VR,
                carGraphicDetailsFactor, 
                trackGraphicDetailsFactor, 
                onlineOfflineReplay,
                NumberOfCars):
  """
  graphicsSetup
    rFactoryControl
      Off
      Replay only         !!!!! but if it pokes around to show a replay how do is it get back to player's original player.json????
      Full control
    MaybeRain
    NightRacing
    GraphicsCapability 
      0:  Running on a potato ;)
      10: Dual 2080 tis and watercooling!
    GraphicsPreference
      0:  Maximum frame rate
      10: Eye candy
  VR
  carGraphicDetailsFactor
    + / - percentage   (+ => it's a graphics hog)
  trackGraphicDetailsFactor
    + / - percentage
  onlineOfflineReplay
    Racing: racing online/offline 
    Replay: just viewing a replay
  """
  """
  ScriptedJsonEditor jobs available:
  graphicsLevel_0.json  : Potato
  ...
  graphicsLevel_10.json : Ninja

  graphicsRain_0.json   : Minimum rain settings, additional to graphicsLevel
  ...
  graphicsRain_5.json   : Maximum rain settings

  graphicsNight_0.json  : Minimum night settings, additional to graphicsLevel
  ...
  graphicsNight_5.json  : Maximum night settings

  graphicsReplay_0.json : Minimum replay settings, in place of graphicsLevel
  ...
  graphicsReplay_5.json : Maximum replay settings

  """
  ScriptedJsonEditorJobs = []

  if graphicsSetup['rFactoryControl'] == 'Off':
    # Don't alter graphics settings
    return ScriptedJsonEditorJobs

  graphicsLoad = 1
  if VR:
    graphicsLoad *= VR_FACTOR
  if graphicsSetup['MaybeRain'] != '0':
    graphicsLoad *= RAIN_FACTOR
  if graphicsSetup['NightRacing'] != '0':
    graphicsLoad *= DARK_FACTOR
  graphicsLoad *= (1 + (NumberOfCars/CARS_FACTOR))
  graphicsLoad *= carGraphicDetailsFactor
  graphicsLoad *= trackGraphicDetailsFactor

  if graphicsSetup['rFactoryControl'] == 'Replay only':
    if onlineOfflineReplay == 'Replay':
      # Full graphics unless GraphicsCapability low
      graphicsLoad *= REPLAY_FACTOR
      graphicsLevel = int(graphicsSetup['GraphicsCapability']) \
                      * (1 / graphicsLoad)
      if graphicsLevel > MAX_GRAPHICS_LEVEL:
        graphicsLevel = MAX_GRAPHICS_LEVEL
      ScriptedJsonEditorJobs = ['graphicsReplay_%d' % int(graphicsLevel/2)]
      # Only half the number of jobs to set replay levels
    # else  # Don't alter graphics settings
  elif graphicsSetup['rFactoryControl'] == 'Full control':
    graphicsLoad *= (1 + int(graphicsSetup['GraphicsPreference']) / EYE_CANDY_FACTOR)
    graphicsLevel = int(graphicsSetup['GraphicsCapability']) \
                    * (1 / graphicsLoad)
    if graphicsLevel > MAX_GRAPHICS_LEVEL:
      graphicsLevel = MAX_GRAPHICS_LEVEL
    ScriptedJsonEditorJobs = ['graphicsLevel_%d' % int(graphicsLevel)]
    if graphicsSetup['MaybeRain'] != '0':
      # Extra settings specific to rain
      ScriptedJsonEditorJobs.append('graphicsRain_%d' % int(graphicsLevel/2))
      # Only half the number of jobs to set rain levels
    if graphicsSetup['NightRacing'] != '0':
      # Extra settings specific to darkness
      ScriptedJsonEditorJobs.append('graphicsNight_%d' % int(graphicsLevel/2))
      # Only half the number of jobs to set night levels
      # (actually there are probably fewer than that, not many 
      # things specific to running in darkness to tweak)
  return ScriptedJsonEditorJobs
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabGraphics = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabGraphics.grid()
    
  o_tab = Tab(tabGraphics)
  root.mainloop()

  graphicsSetup = o_tab.getSettings()
  VR = True
  carGraphicDetailsFactor = 1.0
  trackGraphicDetailsFactor = 1.0
  onlineOfflineReplay = 'Replay'
  NumberOfCars = 20
  ScriptedJsonEditorJobs = setGraphics(graphicsSetup, 
                VR,
                carGraphicDetailsFactor, 
                trackGraphicDetailsFactor, 
                onlineOfflineReplay,
                NumberOfCars)
  pass


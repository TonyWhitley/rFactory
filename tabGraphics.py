# Python 3
import tkinter as tk
from tkinter import font, ttk

from lib.tkToolTip import Tooltip

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame, graphicsDemands=False):
    """ Put this into the parent frame """
    # graphicsDemands could be handled with a sub class
    self.graphicsSetup = {}
    self.vars = {}
    _tkCheckbuttons = {}
    _tkRadiobuttons = {}

    fontBoldItalic = font.Font(family='Helvetica', size=8, weight='bold', slant='italic')
    fontBold = font.Font(family='Helvetica', size=8, weight='bold')

    xPadding = 10
    ####################################################
    self._createVar('rFactoryControl', 'Full control')

    tkFrame_Controls = tk.LabelFrame(parentFrame,
                                        text='Graphics settings')
    tkFrame_Controls.grid(column=1, row=1, sticky='nw', padx=xPadding)
    if not graphicsDemands:

        _tkRadiobuttons['Off'] = tk.Radiobutton(tkFrame_Controls,
                                               text='Off',
                                               variable=self.vars['rFactoryControl'],
                                               value='Off')
        _tkRadiobuttons['Off'].grid(sticky='w')

        _tkRadiobuttons['FullControl'] = tk.Radiobutton(tkFrame_Controls,
                                               text='Full control',
                                               variable=self.vars['rFactoryControl'],
                                               value='Full control')
        _tkRadiobuttons['FullControl'].grid(sticky='w')
    else:
        self._createVar('VR', '0')
        _tkCheckbuttons['VR'] = tk.Checkbutton(tkFrame_Controls,
          text='VR',
          variable=self.vars['VR'])
        _tkCheckbuttons['VR'].grid(sticky='w')

    self._createVar('ReplayOnly', '0')
    _tkCheckbuttons['ReplayOnly'] = tk.Checkbutton(tkFrame_Controls,
                                            text='Replay only',
                                            variable=self.vars['ReplayOnly'])
    _tkCheckbuttons['ReplayOnly'].grid(sticky='w')

    ####################################################
    tkFrame_Conditions = tk.LabelFrame(parentFrame, text='Conditions')
    tkFrame_Conditions.grid(column=1, sticky='nw', padx=xPadding)

    self._createVar('NumberOfCars', 15)
    if graphicsDemands:
        _NumberOfCarsCol = 0
        tkLabel_NumberOfCars = tk.Label(tkFrame_Conditions,
                                              text='Approx number of cars',
                                              font=fontBold,
                                              justify=tk.LEFT)
        tkLabel_NumberOfCars.grid(column=_NumberOfCarsCol,
                                          row=0,
                                          sticky='sw')

        tkScale_NumberOfCars = tk.Scale(tkFrame_Conditions,
                                      from_=5,
                                      to=50,
                                      resolution=5,
                                      orient=tk.HORIZONTAL,
                                      variable=self.vars['NumberOfCars'])
        tkScale_NumberOfCars.grid(column=_NumberOfCarsCol+1,
                                          row=0,
                                          sticky='ew')

    self._createVar('MaybeRain', False)
    _tkCheckbuttons['MaybeRain'] = tk.Checkbutton(tkFrame_Conditions,
      text='Rain is possible',
      variable=self.vars['MaybeRain'])
    Tooltip(_tkCheckbuttons['MaybeRain'], text='No rain, '\
        'no need for raindrops\nRain impacts graphics performance')
    self._createVar('NightRacing', False)
    _tkCheckbuttons['NightRacing'] = tk.Checkbutton(tkFrame_Conditions,
      text='There will be racing in the dark',
      variable=self.vars['NightRacing'])
    Tooltip(_tkCheckbuttons['NightRacing'], text='No night racing, '\
        'no need for headlights\nNight racing impacts graphics performance')

    _tkCheckbuttons['MaybeRain'].grid(sticky='w')
    _tkCheckbuttons['NightRacing'].grid(sticky='w', columnspan=2)

    ####################################################
    tkFrame_GraphicsSetup = tk.LabelFrame(parentFrame, text='Graphics setup')
    tkFrame_GraphicsSetup.grid(column=2, row=0, rowspan=3, sticky='new', padx=xPadding)

    _GraphicsCapabilityCol = 1
    self._createVar('GraphicsCapability', 5)

    tkLabel_GraphicsCapability = tk.Label(tkFrame_GraphicsSetup,
                                          text='Overall\ngraphics\ncapability',
                                          font=fontBoldItalic,
                                          justify=tk.LEFT)
    tkLabel_GraphicsCapability.grid(column=_GraphicsCapabilityCol, row=1, sticky='nw')

    tkScale_GraphicsCapability = tk.Scale(tkFrame_GraphicsSetup,
                                  from_=0,
                                  to=10,
                                  orient=tk.VERTICAL,
                                  variable=self.vars['GraphicsCapability'])
    tkScale_GraphicsCapability.grid(column=_GraphicsCapabilityCol, row=2, rowspan=3, sticky='ew')
    Tooltip(tkScale_GraphicsCapability, text='How powerful is your graphics card and PC?')

    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='Potato')
    tkLabel_Graphics_0.grid(column=_GraphicsCapabilityCol, row=2, sticky='nw')
    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsSetup, text='Ninja!')
    tkLabel_Graphics_10.grid(column=_GraphicsCapabilityCol, row=4, sticky='nw')

    _VRAMcol = 2
    self._createVar('VRAM', 8)

    tkLabel_VRAM = tk.Label(tkFrame_GraphicsSetup,
                                          text='Video\nRAM\nsize',
                                          font=fontBoldItalic,
                                          justify=tk.CENTER)
    tkLabel_VRAM.grid(column=_VRAMcol, row=1, sticky='new')

    tkScale_VRAM = tk.Scale(tkFrame_GraphicsSetup,
                                  from_=1,
                                  to=16,
                                  orient=tk.VERTICAL,
                                  variable=self.vars['VRAM'])
    tkScale_VRAM.grid(column=_VRAMcol, row=2, rowspan=3, sticky='w')
    Tooltip(tkScale_VRAM, text='How much RAM does your graphics have?')

    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='GB')
    tkLabel_Graphics_0.grid(column=_VRAMcol, row=2, sticky='new')

    _GraphicsPreferenceCol = 3
    self._createVar('GraphicsPreference', 5)

    tkLabel_GraphicsPreference = tk.Label(tkFrame_GraphicsSetup,
                                          text='Graphics\npreference',
                                          font=fontBoldItalic,
                                          justify=tk.LEFT)
    tkLabel_GraphicsPreference.grid(column=_GraphicsPreferenceCol,
                                    row=1,
                                    sticky='n')
    tkScale_GraphicsPreference = tk.Scale(tkFrame_GraphicsSetup,
                                  from_=0,
                                  to=10,
                                  orient=tk.VERTICAL,
                                  variable=self.vars['GraphicsPreference'])
    tkScale_GraphicsPreference.grid(column=_GraphicsPreferenceCol,
                                    row=3,
                                    sticky='ewns')
    Tooltip(tkScale_GraphicsPreference, text='Do you prefer performance or eye candy?')

    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsSetup, text='Frame rate')
    tkLabel_Graphics_10.grid(column=_GraphicsPreferenceCol, row=2, sticky='nw')
    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='Eye candy')
    tkLabel_Graphics_0.grid(column=_GraphicsPreferenceCol, row=4, sticky='nw')

    ####################################################
    if not graphicsDemands:
        return  # This frame is not required, graphics demands are set by rFactory

    tkFrame_GraphicsDemands = tk.LabelFrame(parentFrame, text='Graphics demands')
    tkFrame_GraphicsDemands.grid(column=3,
                                 row=0,
                                 rowspan=3,
                                 sticky='nsew',
                                 padx=xPadding)

    _CarGraphicsDemandsCol = 1
    self._createVar('CarGraphicsDemands', 0)

    tkLabel_CarGraphicsDemands = tk.Label(tkFrame_GraphicsDemands,
                                          text='CAR\ndemands',
                                          font=fontBoldItalic,
                                          justify=tk.CENTER)
    tkLabel_CarGraphicsDemands.grid(column=_CarGraphicsDemandsCol,
                                    row=1,
                                    sticky='nw')

    tkScale_CarGraphicsDemands = tk.Scale(tkFrame_GraphicsDemands,
                                  from_=-5,
                                  to=5,
                                  orient=tk.VERTICAL,
                                  variable=self.vars['CarGraphicsDemands'])
    tkScale_CarGraphicsDemands.grid(column=_CarGraphicsDemandsCol,
                                    row=3,
                                    rowspan=3,
                                    sticky='ew')
    Tooltip(tkScale_CarGraphicsDemands, text="Is the car you're using well\n"\
        "optimised or an FPS killer?")

    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsDemands, text='Optimised')
    tkLabel_Graphics_0.grid(column=_CarGraphicsDemandsCol, row=2, sticky='nw')
    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsDemands, text='Heavy')
    tkLabel_Graphics_10.grid(column=_CarGraphicsDemandsCol, row=6, sticky='nw')

    _TrackGraphicsDemandsCol = 2
    self._createVar('TrackGraphicsDemands', 0)

    tkLabel_TrackGraphicsDemands = tk.Label(tkFrame_GraphicsDemands,
                                          text='TRACK\ndemands',
                                          font=fontBoldItalic,
                                          justify=tk.CENTER)
    tkLabel_TrackGraphicsDemands.grid(column=_TrackGraphicsDemandsCol,
                                      row=1,
                                      sticky='nw')

    tkScale_TrackGraphicsDemands = tk.Scale(tkFrame_GraphicsDemands,
                                  from_=-5,
                                  to=5,
                                  orient=tk.VERTICAL,
                                  variable=self.vars['TrackGraphicsDemands'])
    tkScale_TrackGraphicsDemands.grid(column=_TrackGraphicsDemandsCol,
                                      row=3,
                                      rowspan=3,
                                      sticky='ew')
    Tooltip(tkScale_TrackGraphicsDemands, text="Is the track you're using well\n"\
        "optimised or an FPS killer?")

    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsDemands, text='Optimised')
    tkLabel_Graphics_0.grid(column=_TrackGraphicsDemandsCol, row=2, sticky='nw')
    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsDemands, text='Heavy')
    tkLabel_Graphics_10.grid(column=_TrackGraphicsDemandsCol, row=6, sticky='nw')


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
      Full control              Set up a new user called Replay and call rF2 using that profile.
    MaybeRain
    NightRacing
    GraphicsCapability
      0:  Running on a potato ;)
      10: Dual 2080 tis and watercooling!
    VRAM (GB)
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

  # if graphicsDemands then user defines these values
  if 'VR' in graphicsSetup:
      VR = graphicsSetup['VR'] == '1'
  if 'ReplayOnly' in graphicsSetup:
      if graphicsSetup['ReplayOnly'] == '1':
          onlineOfflineReplay = 'Replay'
  if 'NumberOfCars' in graphicsSetup:
      NumberOfCars = int(graphicsSetup['NumberOfCars'])
  if 'CarGraphicsDemands' in graphicsSetup:
      carGraphicDetailsFactor = int(graphicsSetup['CarGraphicsDemands'])*2
  if 'TrackGraphicsDemands' in graphicsSetup:
      trackGraphicDetailsFactor = int(graphicsSetup['TrackGraphicsDemands'])*2

  graphicsLoad = 1
  if VR:
    graphicsLoad *= VR_FACTOR
  if graphicsSetup['MaybeRain'] != '0':
    graphicsLoad *= RAIN_FACTOR
  if graphicsSetup['NightRacing'] != '0':
    graphicsLoad *= DARK_FACTOR

  graphicsLoad *= (1 + (NumberOfCars/CARS_FACTOR))
  graphicsLoad *= (1 + carGraphicDetailsFactor)
  graphicsLoad *= (1 + trackGraphicDetailsFactor)

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
    if int(graphicsSetup['VRAM']) < 5:
      # Extra settings to reduce VRAM usage
      ScriptedJsonEditorJobs.append('graphicsVRAMlow')
    elif int(graphicsSetup['VRAM']) < 9:
      # Extra settings to reduce VRAM usage
      ScriptedJsonEditorJobs.append('graphicsVRAMmedium')
    else:
      ScriptedJsonEditorJobs.append('graphicsVRAMmax')
  return ScriptedJsonEditorJobs

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  root.title('rFactor 2 Graphics Manager')
  tabGraphics = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabGraphics.grid()

  o_tab = Tab(tabGraphics, graphicsDemands=True)
  root.mainloop()

  graphicsSetup = o_tab.getSettings()
  VR = True
  carGraphicDetailsFactor = 1.0
  trackGraphicDetailsFactor = 1.0
  onlineOfflineReplay = 'Replay'
  player = 'Replay'
  NumberOfCars = 20
  ScriptedJsonEditorJobs = setGraphics(graphicsSetup,
                VR,
                carGraphicDetailsFactor,
                trackGraphicDetailsFactor,
                onlineOfflineReplay,
                NumberOfCars)
  # not defined yet  runScriptedJsonEditor(player, ScriptedJsonEditorJobs)
  pass


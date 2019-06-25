# Python 3
import tkinter as tk
from tkinter import ttk

from lib.tkToolTip import Tooltip
wraplength = 100

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabel_Options = tk.Label(parentFrame, 
                                text='Here a set of options including Gearbox model, vehicle damage,\
time multiplier, Main AI strength factor, VR/Monitor\n(doesn\'t do anything yet)')
    tkLabel_Options.grid(column=1, row=1, columnspan=3)
    self.settings = {}
    self.vars = {}
    _tkCheckbuttons = {}
    _tkRadiobuttons = {}

    xPadding = 10
    ####################################################
    tkFrame_Gearbox = tk.LabelFrame(parentFrame, text='Gearbox')
    tkFrame_Gearbox.grid(column=1, row=2, sticky='ew', padx=xPadding)

    self._createVar('RequireClutch', False)
    _tkCheckbuttons['RequireClutch'] = tk.Checkbutton(tkFrame_Gearbox, 
                                                 text='Require clutch (Grinding Tranny)',
                                                 variable=self.vars['RequireClutch'])
    self._createVar('AutoClutch', True)
    _tkCheckbuttons['AutoClutch'] = tk.Checkbutton(tkFrame_Gearbox, 
                                              text='Auto clutch (std. rF2)',
                                              variable=self.vars['AutoClutch'])

    self._createVar('AutoBlip', True)
    _tkCheckbuttons['AutoBlip'] = tk.Checkbutton(tkFrame_Gearbox, 
                                              text='Auto Blip (std. rF2)',
                                              variable=self.vars['AutoBlip'])
    #_tkCheckbuttons['GearDamage'] = tk.Checkbutton(tkFrame_Gearbox, text='Gearbox damage')

    _tkCheckbuttons['RequireClutch'].grid(sticky='w')
    _tkCheckbuttons['AutoClutch'].grid(sticky='w')
    _tkCheckbuttons['AutoBlip'].grid(sticky='w')
    #_tkCheckbuttons['GearDamage'].grid(sticky='w')

    ####################################################
    tkFrame_Monitor = tk.LabelFrame(parentFrame, text='Monitor', padx=xPadding)
    tkFrame_Monitor.grid(column=1, row=3, sticky='ew')

    self._createVar('Monitor', 'Monitor')
    _tkRadiobuttons['Monitor'] = tk.Radiobutton(tkFrame_Monitor, 
                                                text='Monitor', 
                                                variable=self.vars['Monitor'], 
                                                value='Monitor')
    _tkRadiobuttons['VR'] = tk.Radiobutton(tkFrame_Monitor, 
                                           text='VR', 
                                           variable=self.vars['Monitor'], 
                                           value='VR')
    _tkRadiobuttons['Monitor'].grid(sticky='w')
    _tkRadiobuttons['VR'].grid(sticky='w')
    _tkRadiobuttons['Monitor'].update()

    ####################################################
    tkFrame_AIstrength = tk.LabelFrame(parentFrame, text='AI', padx=xPadding)
    tkFrame_AIstrength.grid(column=1, row=4, sticky='ew')

    self._createVar('AIstrength', 100)
    tkLabel_AIstrength = tk.Label(tkFrame_AIstrength, text='Overall AI strength\n(combined with car\nand track factors)')
    tkLabel_AIstrength.grid(column=1, row=1, sticky='e')
    tkScale_AIstrength = tk.Scale(tkFrame_AIstrength, 
                                  from_=95, 
                                  to=110, 
                                  orient=tk.HORIZONTAL, 
                                  variable=self.vars['AIstrength'])
    tkScale_AIstrength.grid(column=2, row=1, sticky='ewns')

    self._createVar('AIaggression', 100)
    tkLabel_AIaggression = tk.Label(tkFrame_AIstrength, text='AI aggression (std. rF2)')
    tkLabel_AIaggression.grid(column=1, row=2, sticky='e')
    tkScale_AIaggression = tk.Scale(tkFrame_AIstrength, 
                                    from_=0, 
                                    to=100, 
                                    orient=tk.HORIZONTAL,
                                    variable=self.vars['AIaggression'])
    tkScale_AIaggression.grid(column=2, row=2, sticky='ewns')

    self._createVar('AIlimiter', 100)
    tkLabel_AIlimiter = tk.Label(tkFrame_AIstrength, text='AI limiter (std. rF2)')
    tkLabel_AIlimiter.grid(column=1, row=3, sticky='e')
    tkScale_AIlimiter = tk.Scale(tkFrame_AIstrength, 
                                 from_=0, 
                                 to=100, 
                                 orient=tk.HORIZONTAL,
                                 variable=self.vars['AIlimiter'])
    tkScale_AIlimiter.grid(column=2, row=3, sticky='ewns')

    ####################################################
    tkFrame_Damage = tk.LabelFrame(parentFrame, text='Damage', padx=xPadding)
    tkFrame_Damage.grid(column=3, row=2, sticky='ew')

    self._createVar('GearDamage', False)
    _tkCheckbuttons['GearDamage'] = tk.Checkbutton(tkFrame_Damage,
                                              text='Gearbox damage (Grinding Tranny)',
                                              variable=self.vars['GearDamage'])

    self._createVar('MechanicalFailure', False)
    _tkCheckbuttons['MechanicalFailure'] = tk.Checkbutton(tkFrame_Damage, 
                                                     text='Mechanical Failure\n(should be\nOff/Normal/Time scaled)',
                                                     variable=self.vars['MechanicalFailure'])

    self._createVar('Invulnerability', False)
    _tkCheckbuttons['Invulnerability'] = tk.Checkbutton(tkFrame_Damage, 
                                                   text='Invulnerability (std. rF2)',
                                                   variable=self.vars['Invulnerability'])

    _tkCheckbuttons['GearDamage'].grid(sticky='w')
    _tkCheckbuttons['MechanicalFailure'].grid(sticky='w')
    _tkCheckbuttons['Invulnerability'].grid(sticky='w')

    ####################################################
    tkFrame_RaceOptions = tk.LabelFrame(parentFrame, text='Race Options', padx=xPadding)
    tkFrame_RaceOptions.grid(column=3, row=3, sticky='ew')

    self._createVar('RaceTime', 20)
    _tkCheckbuttons['RaceTime'] = tk.Checkbutton(tkFrame_RaceOptions,
                                            text='Race time (complicated...)',
                                            variable=self.vars['RaceTime'])

    self._createVar('Timescale', False)
    _tkCheckbuttons['Timescale'] = tk.Checkbutton(tkFrame_RaceOptions,
                                            text='Timescale (list of options)',
                                            variable=self.vars['Timescale'])

    self._createVar('FinishCriteria', False)
    _tkCheckbuttons['FinishCriteria'] = tk.Checkbutton(tkFrame_RaceOptions, 
                                                  text='FinishCriteria - laps/time and...',
                                                  variable=self.vars['FinishCriteria'])

    self._createVar('Laps', 5)
    _tkCheckbuttons['Laps'] = tk.Checkbutton(tkFrame_RaceOptions, text='slider?')

    _tkCheckbuttons['RaceTime'].grid(sticky='w')
    _tkCheckbuttons['Timescale'].grid(sticky='w')
    _tkCheckbuttons['FinishCriteria'].grid(sticky='w')
    _tkCheckbuttons['Laps'].grid(sticky='w')

    ####################################################
    tkFrame_Co_programs = tk.LabelFrame(parentFrame, text='Other programs to run with rF2', padx=xPadding)
    tkFrame_Co_programs.grid(column=3, row=4, sticky='ew')

    self._createVar('CrewChief', False)
    _tkCheckbuttons['CrewChief'] = tk.Checkbutton(tkFrame_Co_programs, 
                                             text='Crew Chief',
                                             variable=self.vars['CrewChief'])
    Tooltip(_tkCheckbuttons['CrewChief'],
            text='Spotter and voice control',
            wraplength=wraplength)

    self._createVar('Discord', False)
    _tkCheckbuttons['Discord'] = tk.Checkbutton(tkFrame_Co_programs, 
                                           text='Discord (voice)',
                                           variable=self.vars['Discord'])
    Tooltip(_tkCheckbuttons['Discord'],
            text='Voice chat between drivers',
            wraplength=wraplength)

    self._createVar('VolumeControl', False)
    _tkCheckbuttons['VolumeControl'] = tk.Checkbutton(tkFrame_Co_programs, 
                                             text='VolumeControl',
                                             variable=self.vars['VolumeControl'])
    Tooltip(_tkCheckbuttons['VolumeControl'],
            text='Buttons to adjust volume of rF2 and co-programs', 
            wraplength=wraplength)

    self._createVar('TeamSpeak', False)
    _tkCheckbuttons['TeamSpeak'] = tk.Checkbutton(tkFrame_Co_programs, 
                                             text='TeamSpeak',
                                             variable=self.vars['TeamSpeak'])
    Tooltip(_tkCheckbuttons['TeamSpeak'],
            text='Voice chat between drivers',
            wraplength=wraplength)

    self._createVar('MyPreCommand', False)
    _tkCheckbuttons['MyPreCommand'] = tk.Checkbutton(tkFrame_Co_programs, 
                                           text='My command to run before rF2',
                                           variable=self.vars['MyPreCommand'])

    self._createVar('MyPostCommand', False)
    _tkCheckbuttons['MyPostCommand'] = tk.Checkbutton(tkFrame_Co_programs, 
                                           text='My command to run after rF2',
                                           variable=self.vars['MyPostCommand'])

    _tkCheckbuttons['CrewChief'].grid(sticky='w')
    _tkCheckbuttons['Discord'].grid(sticky='w')
    _tkCheckbuttons['VolumeControl'].grid(sticky='w')
    _tkCheckbuttons['TeamSpeak'].grid(sticky='w')
    _tkCheckbuttons['MyPreCommand'].grid(sticky='w')
    _tkCheckbuttons['MyPostCommand'].grid(sticky='w')

    ####################################################
    tkFrame_debug = tk.LabelFrame(parentFrame, text='Debug', padx=xPadding)
    tkFrame_debug.grid(column=3, row=5, sticky='ew')

    self._createVar('DummyRF2', True)
    _tkCheckbuttons['Dummy_rF2'] = tk.Checkbutton(tkFrame_debug, 
      text='Run dummy rF2\nprogram that accesses\nthe same data files and\ndumps what rF2\nwould do with it',
      variable=self.vars['DummyRF2'])

    self._createVar('RunCoPrograms', True)
    _tkCheckbuttons['RunCoPrograms'] = tk.Checkbutton(tkFrame_debug, 
      text='Run co-programs with dummy rF2',
      variable=self.vars['RunCoPrograms'])

    _tkCheckbuttons['Dummy_rF2'].grid(sticky='w')
    _tkCheckbuttons['RunCoPrograms'].grid(sticky='w')

  def _createVar(self, name, value):
    self.vars[name] = tk.StringVar(name=name)
    self.vars[name].set(value)

  def getSettings(self):
    """ Return the settings for this tab """
    for _v in self.vars:
      self.settings[self.vars[_v]._name] = self.vars[_v].get()
    result = self.settings
    return result

  def setSettings(self, settings):
    """ Set the settings for this tab """
    for _v in settings:
      try:
        self.vars[_v].set(settings[_v])
      except:
        pass # value error
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabOptions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabOptions.grid()
    
  o_tab = Tab(tabOptions)
  root.mainloop()

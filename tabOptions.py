# Python 3
import tkinter as tk
from tkinter import ttk
import idlelib


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

    xPadding = 10
    tkFrame_Gearbox = tk.LabelFrame(parentFrame, text='Gearbox')
    tkFrame_Gearbox.grid(column=1, row=2, sticky='ew', padx=xPadding)

    self.RequireClutch = tk.StringVar()
    self.RequireClutch.set(False)
    tkCheckbutton_RequireClutch = tk.Checkbutton(tkFrame_Gearbox, 
                                                 text='Require clutch (Grinding Tranny)',
                                                 variable=self.RequireClutch
                                                 )
    self.AutoClutch = tk.StringVar()
    self.AutoClutch.set(True)
    tkCheckbutton_AutoClutch = tk.Checkbutton(tkFrame_Gearbox, 
                                              text='Auto clutch (std. rF2)',
                                              variable=self.AutoClutch)
    #tkCheckbutton_GearDamage = tk.Checkbutton(tkFrame_Gearbox, text='Gearbox damage')

    tkCheckbutton_RequireClutch.grid(sticky='w')
    tkCheckbutton_AutoClutch.grid(sticky='w')
    #tkCheckbutton_GearDamage.grid(sticky='w')

    tkFrame_Monitor = tk.LabelFrame(parentFrame, text='Monitor', padx=xPadding)
    tkFrame_Monitor.grid(column=1, row=3, sticky='ew')
    self.monitor = tk.StringVar()
    tkRadiobutton_Monitor = tk.Radiobutton(tkFrame_Monitor, 
                                           text='Monitor', 
                                           variable=self.monitor, 
                                           value='Monitor')
    tkRadiobutton_VR = tk.Radiobutton(tkFrame_Monitor, 
                                      text='VR', 
                                      variable=self.monitor, 
                                      value='VR')
    tkRadiobutton_Monitor.grid(sticky='w')
    tkRadiobutton_VR.grid(sticky='w')
    self.monitor.set('Monitor')
    tkRadiobutton_Monitor.update()

    tkFrame_AIstrength = tk.LabelFrame(parentFrame, text='AI', padx=xPadding)
    tkFrame_AIstrength.grid(column=1, row=4, sticky='ew')

    tkLabel_AIstrength = tk.Label(tkFrame_AIstrength, text='Overall AI strength\n(combined with car\nand track factors)')
    tkLabel_AIstrength.grid(column=1, row=1, sticky='e')
    tkScale_AIstrength = tk.Scale(tkFrame_AIstrength, from_=95, to=110, orient=tk.HORIZONTAL)
    tkScale_AIstrength.grid(column=2, row=1, sticky='ewns')

    tkLabel_AIaggression = tk.Label(tkFrame_AIstrength, text='AI aggression (std. rF2)')
    tkLabel_AIaggression.grid(column=1, row=2, sticky='e')
    tkScale_AIaggression = tk.Scale(tkFrame_AIstrength, from_=0, to=100, orient=tk.HORIZONTAL)
    tkScale_AIaggression.grid(column=2, row=2, sticky='ewns')

    tkLabel_AIlimiter = tk.Label(tkFrame_AIstrength, text='AI limiter (std. rF2)')
    tkLabel_AIlimiter.grid(column=1, row=3, sticky='e')
    tkScale_AIlimiter = tk.Scale(tkFrame_AIstrength, from_=0, to=100, orient=tk.HORIZONTAL)
    tkScale_AIlimiter.grid(column=2, row=3, sticky='ewns')

    tkFrame_Damage = tk.LabelFrame(parentFrame, text='Damage', padx=xPadding)
    tkFrame_Damage.grid(column=3, row=2, sticky='ew')

    tkCheckbutton_GearDamage = tk.Checkbutton(tkFrame_Damage, text='Gearbox damage (Grinding Tranny)')
    tkCheckbutton_MechanicalFailure = tk.Checkbutton(tkFrame_Damage, text='Mechanical Failure\n(should be\nOff/Normal/Time scaled)')
    tkCheckbutton_Invulnerability = tk.Checkbutton(tkFrame_Damage, text='Invulnerability (std. rF2)')

    tkCheckbutton_GearDamage.grid(sticky='w')
    tkCheckbutton_MechanicalFailure.grid(sticky='w')
    tkCheckbutton_Invulnerability.grid(sticky='w')

    tkFrame_RaceOptions = tk.LabelFrame(parentFrame, text='Race Options', padx=xPadding)
    tkFrame_RaceOptions.grid(column=3, row=3, sticky='ew')

    tkCheckbutton_RaceTime = tk.Checkbutton(tkFrame_RaceOptions, text='Race time (complicated...)')
    tkCheckbutton_Timescale = tk.Checkbutton(tkFrame_RaceOptions, text='Timescale (list of options)')
    tkCheckbutton_FinishCriteria = tk.Checkbutton(tkFrame_RaceOptions, text='FinishCriteria - laps/time and...')
    tkCheckbutton_Laps = tk.Checkbutton(tkFrame_RaceOptions, text='slider?')

    tkCheckbutton_RaceTime.grid(sticky='w')
    tkCheckbutton_Timescale.grid(sticky='w')
    tkCheckbutton_FinishCriteria.grid(sticky='w')
    tkCheckbutton_Laps.grid(sticky='w')

    tkFrame_Co_programs = tk.LabelFrame(parentFrame, text='Other programs to run with rF2', padx=xPadding)
    tkFrame_Co_programs.grid(column=3, row=4, sticky='ew')

    tkCheckbutton_CrewChief = tk.Checkbutton(tkFrame_Co_programs, text='Crew Chief')
    tkCheckbutton_TeamSpeak = tk.Checkbutton(tkFrame_Co_programs, text='TeamSpeak')
    tkCheckbutton_Discord = tk.Checkbutton(tkFrame_Co_programs, text='Discord (voice)')

    tkCheckbutton_CrewChief.grid(sticky='w')
    tkCheckbutton_TeamSpeak.grid(sticky='w')
    tkCheckbutton_Discord.grid(sticky='w')

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Options']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabOptions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabOptions.grid()
    
  o_tab = Tab(tabOptions)
  root.mainloop()

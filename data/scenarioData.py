"""
This handles reading and writing rFactory's Scenario files.
A Scenario captures all the settings in rFactory so the user
can switch from a wet daytime race with damage on using the clutch
in a classic F1 car against 10 classic F1 opponents in VR at the 
old Spa to a dry day/night race with no damage in an LMP1 against 
25 cars in mixed classes on a monitor at modern Le Mans.  
Graphics detail settings and driving controls are included.

Online / offline is also included. If online then the server can 
be joined automatically and other settings may differ.

rFactory can also invoke third party programs like TeamSpeak,
Crew Chief and its own Gearshift simulator.
"""

scenarioData = {
  'tabCar' : '',
  'tabConditions' : '',
  'tabOpponents' : '',
  'tabOptions' : '',
  'tabScenarios' : '',
  'tabServers' : '',
  'tabSessions' : '',
  'tabTrack' : '',
}
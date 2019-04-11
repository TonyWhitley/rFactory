# rFactory
A "Super UI" for rFactor 2 like AC's "Content Manager" but more so!

tl;dr  Most of it works but it has a number of rough edges.

See https://github.com/TonyWhitley/rFactory/blob/master/faq.txt for current status (also available in the program as Help/FAQ menu).

The concept is a GUI that allows you to tweak the major game settings in a similar way to Assetto Corsa's Content Manager.  Taking offline first: you'd select which car you want to drive, what and how many opponents and which circuit, all with the aid of filters.  You could then tweak the graphics settings if needed before saving the whole thing as a "scenario".  For online you'd do much the same (even though car, opponents and circuit are set by the server rFactoring still needs to know) and pick the server you're going to race on.

## Installing and first run
Any brave souls who want to try it out: download the rfactory.zip from the releases page https://github.com/TonyWhitley/rFactory/releases and unzip it into a new folder (referred to as <rfactory> from now on) and run rFactory.exe There will be a page scrolling away for many seconds as it makes its own data files from your rFactor installation (it only needs to do that once).

1st gotcha:  if your rFactor is not installed in the usual place then edit <rfactory>\Datafiles\favourites\rFactoryConfig.JSON and change this entry

`"rF2root": "%ProgramFiles(x86)%/Steam/steamapps/common/rFactor 2"`

The data is extracted from rFactor's data files and then run through my "AI" to make some sense of it but if you right-click an entry you can edit it.  (Warning: you can edit any of the values but it may not work afterwards if you edit the wrong one!)

## Offline
Pick the car and track you want. Use the filters at the top and sorting by clicking the column headings

## Options
The only Options that work are the `Other programs to run with rF2`
Again you can find the commands for the programs in `<rfactory>\Datafiles\favourites\rFactoryConfig.JSON`

Once you've set everything up then the menu `Scenarios/Save scenario as...` saves all the options so you can reload it later.  (Also rFactory saves all options in `<rfactory>\Datafiles\scenarioFiles\lastScenario.rFactoryScenarioJSON` every time you close it down and reloads them next time.)

## Online
Before it can connect online you need to edit `<rfactory>\Datafiles\favourites\favouriteServers.JSON`
```
{
"server": "password",
"RSVR sig-racing.boards.net": "<you know what to put here>",
"Some server that doesn't have a password": "",
"Another server that does": "PaSsWoRd"
}
```

Once everything is set click Run rFactor 2 and it all happens automatically: CrewChief and Discord start up (if you selected those options), it runs offline (using the car/track you selected) or connects straight to the server (no need to enter the password).



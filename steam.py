"""
Steam.exe utils: run it, minimise it, is it running?
"""
import os
import subprocess
import time
import win32con
import win32api
import win32gui

SteamExe = os.path.expandvars("%ProgramFiles(x86)%/Steam/steam.exe")
SteamDelayS = 10  # How long it takes Steam to start up


class Steam:
    def __init__(self):
        pass

    def getSteamWindow(self):
        toplist = []
        winlist = []

        def enum_callback(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_callback, toplist)
        steam = [(hwnd, title)
                 for hwnd, title in winlist if 'steam' in title.lower()]
        # just grab the first window that matches
        if len(steam):
            steam = steam[0]
        return steam

    def runIt(self, steamCmd, steamDelay=SteamDelayS):
        # Popen doesn't wait for completion (Steam closed)
        subprocess.Popen(steamCmd)
        time.sleep(steamDelay)

    def isItRunning(self):
        steam = self.getSteamWindow()
        if len(steam):
            # use the window handle to set focus
            try:
                win32gui.SetForegroundWindow(steam[0])
            except BaseException:  # error when 2nd monitor was turned off???
                pass
        return len(steam)

    def minimise(self):
        steam = self.getSteamWindow()
        if len(steam):
            win32gui.ShowWindow(steam[0], win32con.SW_MINIMIZE)


def runSteamMinimised(SteamExe=SteamExe, steamDelay=SteamDelayS):
    # Start it (if it's not running), wait then minimise it.
    _steam = Steam()
    if not _steam.isItRunning():
        _steam.runIt(SteamExe, steamDelay)

    while not _steam.isItRunning():
        time.sleep(1)

    _steam.minimise()


if __name__ == '__main__':
    _steam = Steam()
    if not _steam.isItRunning():
        _steam.runIt(SteamExe)

    while not _steam.isItRunning():
        time.sleep(1)

    _steam.minimise()
    pass

import pprint
from tkinter import messagebox

from edit.editRF2files import readCar, readTrack, readOpponents


def dummyRF2(online, settings, _password=None):
    """
    Function that accesses the same data files and dumps what rF2 would do with it
    """
    pp = "This is the result of the 'Dummy_rF2' checkbox on the Options tab which is used for debugging.\n\n"

    if online == 'Offline':
        pp += 'Car: %s\n' % readCar()
        pp += 'Track: %s\n' % readTrack()
        pp += 'Opponents: %s\n\n' % readOpponents()
    else:
        pp += 'Server: %s\n' % settings['Favourite Servers']
        if _password is not None:
            pp += 'Password: %s\n\n' % _password
        else:
            pp += 'No password\n\n'

    try:
        pp += pprint.pformat(settings, indent=2)
    except Exception as e:
        pp += 'Error formatting settings %s' % e

    messagebox.askokcancel('Settings', pp)
    # showinfo does an annoying bleep
    return 'OK'


if __name__ == '__main__':
    settings = {'one': 'setting'}
    dummyRF2(settings)

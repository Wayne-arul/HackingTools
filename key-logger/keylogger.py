from pynput.keyboard import *


def pressed(key):
    print(key)


def released(key):
    pass


with Listener(on_press=pressed, on_release=released) as l:
    l.join()

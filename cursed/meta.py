#!/usr/bin/env python
'''
cursed.meta

This contains the metaclass used to decorate all user classes that subclass
CursedWindow, crucial for the curses interface to work.
'''
from six.moves.queue import Queue

BASE_CURSED_CLASSES = ('CursedWindowClass', 'CursedWindow', 'CursedMenu')


class CursedWindowClass(type):

    WINDOWS = []

    def __new__(cls, name, parents, dct):
        new = super(CursedWindowClass, cls).__new__(cls, name, parents, dct)
        if name in BASE_CURSED_CLASSES:
            return new
        new.WIDTH = dct.get('WIDTH')
        new.HEIGHT = dct.get('HEIGHT')
        new.WINDOW = None
        new.APP = None
        new.X = dct.get('X', 0)
        new.Y = dct.get('Y', 0)
        new.BORDERED = dct.get('BORDERED', False)
        new.EVENTS = Queue()
        new.RESULTS = Queue()
        new.KEY_EVENTS = Queue()
        new.SCROLL = dct.get('SCROLL', False)
        new.WAIT = dct.get('WAIT', True)
        new.MENU = dct.get('MENU', None)
        new._MENU_MAP = {}
        new._OPENED_MENU = None
        new._SELECTED_ITEM = None
        cls.WINDOWS += [new]
        return new

    @classmethod
    def fix_windows(cls, maxw, maxh):
        '''
        Fixes all windows for which width or height is specified as 'max'.
        '''
        if not cls.WINDOWS:
            return
        for win in cls.WINDOWS:
            if win.WIDTH == 'max':
                win.WIDTH = maxw - win.X
            if win.HEIGHT == 'max':
                win.HEIGHT = maxh - win.Y

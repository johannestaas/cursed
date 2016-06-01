#!/usr/bin/env python
'''
cursed.meta

This contains the metaclass used to decorate all user classes that subclass
CursedWindow, crucial for the curses interface to work.
'''
from six.moves.queue import Queue
from .exceptions import CursedPadError, CursedWindowError

BASE_CURSED_CLASSES = ('CursedWindowClass', 'CursedWindow', 'CursedMenu')


class CursedWindowClass(type):
    '''
    The CursedWindow has this as a metaclass, to keep track of all classes
    that inherit from it so that the app can instanciate the correct windows.
    '''

    WINDOWS = []

    def __new__(cls, name, parents, dct):
        new = super(CursedWindowClass, cls).__new__(cls, name, parents, dct)
        if name in BASE_CURSED_CLASSES:
            return new
        new.X = dct.get('X', 0)
        new.Y = dct.get('Y', 0)
        new.WIDTH = dct.get('WIDTH')
        new.HEIGHT = dct.get('HEIGHT')
        if new.WIDTH is None or new.HEIGHT is None:
            raise CursedWindowError('specify WIDTH and HEIGHT for {name}, '
                                    'either as "max" or a positive integer'
                                    .format(name=name))
        new.PAD = dct.get('PAD', False)
        new.PAD_WIDTH = dct.get('PAD_WIDTH')
        new.PAD_HEIGHT = dct.get('PAD_HEIGHT')
        new.PAD_X = dct.get('PAD_X', 0)
        new.PAD_Y = dct.get('PAD_Y', 0)
        new.BORDERED = dct.get('BORDERED', False)
        if new.PAD and (new.PAD_WIDTH is None or new.PAD_HEIGHT is None):
            raise CursedPadError('specify PAD_WIDTH and PAD_HEIGHT for {name}'
                                 .format(name=name))
        if new.PAD and new.BORDERED:
            raise CursedPadError('{name} cant be both a PAD and BORDERED'
                                 .format(name=name))
        new.SCROLL = dct.get('SCROLL', False)
        if new.PAD and new.SCROLL:
            raise CursedPadError('{name} cant be both a PAD and SCROLL'
                                 .format(name=name))
        new.WINDOW = None
        new.APP = None
        new.EVENTS = Queue()
        new.RESULTS = Queue()
        new.KEY_EVENTS = Queue()
        new.WAIT = dct.get('WAIT', True)
        new.MENU = dct.get('MENU', None)
        new._MENU_MAP = {}
        new._OPENED_MENU = None
        new._SELECTED_ITEM = None
        cls.WINDOWS += [new]
        return new

    @classmethod
    def _fix_windows(cls, maxw, maxh):
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

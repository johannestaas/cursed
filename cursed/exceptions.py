#!/usr/bin/env python
'''
cursed.exceptions

Base exceptions used by cursed.
'''


class CursedSizeError(RuntimeError):
    '''
    Raised when a terminal size issue occurs, such as the menu not fitting in
    the width of the screen, or writing text outside of the window.
    '''
    pass


class CursedCallbackError(RuntimeError):
    '''
    Raised when a callback issue occurs, such as triggering a callback that
    doesn't exist, example:
    ::

        cls.trigger('typo_in_nmae')
    '''
    pass


class CursedMenuError(RuntimeError):
    '''
    Raised when menus aren't initialized correctly.
    Check in the CursedMenu documentation or the example projects for examples
    of proper creation of menus.
    '''
    pass

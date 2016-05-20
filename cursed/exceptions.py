#!/usr/bin/env python
'''
cursed.exceptions

Base exceptions used by cursed.
'''


class CursedSizeError(RuntimeError):
    pass


class CursedCallbackError(RuntimeError):
    pass


class CursedMenuError(RuntimeError):
    pass

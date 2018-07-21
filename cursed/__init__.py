'''
cursed

Simplified curses interface with concurrency, for quick and sane curses apps.
Allows easy creation of windows and menus. Code for each window runs concurrently.

'''
from cursed.app import CursedApp
from cursed.window import CursedWindow
from cursed.menu import CursedMenu

__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__title__ = 'cursed'
__version__ = '0.2.1'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2016 Johan Nestaas'
__all__ = ['CursedApp', 'CursedWindow', 'CursedMenu']

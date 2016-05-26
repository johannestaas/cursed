#!/usr/bin/env python
'''
cursed.menu

The menu data class.
Most of the menu implementation is actually in the cursed.window module.
'''

from cursed.exceptions import CursedMenuError


class CursedMenu(object):

    def __init__(self):
        self.menus = []
        self.counts = {}
        self.callbacks = {}

    def add_menu(self, title, key=None):
        title = title.strip()
        if not title:
            raise CursedMenuError('Menu must have a name.')
        if key is None:
            key = title[0].lower()
        self.menus += [
            (key, title, [])
        ]
        self.counts[title] = 0
        self.callbacks[title] = []

    def add_items(self, *args):
        if not self.menus:
            raise CursedMenuError('Must add_menu before adding items.')
        mkey, mtitle, menu = self.menus[-1]
        for arg in args:
            if len(arg) == 2:
                name, cb = arg
                key = None
            elif len(arg) == 3:
                name, key, cb = arg
            else:
                raise CursedMenuError('Format for menu item must be (Title, '
                                      'key, function name)')
            name = name.strip()
            if not name:
                raise CursedMenuError('Menu item must have a name.')
            menu += [(name, key, cb)]
            self.callbacks[mtitle] += [cb]
        self.menus[-1] = mkey, mtitle, menu
        self.counts[mtitle] = len(menu)

#!/usr/bin/env python
'''
cursed.menu

The menu data class.
Most of the menu implementation is actually in the cursed.window module.
'''

from cursed.exceptions import CursedMenuError


class CursedMenu(object):
    '''
    The CursedMenu is the class which is used to initialize all the menus and
    items.
    '''

    def __init__(self):
        self.menus = []

    def add_menu(self, title, key=None, items=None):
        '''
        This creates a full menu with a title, an optional hotkey, and a list
        of items inside the menu, with their name, hotkey and callback.

        Example:
        ::

            MENU = CursedMenu('File', key='f', items=[
                ('Save', 's', 'save_callback'),
                ('Open', 'open_callback'),
                ('Quit', 'q', 'quit'),
            ])
        '''
        title = title.strip()
        if not title:
            raise CursedMenuError('Menu must have a name.')
        menu = _Menu(title=title, key=key, items=[])
        if not items:
            raise CursedMenuError('Menu must define items inside it.')
        menu.add_items(items)


class _OpenMenu(object):

    def __init__(self, index=None, title=None, cb_map=None):
        self.index = index
        self.title = title
        self.cb_map = cb_map


class _MenuItem(object):

    def __init__(self, name=None, key=None, cb=None):
        self.name = name
        self.key = key
        self.cb = cb

    def __str__(self):
        if self.key:
            return '[{0}] {1}'.format(self.key, self.name)
        return self.name


class _Menu(object):
    ALL = []
    KEY_MAP = {}
    TITLE_MAP = {}

    def __init__(self, title=None, key=None, items=None):
        self.title = title
        self.key = key
        self.items = []
        self.item_map = {}
        self.index = len(_Menu.ALL)
        self.selected = None
        _Menu.ALL += [self]
        _Menu.TITLE_MAP[title] = self
        if key is not None:
            _Menu.KEY_MAP[key] = self

    @classmethod
    def clear_select(cls):
        for menu in cls.ALL:
            menu.selected = None

    def add_item(self, menu_item):
        self.items += [menu_item]
        self.item_map[menu_item.key] = menu_item

    def add_items(self, args):
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
            self.add_item(_MenuItem(name=name, key=key, cb=cb))

    def get_cb(self, key):
        if key in self.item_map:
            return self.item_map[key].cb
        return None

    @classmethod
    def get_menu_from_key(cls, key):
        return _Menu.KEY_MAP.get(key)

    @classmethod
    def get_menu_at(cls, i):
        if i >= len(_Menu.ALL):
            return None
        return _Menu.ALL[i]

    @classmethod
    def get_menu_from_title(cls, title):
        return _Menu.TITLE_MAP.get(title)

    @classmethod
    def size(cls):
        return len(_Menu.ALL)

    def down(self):
        if self.selected is None:
            self.selected = self.items[0]
        else:
            i = self.items.index(self.selected)
            i += 1
            if i == len(self.items):
                i = 0
            self.selected = self.items[i]

    def up(self):
        if self.selected is None:
            self.selected = self.items[-1]
        else:
            i = self.items.index(self.selected)
            i -= 1
            if i == -1:
                i = len(self.items) - 1
            self.selected = self.items[i]

    @classmethod
    def right(cls, menu):
        if menu is None:
            return None
        i = cls.ALL.index(menu)
        i += 1
        if i == len(cls.ALL):
            return cls.ALL[0]
        return cls.ALL[i]

    @classmethod
    def left(cls, menu):
        if menu is None:
            return None
        i = cls.ALL.index(menu)
        i -= 1
        if i == -1:
            return cls.ALL[-1]
        return cls.ALL[i]

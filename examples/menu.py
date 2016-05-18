#!/usr/bin/env python
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class MainWindow(CursedWindow):
    HEIGHT = 22
    # SCROLL = True

    MENU = CursedMenu()
    MENU.add_menu('File', 'f')
    MENU.add_items(
        ('Save', 's', 'save'),
        ('Quit', 'q', 'quit'),
    )
    MENU.add_menu('Edit', 'e')
    MENU.add_items(
        ('Copy', 'c', 'copy'),
        ('Paste', 'v', 'paste'),
        ('Delete', 'delete')
    )

    @classmethod
    def save(cls):
        cls.addstr('File->Save')

    @classmethod
    def quit(cls):
        cls.addstr('Quitting')

    @classmethod
    def copy(cls):
        cls.addstr('edit->copy')

    @classmethod
    def paste(cls):
        cls.addstr('edit->paste')

    @classmethod
    def delete(cls):
        cls.addstr('edit->delete')

    @classmethod
    def update(cls):
        cls.cx = 10
        cls.cy = 10


class FooterWindow(CursedWindow):
    HEIGHT = 1
    Y = 23

    @classmethod
    def init(cls):
        cls.addstr('Press f then q to exit')
        cls.refresh()
        cls.trigger('quit')


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

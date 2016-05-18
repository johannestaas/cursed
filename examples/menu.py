#!/usr/bin/env python
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class MainWindow(CursedWindow):
    WIDTH = 100
    HEIGHT = 23

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
        cls.addstr('File->Save', 5, 5)

    @classmethod
    def quit(cls):
        cls.addstr('Quitting', 5, 5)

    @classmethod
    def copy(cls):
        cls.addstr('edit->copy', 5, 5)

    @classmethod
    def paste(cls):
        cls.addstr('edit->paste', 5, 5)

    @classmethod
    def delete(cls):
        cls.addstr('edit->delete', 5, 5)

    @classmethod
    def update(cls):
        cls.addstr('x=10, y=12', 10, 12)


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

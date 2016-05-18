#!/usr/bin/env python
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class MainWindow(CursedWindow):
    HEIGHT = 22
    SCROLL = True
    i = 0

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
        MainWindow.write('File->Save')

    @classmethod
    def quit(cls):
        MainWindow.write('Quitting')

    @classmethod
    def copy(cls):
        MainWindow.write('edit->copy')

    @classmethod
    def paste(cls):
        MainWindow.write('edit->paste')

    @classmethod
    def delete(cls):
        MainWindow.write('edit->delete')


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

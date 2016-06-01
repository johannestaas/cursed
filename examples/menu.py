#!/usr/bin/env python
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class MainWindow(CursedWindow):
    X, Y = (0, 0)
    WIDTH, HEIGHT = 'max', 23

    MENU = CursedMenu()
    MENU.add_menu('File', key='f', items=[
        ('Save', 's', 'save'),
        ('Quit', 'q', 'quit'),
    ])
    MENU.add_menu('Edit', key='e', items=[
        ('Copy', 'c', 'copy'),
        ('Paste', 'v', 'paste'),
        ('Delete', 'delete')
    ])

    @classmethod
    def save(cls):
        cls.addstr('File->Save', 0, 7)

    @classmethod
    def quit(cls):
        cls.addstr('Quitting', 0, 7)

    @classmethod
    def copy(cls):
        cls.addstr('edit->copy', 0, 7)

    @classmethod
    def paste(cls):
        cls.addstr('edit->paste', 0, 7)

    @classmethod
    def delete(cls):
        cls.addstr('edit->delete', 0, 7)

    @classmethod
    def update(cls):
        cls.addstr('x=10, y=12', 10, 12)
        # Press spacebar to open menu
        cls.addstr('Constantly updating with addstr ', 2, 2)
        cls.nextline()
        cls.addstr('overwrites the menu.', 2, 3)
        cls.addstr('The "Edit" menu should have "Delete"', 2, 4)
        cls.addstr('as the third menu item.', 2, 5)
        k = cls.getch()
        if k == 32:
            cls.openmenu()


class FooterWindow(CursedWindow):
    X, Y = (0, 23)
    WIDTH, HEIGHT = 'max', 1

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

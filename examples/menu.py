#!/usr/bin/env python
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class Menu(CursedMenu):
    ITEMS = (
        ('f', 'file'),
        ('e', 'edit'),
        ('q', 'quitit'),
    )

    @classmethod
    def file(cls):
        MainWindow.write('Pressed f for file!')

    @classmethod
    def edit(cls):
        MainWindow.write('Pressed e for edit!')

    @classmethod
    def quitit(cls):
        cls.trigger('quit')
        MainWindow.trigger('quit')


class MainWindow(CursedWindow):
    Y = 1
    HEIGHT = 22
    SCROLL = True
    i = 0

    @classmethod
    def update(cls):
        c = cls.getch()
        if c == 27:
            cls.trigger('quit')
            return
        cls.refresh()


class FooterWindow(CursedWindow):
    HEIGHT = 1
    Y = 23

    @classmethod
    def init(cls):
        cls.addstr('Press ESCAPE to exit')
        cls.refresh()
        cls.trigger('quit')


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
    if result.threads is not None:
        print('Threads: %s' % ' || '.join(str(x) for x in result.threads))
else:
    result.unwrap()

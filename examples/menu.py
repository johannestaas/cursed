#!/usr/bin/env python
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class Menu(CursedMenu):
    # Tuple of menus
    # First tuple is a 2-tuple of (letter, name) of the menu
    # Next few is 3-tuple of (letter, name, function_name)
    ITEMS = (
        (
            ('f', 'File'),
            ('s', 'Save', 'save'),
            ('q', 'Quit', 'quit'),
        ),
        (
            ('e', 'Edit'),
            ('c', 'Copy', 'copy'),
            ('p', 'Paste', 'paste'),
        ),
        (
            ('t', 'Test'),
            ('T', 'Test2', 'test2'),
            ('3', 'Three', 'three'),
        ),
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
    def test2(cls):
        MainWindow.write('test->test2')

    @classmethod
    def three(cls):
        MainWindow.write('test->three')


class MainWindow(CursedWindow):
    Y = 1
    HEIGHT = 22
    SCROLL = True
    i = 0


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
    if result.threads is not None:
        print('Threads: %s' % ' || '.join(str(x) for x in result.threads))
else:
    result.unwrap()

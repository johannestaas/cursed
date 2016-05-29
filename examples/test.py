#!/usr/bin/env python
from cursed import CursedApp, CursedWindow

app = CursedApp()


class MainWindow(CursedWindow):
    X, Y = (0, 0)
    WIDTH = 60
    HEIGHT = 'max'
    BORDERED = True

    @classmethod
    def update(cls):
        c = cls.getkey()
        if c is None:
            return
        if c == 'q':
            cls.trigger('quit')
            return
        cls.addstr(c * 10, x=0, y=0, attr='reverse')
        cls.nextline()
        cls.hline(n=10)
        cls.refresh()


class SideWindow(CursedWindow):
    X, Y = (60, 0)
    WIDTH = 20
    HEIGHT = 'max'
    BORDERED = True

    @classmethod
    def init(cls):
        cls.addstr('foo', 0, 0)
        cls.addstr('bar', x=0, y=1, attr='bold')
        w, h = cls.getwh()
        cls.nextline()
        cls.addstr(str(w))
        cls.refresh()

    @classmethod
    def update(cls):
        c = cls.getkey()
        if c is None:
            return
        if c == 'q':
            cls.trigger('quit')


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

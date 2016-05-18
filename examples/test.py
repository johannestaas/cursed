#!/usr/bin/env python
from cursed import CursedApp, CursedWindow

app = CursedApp()


class MainWindow(CursedWindow):
    WIDTH = 60
    BORDERED = True

    @classmethod
    def update(cls):
        c = cls.getlkey()
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
    WIDTH = 20
    X = 60
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
        c = cls.getlkey()
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

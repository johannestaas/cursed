#!/usr/bin/env python
from cursed import CursedApp, CursedWindow

app = CursedApp()


class MainWindow(CursedWindow):
    WIDTH = 60
    BORDERED = True

    @classmethod
    def update(cls):
        c = cls.getlchar()
        if c is None:
            return
        if c == 'q':
            cls.new_event('quit')
            return
        cls.addstr(c * 10, x=0, y=0)
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
        cls.addstr('bar', x=0, y=1)
        w, h = cls.getwh()
        cls.nextline()
        cls.addstr(str(w))
        cls.refresh()

    @classmethod
    def update(cls):
        c = cls.getlchar()
        if c is None:
            return
        if c == 'q':
            cls.new_event('quit')


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

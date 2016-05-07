#!/usr/bin/env python
from cursed import CursedApp, CursedWindow

app = CursedApp()


class MainWindow(CursedWindow):
    WIDTH = 60
    BORDERED = True
    ACTIVE = True

    @classmethod
    def run(cls):
        c = cls.getkey()
        if c.lower() == 'q':
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
    def run(cls):
        cls.addstr('foo', 0, 0)
        cls.addstr('bar', x=0, y=1)
        w, h = cls.getwh()
        cls.nextline()
        cls.addstr(str(w))
        cls.refresh()
        c = cls.getkey()
        if c.lower() == 'q':
            cls.new_event('quit')


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

#!/usr/bin/env python
from cursed import CursedApp, CursedWindow

app = CursedApp()


class MainWindow(CursedWindow):
    WIDTH = 60
    BORDERED = True

    @classmethod
    def run(cls):
        cls.c = cls.getkey()
        cls.addstr(cls.c * 10, x=0, y=0)
        cls.nextline()
        cls.hline(n=10)
        cls.refresh()
        return cls.c


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
        return cls.getkey()


def loop():
    while True:
        char = MainWindow.run()
        if char.lower() in 'q':
            break
    MainWindow.clear()
    MainWindow.refresh()
    while True:
        char = SideWindow.run()
        if char.lower() in 'q':
            break
    MainWindow.clear()

result = app.run(loop)
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

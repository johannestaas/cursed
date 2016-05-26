#!/usr/bin/env python
from cursed import CursedApp, CursedWindow

app = CursedApp()


class MainWindow(CursedWindow):
    WIDTH = 8
    HEIGHT = 4
    BORDERED = True

    @classmethod
    def update(cls):
        k = cls.getch()
        if k is None:
            return
        cls.addstr('{:6}'.format(k), x=0, y=0)
        cls.addstr('0x{:04x}'.format(k), x=0, y=1)
        cls.refresh()


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

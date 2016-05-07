#!/usr/bin/env python
from cursed import CursedApp, CursedWindow
app = CursedApp()


class ScrollingWindow(CursedWindow):
    HEIGHT = 24
    SCROLL = True
    i = 0

    @classmethod
    def update(cls):
        c = cls.getch()
        if c == 27:
            cls.trigger('quit')
            return
        cls.write(cls.i)
        cls.i += 1
        cls.refresh()


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

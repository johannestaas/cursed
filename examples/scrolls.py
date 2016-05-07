#!/usr/bin/env python
from cursed import CursedApp, CursedWindow
app = CursedApp()


class ScrollingWindow(CursedWindow):
    HEIGHT = 23
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

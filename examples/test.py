#!/usr/bin/env python
from cursed import CursedApp

app = CursedApp()


@app.window(width=60, bordered=True)
class MainWindow(object):

    def run(self):
        self.c = self.getkey()
        self.addstr(self.c * 10, x=1, y=1)
        self.cx = 1
        self.cy = self.cy + 1
        self.hline(n=10)
        self.refresh()
        return self.c


@app.window(width=20, x=60, bordered=True)
class SideWindow(object):

    def run(self):
        self.addstr('foo', 1, 1)
        self.addstr('bar', x=1, y=2)
        w, h = self.getwh()
        self.addstr(str(w), 1, 3)
        self.refresh()
        return self.getkey()


def loop():
    window = MainWindow()
    side = SideWindow()
    while True:
        char = window.run()
        if char.lower() in 'q':
            break
    window.clear()
    window.refresh()
    while True:
        char = side.run()
        if char.lower() in 'q':
            break
    window.clear()

result = app.run(loop)
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

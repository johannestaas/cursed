#!/usr/bin/env python
from cursed import CursedApp

app = CursedApp()


@app.window(width=60, bordered=True)
class MainWindow(object):

    def run(self):
        self.c = self.getkey()
        for i in range(10):
            self.addch(i + 1, 1, self.c)
        self.cx = 1
        self.cy = self.cy + 1
        self.hline(n=10)
        self.refresh()
        return self.c


@app.window(width=20, x=60, bordered=True)
class SideWindow(object):

    def run(self):
        self.addstr(1, 1, 'foo')
        self.addstr(1, 2, 'bar')
        w, h = self.getwh()
        self.addstr(1, 3, str(w))
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

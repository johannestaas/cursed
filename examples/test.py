#!/usr/bin/env python
from cursed import CursedApp

app = CursedApp()


@app.window
class MainWindow(object):

    def run(self):
        self.c = self.getch()
        for i in range(10):
            self.addch(i, 0, self.c)
        self.refresh()


def loop():
    window = MainWindow()
    while True:
        window.run()


result = app.run(loop)
result.unwrap()
if result.interrupt:
    print('Ctrl-C pressed.')

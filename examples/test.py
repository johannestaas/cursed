#!/usr/bin/env python
from cursed import CursedApp

app = CursedApp()


@app.window
class MainWindow(object):

    def run(self):
        self.c = self.getch()
        if self.c in (ord('q'), ord('Q')):
            return False
        if self.c in (ord('e'), ord('E')):
            raise RuntimeError('example error')
        for i in range(10):
            self.addch(i, 0, self.c)
        self.refresh()
        return True


def loop():
    window = MainWindow()
    while window.run():
        pass


result = app.run(loop)
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

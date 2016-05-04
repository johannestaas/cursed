#!/usr/bin/env python
from cursed import CursedApp

app = CursedApp()


@app.window(width=60)
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


@app.window(width=20, x=60)
class SideWindow(object):

    def run(self):
        self.addstr(0, 0, 'foo')
        self.addstr(0, 1, 'bar')
        self.refresh()
        self.c = self.getch()
        return self.c not in (ord('q'), ord('Q'))


def loop():
    window = MainWindow()
    side = SideWindow()
    while window.run():
        pass
    while side.run():
        pass
    window.clear()

result = app.run(loop)
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

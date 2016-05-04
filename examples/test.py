#!/usr/bin/env python
from cursed import CursedApp

app = CursedApp()


@app.window(width=60, bordered=True)
class MainWindow(object):

    def run(self):
        self.c = self.getkey()
        if self.c.lower() == 'q':
            return False
        if self.c.lower() == 'e':
            raise RuntimeError('example error')
        for i in range(10):
            self.addch(i + 1, 1, self.c)
        self.hline(1, 2, '-', 10)
        self.refresh()
        return True


@app.window(width=20, x=60, bordered=True)
class SideWindow(object):

    def run(self):
        self.addstr(1, 1, 'foo')
        self.addstr(1, 2, 'bar')
        w, h = self.get_wh()
        self.addstr(1, 3, str(w))
        self.refresh()
        self.c = self.getkey()
        return self.c.lower() != 'q'


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

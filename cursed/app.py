#!/usr/bin/env python
import traceback
import curses


class CursedWindow(object):

    def __init__(self, cls, width=80, height=24, x=0, y=0):
        self.cls = cls
        self.window = None
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.fix_class(cls)

    def run(self, window):
        self.window = window.subwin(self.height, self.width, self.y, self.x)

    def addch(self, x, y, c):
        return self.window.addch(y, x, c)

    def getch(self):
        return self.window.getch()

    def fix_class(self):
        self.cls.addch = self.addch
        self.cls.getch = self.getch


class CursedApp(object):

    def __init__(self):
        self.scr = None
        self.menu = None
        self.windows = {}

    def window(self, *args, **kwargs):
        def decorator(cls):
            self.windows[cls] = CursedWindow(cls, **kwargs)
            return cls
        if len(args) == 1:
            return decorator(args[0])
        else:
            return decorator

    def run_windows(self):
        for cls, cw in self.windows.items():
            cw.run(self.window)

    def run(self, loop_func, *args, **kwargs):
        try:
            self.scr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.window = self.scr.subwin(0, 0)
            self.window.keypad(1)
            self.run_windows()
            loop_func(*args, **kwargs)
        except Exception:
            traceback.print_exc()
        finally:
            if self.scr is not None:
                self.scr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

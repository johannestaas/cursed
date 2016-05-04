#!/usr/bin/env python
import sys
import traceback
import curses


class CursedWindow(object):

    def __init__(self, app, cls, width=80, height=24, x=0, y=0):
        self.app = app
        self.cls = cls
        self.window = None
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.fix_class()

    def run(self, window):
        self.window = window.subwin(self.height, self.width, self.y, self.x)

    def addch(self, x, y, c):
        return self.window.addch(y, x, c)

    def getch(self):
        return self.app.getch()

    def refresh(self):
        self.window.refresh()

    def fix_class(self):
        for attr in ('addch', 'getch', 'refresh'):
            setattr(self.cls, attr, getattr(self, attr))


class Result(object):

    def __init__(self):
        self.interrupt = False
        self.tb = None
        self.exception = None

    def unwrap(self, reraise=True):
        self.print_tb()
        if self.exception and reraise:
            raise self.exception

    def ok(self):
        return not any(self.tb, self.exception, self.interrupt)

    def err(self):
        if self.ok():
            return None
        if self.exception:
            return self.exception
        if self.interrupt:
            return KeyboardInterrupt

    def print_tb(self):
        if self.tb:
            sys.stderr.write(self.tb)


class CursedApp(object):

    def __init__(self):
        self.scr = None
        self.menu = None
        self.windows = {}

    def window(self, *args, **kwargs):
        def decorator(cls):
            self.windows[cls] = CursedWindow(self, cls, **kwargs)
            return cls
        if len(args) == 1:
            return decorator(args[0])
        else:
            return decorator

    def getch(self):
        return self.scr.getch()

    def run_windows(self):
        for cls, cw in self.windows.items():
            cw.run(self.window)

    def run(self, loop_func, *args, **kwargs):
        result = Result()
        try:
            self.scr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.window = self.scr.subwin(0, 0)
            self.window.keypad(1)
            self.run_windows()
            loop_func(*args, **kwargs)
        except KeyboardInterrupt:
            result.interrupt = True
        except Exception as e:
            result.tb = traceback.format_exc()
            result.exception = e
        finally:
            if self.scr is not None:
                self.scr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        return result

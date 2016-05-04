#!/usr/bin/env python
import sys
import curses


class CursedWindow(object):

    OVERRIDE_FUNCS = (
        'addch', 'get_wh',
    )
    WINDOW_SWAP_FUNCS = (
        'delch', 'addnstr', 'addstr',
    )
    SCREEN_SWAP_FUNCS = (
    )
    WINDOW_FUNCS = (
        'refresh', 'clear', 'deleteln', 'erase',
    )
    SCREEN_FUNCS = (
        'getch', 'getkey',
    )

    def __init__(self, app, cls, width=80, height=24, x=0, y=0):
        self.app = app
        self.cls = cls
        self.window = None
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def addch(self, x, y, c, *args):
        if isinstance(c, int):
            c = chr(c)
        return self.window.addch(y, x, c, *args)

    def get_wh(self):
        h, w = self.window.getmaxyx()
        return w, h

    def run(self, window):
        self.window = window.subwin(self.height, self.width, self.y, self.x)
        for attr in self.OVERRIDE_FUNCS:
            setattr(self.cls, attr, getattr(self, attr))
        for attr in self.WINDOW_FUNCS:
            setattr(self.cls, attr, getattr(self.window, attr))
        for attr in self.SCREEN_FUNCS:
            setattr(self.cls, attr, getattr(self.app.scr, attr))
        for attr in self.WINDOW_SWAP_FUNCS:
            window_func = getattr(self.window, attr)

            def new_func(s, x, y, *args, **kwargs):
                return window_func(y, x, *args, **kwargs)
            setattr(self.cls, attr, new_func)
        for attr in self.SCREEN_SWAP_FUNCS:
            scr_func = getattr(self.app.scr, attr)

            def new_func(s, x, y, *args, **kwargs):
                return scr_func(y, x, *args, **kwargs)
            setattr(self.cls, attr, new_func)


class Result(object):

    def __init__(self):
        self.exc_type, self.exc, self.tb = None, None, None

    def _extract_exception(self):
        self.exc_type, self.exc, self.tb = sys.exc_info()

    def unwrap(self):
        if self.exc:
            raise self.exc_type, self.exc, self.tb

    def ok(self):
        return not bool(self.exc)

    def err(self):
        return self.exc if self.exc else None

    def interrupted(self):
        return self.exc_type is KeyboardInterrupt

    def print_exc(self):
        if self.tb:
            sys.stderr.write(self.tb)

    def __repr__(self):
        if self.exc_type is None:
            return 'Result(OKAY)'
        if self.interrupted():
            return 'Result(KeyboardInterrupt)'
        return 'Result(%s, message=%s)' % (self.exc_type.__name__,
                                           str(self.exc))


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
            result._extract_exception()
        except Exception:
            result._extract_exception()
        finally:
            if self.scr is not None:
                self.scr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
        return result

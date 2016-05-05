#!/usr/bin/env python
import sys
import curses


class CursedWindow(object):

    OVERRIDE_FUNCS = (
        'addch', 'addstr', 'addnstr', 'getwh', 'getstr', 'getxy', 'hline',
        'vline', 'nextline', 'delch', 'instr', 'insstr', 'insnstr', 'inch',
        'insch',
    )
    WINDOW_SWAP_FUNCS = (
        'mvwin', 'move',
    )
    SCREEN_SWAP_FUNCS = (
    )
    WINDOW_FUNCS = (
        'refresh', 'clear', 'deleteln', 'erase', 'insertln', 'border',
        'nodelay', 'notimeout', 'clearok', 'is_linetouched', 'is_wintouched',
    )
    SCREEN_FUNCS = (
        'getch', 'getkey',
    )

    def __init__(self, app, cls, width=80, height=24, x=0, y=0, bordered=False,
                 border_shift=True):
        self.app = app
        self.cls = cls
        self.window = None
        self.width = width
        self.height = height
        self._x = x
        self._y = y
        self.bordered = bordered
        self.border_shift = border_shift

    def addch(self, c, x=None, y=None, attr=None):
        x, y = self.fix_xy(x, y)
        if isinstance(c, int):
            c = chr(c)
        if attr is None:
            return self.window.addch(y, x, c)
        else:
            return self.window.addch(y, x, c, attr)

    def delch(self, x=None, y=None):
        x, y = self.fix_xy(x, y)
        return self.window.delch(y, x)

    def getwh(self):
        h, w = self.window.getmaxyx()
        return w, h

    def getxy(self):
        y, x = self.window.getyx()
        if self.border_shift:
            return x - 1, y - 1
        return x, y

    def inch(self, x=None, y=None):
        x, y = self.fix_xy(x, y)
        return self.window.inch(y, x)

    def insch(self, ch, x=None, y=None, attr=None):
        x, y = self.fix_xy(x, y)
        if attr is None:
            return self.window.insch(y, x, ch)
        else:
            return self.window.insch(y, x, ch, attr)

    def instr(self, x=None, y=None, n=None):
        x, y = self.fix_xy(x, y)
        if n is None:
            return self.window.instr(y, x)
        else:
            return self.window.instr(y, x, n)

    def insstr(self, s, x=None, y=None, attr=None):
        x, y = self.fix_xy(x, y)
        if attr is None:
            return self.window.insstr(y, x, s)
        else:
            return self.window.insstr(y, x, s, attr)

    def insnstr(self, s, x=None, y=None, n=None, attr=None):
        x, y = self.fix_xy(x, y)
        n = n if n is not None else self.width
        if attr is None:
            return self.window.insnstr(y, x, s, n)
        else:
            return self.window.insnstr(y, x, s, n, attr)

    def nextline(self, cr=True):
        x, y = self.getxy()
        if cr:
            x = 0
        x, y = self.fix_xy(x, y)
        self.window.move(y + 1, x)

    def fix_xy(self, x, y):
        if x is None or y is None:
            x0, y0 = self.getxy()
            x = x0 if x is None else x
            y = y0 if y is None else y
        if self.border_shift:
            return x + 1, y + 1
        return x, y

    def addstr(self, s, x=None, y=None, attr=None):
        x, y = self.fix_xy(x, y)
        if attr is None:
            return self.window.addstr(y, x, s)
        else:
            return self.window.addstr(y, x, s, attr)

    def addnstr(self, s, x=None, y=None, n=None, attr=None):
        x, y = self.fix_xy(x, y)
        n = self.width if n is None else n
        if attr is None:
            return self.window.addnstr(y, x, s, n)
        else:
            return self.window.addnstr(y, x, s, n, attr)

    def getstr(self, *args):
        if args:
            x, y = self.fix_xy(*args)
            return self.window.getstr(x, y)
        return self.window.getstr()

    def hline(self, x=None, y=None, char='-', n=None):
        x, y = self.fix_xy(x, y)
        n = self.width if n is None else n
        return self.window.hline(y, x, char, n)

    def vline(self, x=None, y=None, char='|', n=None):
        x, y = self.fix_xy(x, y)
        n = self.height if n is None else n
        return self.window.vline(y, x, char, n)

    def set_window_func(self, attr):
        setattr(self.cls, attr, getattr(self.window, attr))

    def set_screen_func(self, attr):
        setattr(self.cls, attr, getattr(self.app.scr, attr))

    def swap_window_func(self, attr):
        func = getattr(self.window, attr)

        def new_func(s, x, y, *args, **kwargs):
            x, y = self.fix_xy(x, y)
            return func(y, x, *args, **kwargs)
        setattr(self.cls, attr, new_func)

    def swap_screen_func(self, attr):
        func = getattr(self.app.scr, attr)

        def new_func(s, x, y, *args, **kwargs):
            x, y = self.fix_xy(x, y)
            return func(y, x, *args, **kwargs)
        setattr(self.cls, attr, new_func)

    def getter_cx(self):
        def get_cx(s):
            x, y = self.getxy()
            x, y = self.fix_xy(x, y)
            return x
        return get_cx

    def getter_cy(self):
        def get_cy(s):
            x, y = self.getxy()
            x, y = self.fix_xy(x, y)
            return y
        return get_cy

    def setter_cx(self):
        def set_cx(s, v):
            x, y = self.getxy()
            x, y = self.fix_xy(x, y)
            s.move(v, y)
        return set_cx

    def setter_cy(self):
        def set_cy(s, v):
            x, y = self.getxy()
            x, y = self.fix_xy(x, y)
            s.move(x, v)
        return set_cy

    def run(self, window):
        self.window = window.subwin(self.height, self.width, self._y, self._x)
        if self.bordered:
            self.window.border()
        for attr in self.OVERRIDE_FUNCS:
            setattr(self.cls, attr, getattr(self, attr))
        for attr in self.WINDOW_FUNCS:
            self.set_window_func(attr)
        for attr in self.SCREEN_FUNCS:
            self.set_screen_func(attr)
        for attr in self.WINDOW_SWAP_FUNCS:
            self.swap_window_func(attr)
        for attr in self.SCREEN_SWAP_FUNCS:
            self.swap_screen_func(attr)
        self.cls.cx = property(self.getter_cx(), self.setter_cx())
        self.cls.cy = property(self.getter_cy(), self.setter_cy())


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

#!/usr/bin/env python
import sys
import curses


class CursedWindowClass(type):

    def __new__(cls, name, parents, dct):
        cls.WIDTH = dct.get('WIDTH', 80)
        cls.HEIGHT = dct.get('HEIGHT', 24)
        cls.WINDOW = None
        cls.APP = None
        cls.X = dct.get('X', 0)
        cls.Y = dct.get('Y', 0)
        cls.BORDERED = dct.get('BORDERED', False)
        return super(CursedWindowClass, cls).__new__(name, parents, dct)


class CursedWindow(object):
    __metaclass__ = CursedWindowClass

    _CW_WINDOW_SWAP_FUNCS = (
        'mvwin', 'move',
    )
    _CW_SCREEN_SWAP_FUNCS = (
    )
    _CW_WINDOW_FUNCS = (
        'refresh', 'clear', 'deleteln', 'erase', 'insertln', 'border',
        'nodelay', 'notimeout', 'clearok', 'is_linetouched', 'is_wintouched',
    )
    _CW_SCREEN_FUNCS = (
        'getch', 'getkey',
    )

    def addch(self, c, x=None, y=None, attr=None):
        x, y = self._fix_xy(x, y)
        if isinstance(c, int):
            c = chr(c)
        if attr is None:
            return self.WINDOW.addch(y, x, c)
        else:
            return self.WINDOW.addch(y, x, c, attr)

    def delch(self, x=None, y=None):
        x, y = self._fix_xy(x, y)
        return self.WINDOW.delch(y, x)

    def getwh(self):
        h, w = self.WINDOW.getmaxyx()
        return w, h

    def getxy(self):
        y, x = self.WINDOW.getyx()
        if self.border_shift:
            return x - 1, y - 1
        return x, y

    def inch(self, x=None, y=None):
        x, y = self._fix_xy(x, y)
        return self.WINDOW.inch(y, x)

    def insch(self, ch, x=None, y=None, attr=None):
        x, y = self._fix_xy(x, y)
        if attr is None:
            return self.WINDOW.insch(y, x, ch)
        else:
            return self.WINDOW.insch(y, x, ch, attr)

    def instr(self, x=None, y=None, n=None):
        x, y = self._fix_xy(x, y)
        if n is None:
            return self.WINDOW.instr(y, x)
        else:
            return self.WINDOW.instr(y, x, n)

    def insstr(self, s, x=None, y=None, attr=None):
        x, y = self._fix_xy(x, y)
        if attr is None:
            return self.WINDOW.insstr(y, x, s)
        else:
            return self.WINDOW.insstr(y, x, s, attr)

    def insnstr(self, s, x=None, y=None, n=None, attr=None):
        x, y = self._fix_xy(x, y)
        n = n if n is not None else self.WIDTH
        if attr is None:
            return self.WINDOW.insnstr(y, x, s, n)
        else:
            return self.WINDOW.insnstr(y, x, s, n, attr)

    def nextline(self, cr=True):
        x, y = self.getxy()
        if cr:
            x = 0
        x, y = self._fix_xy(x, y)
        self.WINDOW.move(y + 1, x)

    def fix_xy(self, x, y):
        if x is None or y is None:
            x0, y0 = self.getxy()
            x = x0 if x is None else x
            y = y0 if y is None else y
        if self.border_shift:
            return x + 1, y + 1
        return x, y

    def addstr(self, s, x=None, y=None, attr=None):
        x, y = self._fix_xy(x, y)
        if attr is None:
            return self.WINDOW.addstr(y, x, s)
        else:
            return self.WINDOW.addstr(y, x, s, attr)

    def addnstr(self, s, x=None, y=None, n=None, attr=None):
        x, y = self._fix_xy(x, y)
        n = self.WIDTH if n is None else n
        if attr is None:
            return self.WINDOW.addnstr(y, x, s, n)
        else:
            return self.WINDOW.addnstr(y, x, s, n, attr)

    def getstr(self, *args):
        if args:
            x, y = self._fix_xy(*args)
            return self.WINDOW.getstr(x, y)
        return self.WINDOW.getstr()

    def hline(self, x=None, y=None, char='-', n=None):
        x, y = self._fix_xy(x, y)
        n = self.WIDTH if n is None else n
        return self.WINDOW.hline(y, x, char, n)

    def vline(self, x=None, y=None, char='|', n=None):
        x, y = self._fix_xy(x, y)
        n = self.HEIGHT if n is None else n
        return self.WINDOW.vline(y, x, char, n)

    def _cw_set_window_func(self, attr):
        setattr(self.cls, attr, getattr(self.WINDOW, attr))

    def _cw_set_screen_func(self, attr):
        setattr(self.cls, attr, getattr(self.app.scr, attr))

    def _cw_swap_window_func(self, attr):
        func = getattr(self.WINDOW, attr)

        def new_func(s, x, y, *args, **kwargs):
            x, y = self._fix_xy(x, y)
            return func(y, x, *args, **kwargs)
        setattr(self.cls, attr, new_func)

    def _cw_swap_screen_func(self, attr):
        func = getattr(self.app.scr, attr)

        def new_func(s, x, y, *args, **kwargs):
            x, y = self._fix_xy(x, y)
            return func(y, x, *args, **kwargs)
        setattr(self.cls, attr, new_func)

    @property
    def cx(self):
        x, y = self._fix_xy(*self.get_xy())
        return x

    @property
    def cy(self):
        x, y = self._fix_xy(*self.get_xy())
        return y

    @cx.setter
    def cx(self, val):
        x, y = self._fix_xy(*self.get_xy())
        self.move(val, y)

    @cy.setter
    def cy(self, val):
        x, y = self._fix_xy(*self.get_xy())
        self.move(x, val)

    def _cw_run(self, window):
        self.WINDOW = window.subwin(self.HEIGHT, self.WIDTH, self.Y, self.X)
        if self.BORDERED:
            self.WINDOW.border()
        for attr in self._CW_WINDOW_FUNCS:
            self._cw_set_window_func(attr)
        for attr in self._CW_SCREEN_FUNCS:
            self._cw_set_screen_func(attr)
        for attr in self._CW_WINDOW_SWAP_FUNCS:
            self._cw_swap_window_func(attr)
        for attr in self._CW_SCREEN_SWAP_FUNCS:
            self._cw_swap_screen_func(attr)


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

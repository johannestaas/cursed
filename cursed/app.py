#!/usr/bin/env python
import sys
import traceback
from Queue import Queue
import curses
import gevent


BASE_CURSED_CLASSES = ('CursedWindowClass', 'CursedWindow', 'CursedMenu')


class CursedError(ValueError):
    pass


class CursedWindowClass(type):

    WINDOWS = []

    def __new__(cls, name, parents, dct):
        new = super(CursedWindowClass, cls).__new__(cls, name, parents, dct)
        if name in BASE_CURSED_CLASSES:
            return new
        new.WIDTH = dct.get('WIDTH', 80)
        new.HEIGHT = dct.get('HEIGHT', 24)
        new.WINDOW = None
        new.APP = None
        new.X = dct.get('X', 0)
        new.Y = dct.get('Y', 0)
        new.BORDERED = dct.get('BORDERED', False)
        new.EVENTS = Queue()
        new.RESULTS = Queue()
        new.KEY_EVENTS = Queue()
        new.SCROLL = dct.get('SCROLL', False)
        new.WAIT = dct.get('WAIT', True)
        cls.WINDOWS += [new]
        return new


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
    )

    @classmethod
    def getlkey(cls):
        key = cls.getkey()
        if key is None:
            return None
        return key.lower()

    @classmethod
    def getch(cls):
        if cls.KEY_EVENTS.empty():
            return None
        return cls.KEY_EVENTS.get()

    @classmethod
    def getkey(cls):
        if cls.KEY_EVENTS.empty():
            return None
        nchar = cls.KEY_EVENTS.get()
        return chr(nchar)

    @classmethod
    def addch(cls, c, x=None, y=None, attr=None):
        x, y = cls._fix_xy(x, y)
        if isinstance(c, int):
            c = chr(c)
        if attr is None:
            return cls.WINDOW.addch(y, x, c)
        else:
            return cls.WINDOW.addch(y, x, c, attr)

    @classmethod
    def delch(cls, x=None, y=None):
        x, y = cls._fix_xy(x, y)
        return cls.WINDOW.delch(y, x)

    @classmethod
    def getwh(cls):
        h, w = cls.WINDOW.getmaxyx()
        return w, h

    @classmethod
    def getxy(cls):
        y, x = cls.WINDOW.getyx()
        if cls.BORDERED:
            return x - 1, y - 1
        return x, y

    @classmethod
    def inch(cls, x=None, y=None):
        x, y = cls._fix_xy(x, y)
        return cls.WINDOW.inch(y, x)

    @classmethod
    def insch(cls, ch, x=None, y=None, attr=None):
        x, y = cls._fix_xy(x, y)
        if attr is None:
            return cls.WINDOW.insch(y, x, ch)
        else:
            return cls.WINDOW.insch(y, x, ch, attr)

    @classmethod
    def instr(cls, x=None, y=None, n=None):
        x, y = cls._fix_xy(x, y)
        if n is None:
            return cls.WINDOW.instr(y, x)
        else:
            return cls.WINDOW.instr(y, x, n)

    @classmethod
    def insstr(cls, s, x=None, y=None, attr=None):
        x, y = cls._fix_xy(x, y)
        if attr is None:
            return cls.WINDOW.insstr(y, x, s)
        else:
            return cls.WINDOW.insstr(y, x, s, attr)

    @classmethod
    def insnstr(cls, s, x=None, y=None, n=None, attr=None):
        x, y = cls._fix_xy(x, y)
        n = n if n is not None else cls.WIDTH
        if attr is None:
            return cls.WINDOW.insnstr(y, x, s, n)
        else:
            return cls.WINDOW.insnstr(y, x, s, n, attr)

    @classmethod
    def nextline(cls, cr=True):
        x, y = cls.getxy()
        if cr:
            x = 0
        x, y = cls._fix_xy(x, y)
        if y + 1 == cls.HEIGHT:
            if cls.SCROLL:
                cls.WINDOW.scroll()
                cls.WINDOW.move(y, 0)
            else:
                raise CursedError('Window %s reached height at %d' % (
                    cls.__name__, y + 1))
        else:
            cls.WINDOW.move(y + 1, x)

    @classmethod
    def write(cls, msg):
        cls.addstr(str(msg))
        cls.nextline()

    @classmethod
    def _fix_xy(cls, x, y):
        if x is None or y is None:
            x0, y0 = cls.getxy()
            x = x0 if x is None else x
            y = y0 if y is None else y
        if cls.BORDERED:
            return x + 1, y + 1
        return x, y

    @classmethod
    def addstr(cls, s, x=None, y=None, attr=None):
        x, y = cls._fix_xy(x, y)
        if attr is None:
            return cls.WINDOW.addstr(y, x, s)
        else:
            return cls.WINDOW.addstr(y, x, s, attr)

    @classmethod
    def addnstr(cls, s, x=None, y=None, n=None, attr=None):
        x, y = cls._fix_xy(x, y)
        n = cls.WIDTH if n is None else n
        if attr is None:
            return cls.WINDOW.addnstr(y, x, s, n)
        else:
            return cls.WINDOW.addnstr(y, x, s, n, attr)

    @classmethod
    def getstr(cls, *args):
        if args:
            x, y = cls._fix_xy(*args)
            return cls.WINDOW.getstr(x, y)
        return cls.WINDOW.getstr()

    @classmethod
    def hline(cls, x=None, y=None, char='-', n=None):
        x, y = cls._fix_xy(x, y)
        n = cls.WIDTH if n is None else n
        return cls.WINDOW.hline(y, x, char, n)

    @classmethod
    def vline(cls, x=None, y=None, char='|', n=None):
        x, y = cls._fix_xy(x, y)
        n = cls.HEIGHT if n is None else n
        return cls.WINDOW.vline(y, x, char, n)

    @classmethod
    def _cw_set_window_func(cls, attr):
        setattr(cls, attr, getattr(cls.WINDOW, attr))

    @classmethod
    def _cw_set_screen_func(cls, attr):
        setattr(cls, attr, getattr(cls.APP.scr, attr))

    @classmethod
    def _cw_swap_window_func(cls, attr):
        func = getattr(cls.WINDOW, attr)

        def new_func(s, x, y, *args, **kwargs):
            x, y = cls._fix_xy(x, y)
            return func(y, x, *args, **kwargs)
        setattr(cls, attr, new_func)

    @classmethod
    def _cw_swap_screen_func(cls, attr):
        func = getattr(cls.APP.scr, attr)

        def new_func(s, x, y, *args, **kwargs):
            x, y = cls._fix_xy(x, y)
            return func(y, x, *args, **kwargs)
        setattr(cls, attr, new_func)

    @classmethod
    def app_get(cls, var):
        return getattr(cls.APP, var)

    @classmethod
    def app_set(cls, var, val):
        return setattr(cls.APP, var, val)

    @property
    @classmethod
    def cx(cls):
        x, y = cls._fix_xy(*cls.get_xy())
        return x

    @property
    @classmethod
    def cy(cls):
        x, y = cls._fix_xy(*cls.get_xy())
        return y

    @cx.setter
    @classmethod
    def cx(cls, val):
        x, y = cls._fix_xy(*cls.get_xy())
        cls.move(val, y)

    @cy.setter
    @classmethod
    def cy(cls, val):
        x, y = cls._fix_xy(*cls.get_xy())
        cls.move(x, val)

    @classmethod
    def _cw_setup_run(cls, app, window):
        cls.RUNNING = True
        cls.APP = app
        cls.WINDOW = window.subwin(cls.HEIGHT, cls.WIDTH, cls.Y, cls.X)
        if cls.SCROLL:
            cls.WINDOW.scrollok(True)
            cls.WINDOW.idlok(1)
        if cls.BORDERED:
            cls.WINDOW.border()
        for attr in cls._CW_WINDOW_FUNCS:
            cls._cw_set_window_func(attr)
        for attr in cls._CW_SCREEN_FUNCS:
            cls._cw_set_screen_func(attr)
        for attr in cls._CW_WINDOW_SWAP_FUNCS:
            cls._cw_swap_window_func(attr)
        for attr in cls._CW_SCREEN_SWAP_FUNCS:
            cls._cw_swap_screen_func(attr)
        cls.WINDOW.refresh()

    @classmethod
    def _cw_handle_events(cls):
        while not cls.EVENTS.empty():
            func_name, args, kwargs = cls.EVENTS.get()
            if func_name == 'quit':
                if hasattr(cls, 'quit') and callable(cls.quit):
                    result = cls.quit(*args, **kwargs)
                    cls.RESULTS.put(('quit', args, kwargs, result))
                cls.RUNNING = False
                break
            if not hasattr(cls, func_name):
                raise CursedError('%s has no function %s' % (cls.__name__,
                                                             func_name))
            func = getattr(cls, func_name)
            if not callable(func):
                raise CursedError('%s has no callable %s' % (cls.__name__,
                                                             func_name))
            cls.RESULTS.put(
                (func_name, args, kwargs, func(*args, **kwargs))
            )

    @classmethod
    def _cw_run(cls, app, window):
        cls._cw_setup_run(app, window)
        has_update = hasattr(cls, 'update') and callable(cls.update)
        if hasattr(cls, 'init') and callable(cls.init):
            cls.trigger('init')
        while cls.RUNNING:
            # Yield to others for a bit
            gevent.sleep(0)
            cls._cw_handle_events()
            if has_update and cls.RUNNING:
                cls.update()

    @classmethod
    def trigger(cls, func_name, *args, **kwargs):
        cls.EVENTS.put((func_name, args, kwargs))


class Result(object):

    def __init__(self):
        self.exc_type, self.exc, self.tb = None, None, None

    def _extract_exception(self):
        self.exc_type, self.exc, self.tb = sys.exc_info()

    def _extract_thread_exception(self, thread):
        exc = thread.exception
        self.exc_type, self.exc, self.tb = thread.exc_info

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
            traceback.print_tb(self.tb)

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
        self.threads = []
        self.windows = None
        self.running = True

    def run_windows(self):
        self.windows = CursedWindowClass.WINDOWS
        self.active_window = None
        for i, cw in enumerate(self.windows):
            thread = gevent.spawn(cw._cw_run, self, self.window)
            cw.THREAD = thread
            self.threads += [thread]

    def input_loop(self):
        while self.running:
            for cw in self.windows:
                if cw.THREAD.exception is not None:
                    for cw in self.windows:
                        cw.RUNNING = False
                    self.running = False
                    break
                if cw.RUNNING and cw.WAIT:
                    break
            else:
                self.running = False
                break
            gevent.sleep(0)
            c = self.window.getch()
            if c == -1:
                continue
            for cw in self.windows:
                cw.KEY_EVENTS.put(c)

    def run(self):
        result = Result()
        try:
            self.scr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.window = self.scr.subwin(0, 0)
            self.window.keypad(1)
            self.window.nodelay(1)
            self.run_windows()
            self.threads += [gevent.spawn(self.input_loop)]
            gevent.joinall(self.threads)
            for thread in self.threads:
                if thread.exception:
                    result._extract_thread_exception(thread)
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


class CursedMenuBar(object):

    def __init__(self):
        self.menus = []

    def add_menu(self, title, key=None):
        title = title.strip()
        if not title:
            raise CursedError('Menu must have a name.')
        if key is None:
            key = title[0].lower()
        self.menus += [
            (key, title, [])
        ]

    def add_items(self, *args):
        if not self.menus:
            raise CursedError('Must add_menu before adding items.')
        mkey, mtitle, menu = self.menus[-1]
        for arg in args:
            if len(arg) == 2:
                name, cb = arg
                key = None
            elif len(arg) == 3:
                name, key, cb = arg
            else:
                raise CursedError('Format for menu item must be '
                                  '(Title, key, function name)')
            name = name.strip()
            if not name:
                raise CursedError('Menu item must have a name.')
            menu += [(name, key, cb)]


class CursedMenu(CursedWindow):
    HEIGHT = 1
    MENU = None
    WAIT = False
    KEYMAP = {}
    OPENED_MENU = None

    @classmethod
    def init(cls):
        for mkey, title, menu in cls.MENU.menus:
            key_d = {}
            cls.KEYMAP[mkey] = (title, key_d)
            for name, key, cb in menu:
                if key:
                    key_d[key] = cb

    @classmethod
    def _display(cls):
        l = 0
        for mkey, title, menu in cls.MENU.menus:
            cls.cy = 0
            cls.cx = l
            cls.addstr(title, attr=curses.A_BOLD)
            cls.addstr('  ')
            if cls.OPENED_MENU[0] == title:
                for name, key, cb in menu:
                    cls.cx = l
                    cls.cy += 1
                    s = name
                    if key:
                        s = '{} - {}'.format(name, key)
                    cls.addstr(s)
            l += len(title) + 2

    @classmethod
    def update(cls):
        c = cls.getch()
        if c is None:
            return
        if cls.OPENED_MENU is None:
            if chr(c) in cls.KEYMAP:
                cls._display()
                cls.OPENED_MENU = cls.KEYMAP[chr(c)]
        else:
            cb = cls.OPENED_MENU[1].get(chr(c))
            if cb is not None:
                func = getattr(cls, cb)
                func()

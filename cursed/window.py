#!/usr/bin/env python
'''
cursed.window

This contains the core logic used by cursed to create the window and offer the
ncurses interface to display everything.
'''

import curses
import gevent
import six
from cursed.exceptions import CursedSizeError, CursedCallbackError
from cursed.meta import CursedWindowClass
from cursed.menu import _Menu as Menu


@six.add_metaclass(CursedWindowClass)
class CursedWindow(object):
    '''
    The CursedWindow should be the parent class of all Window classes you
    declare.
    Each should have class variables X, Y, WIDTH, and HEIGHT declared.
    WIDTH and HEIGHT can be integers or 'max'.

    Each function in a class derived from CursedWindow should be a classmethod,
    since no instances of the class will be created. The code will run as the
    single class, like a singleton.
    '''

    _CW_WINDOW_SWAP_FUNCS = (
        'mvwin',
    )
    _CW_SCREEN_SWAP_FUNCS = (
    )
    _CW_WINDOW_FUNCS = (
        'clear', 'deleteln', 'erase', 'insertln', 'border',
        'nodelay', 'notimeout', 'clearok', 'is_linetouched', 'is_wintouched',
    )
    _CW_SCREEN_FUNCS = (
    )

    @classmethod
    def sleep(cls, seconds=0):
        '''
        Tell the CursedWindow's greenlet to sleep for seconds.
        This should be used to allow other CursedWindow's greenlets to execute,
        especially if you have long running code in your ``update`` classmethod.

        This is purely a restriction imposed by gevent, the concurrency library
        used for cursed. It is not truly parallel, so one long running greenlet
        can lock up execution of other windows. Calling cls.sleep() even with
        zero seconds (default) will allow other greenlets to start execution
        again.

        There is no benefit to calling sleep with a number other than zero. Zero
        will allow other greenlets to take over just fine.

        :param seconds: seconds to sleep. default zero is fine.
        '''
        return gevent.sleep(seconds)

    @classmethod
    def getch(cls):
        '''
        Get the integer value for the keypress, such as 27 for escape.

        :return: integer keycode of keypress
        '''
        if cls.KEY_EVENTS.empty():
            return None
        return cls.KEY_EVENTS.get()

    @classmethod
    def getkey(cls):
        '''
        Get the key that was pressed, or None.
        This is useful to simply check what key was pressed on the keyboard,
        ignoring special keys like the arrow keys.

        :return: character specifying key pressed, like 'a' or 'C'
        '''
        if cls.KEY_EVENTS.empty():
            return None
        nchar = cls.KEY_EVENTS.get()
        return chr(nchar)

    @classmethod
    def addch(cls, c, x=None, y=None, attr=None):
        '''
        Add a character to a position on the screen or at cursor.

        :param c: the character to insert
        :param x: optional x value, or current x position
        :param y: optional y value, or current y position
        :param attr: optional attribute, like 'bold'
        '''
        attr = cls._fix_attr(attr)
        x, y = cls._fix_xy(x, y)
        if isinstance(c, int):
            c = chr(c)
        if attr is None:
            return cls.WINDOW.addch(y, x, c)
        else:
            return cls.WINDOW.addch(y, x, c, attr)

    @classmethod
    def delch(cls, x=None, y=None):
        '''
        Delete a character at position, at cursor or specified position.

        :param x: optional x value
        :param y: optional y value
        '''
        x, y = cls._fix_xy(x, y)
        return cls.WINDOW.delch(y, x)

    @classmethod
    def getwh(cls):
        '''
        Get the width and height of a window.

        :return: (width, height)
        '''
        h, w = cls.WINDOW.getmaxyx()
        return w, h

    @classmethod
    def getxy(cls):
        '''
        Get the x and y position of the cursor.

        :return: (x, y)
        '''
        y, x = cls.WINDOW.getyx()
        if cls.BORDERED:
            x -= 1
            y -= 1
        if cls.MENU:
            y -= 1
        return x, y

    @classmethod
    def inch(cls, x=None, y=None):
        '''
        Return the character and attributes of the character at the specified
        position in the window or cursor.

        :param x: optional x value
        :param y: optional y value
        :return: (character, attributes)
        '''
        x, y = cls._fix_xy(x, y)
        ret = cls.WINDOW.inch(y, x)
        char = 0xf & ret
        attrs = 0xf0 & ret
        return char, attrs

    @classmethod
    def insch(cls, ch, x=None, y=None, attr=None):
        '''
        Write a character at specified position or cursor, with attributes.

        :param ch: character to insert
        :param x: optional x value
        :param y: optional y value
        :param attr: optional attributes
        '''
        x, y = cls._fix_xy(x, y)
        attr = cls._fix_attr(attr)
        if attr is None:
            return cls.WINDOW.insch(y, x, ch)
        else:
            return cls.WINDOW.insch(y, x, ch, attr)

    @classmethod
    def instr(cls, x=None, y=None, n=None):
        '''
        Return a string at cursor or specified position.
        If n is specified, returns at most n characters.

        :param x: optional x value
        :param y: optional y value
        :param n: optional max length of string
        :return: string at position
        '''
        x, y = cls._fix_xy(x, y)
        if n is None:
            return cls.WINDOW.instr(y, x)
        else:
            return cls.WINDOW.instr(y, x, n)

    @classmethod
    def insstr(cls, s, x=None, y=None, attr=None):
        '''
        Insert a string at cursor or specified position.
        Cursor is not moved and characters to the right are shifted right.

        :param s: the string
        :param x: optional x value
        :param y: optional y value
        :param attr: optional attributes
        '''
        x, y = cls._fix_xy(x, y)
        attr = cls._fix_attr(attr)
        if attr is None:
            return cls.WINDOW.insstr(y, x, s)
        else:
            return cls.WINDOW.insstr(y, x, s, attr)

    @classmethod
    def insnstr(cls, s, x=None, y=None, n=None, attr=None):
        '''
        Insert a string at cursor or specified position, at most n characters.
        Cursor is not moved and characters to the right are shifted right.
        If n is zero, all characters are inserted.

        :param s: the string
        :param x: optional x value
        :param y: optional y value
        :param n: max characters to insert (0 is all)
        :param attr: optional attributes
        '''
        x, y = cls._fix_xy(x, y)
        attr = cls._fix_attr(attr)
        n = n if n is not None else cls.WIDTH
        if attr is None:
            return cls.WINDOW.insnstr(y, x, s, n)
        else:
            return cls.WINDOW.insnstr(y, x, s, n, attr)

    @classmethod
    def nextline(cls):
        '''
        Goes to the next line like a carriage return.
        '''
        x, y = cls.getxy()
        x = 0
        x, y = cls._fix_xy(x, y)
        if y + 1 == cls.HEIGHT:
            if cls.SCROLL:
                cls.WINDOW.scroll()
                cls.WINDOW.move(y, 0)
            else:
                raise CursedSizeError('Window %s reached height at %d' % (
                    cls.__name__, y + 1))
        else:
            cls.WINDOW.move(y + 1, x)

    @classmethod
    def write(cls, msg, x=None, y=None):
        '''
        Writes a msg to the screen, with optional x and y values.
        If newlines are present, it goes to the next line.

        :param msg: the message to print
        :param x: optional x value
        :param y: optional y value
        '''
        x, y = cls._fix_xy(x, y)
        for i, line in enumerate(msg.splitlines()):
            if y == cls.HEIGHT - 1:
                break
            if len(line) + x >= cls.WIDTH:
                line = line[:cls.WIDTH - x - 1]
            cls.WINDOW.addstr(y, x, line)
            y += 1

    @classmethod
    def _fix_xy(cls, x, y):
        win_x, win_y = x, y
        curs_y, curs_x = cls.WINDOW.getyx()
        if x is None:
            win_x = curs_x
        if y is None:
            win_y = curs_y
        if x is not None and cls.BORDERED:
            win_x += 1
        if y is not None and cls.BORDERED:
            win_y += 1
        if y is not None and cls.MENU:
            win_y += 1
        return win_x, win_y

    @classmethod
    def _fix_attr(cls, attr):
        if isinstance(attr, six.string_types):
            return getattr(curses, 'A_%s' % attr.upper())
        return attr

    @classmethod
    def addstr(cls, s, x=None, y=None, attr=None):
        '''
        write the string onto specified position or cursor, overwriting anything
        already at position.

        :param s: string to write
        :param x: optional x value
        :param y: optional y value
        :param attr: optional attributes
        '''
        x, y = cls._fix_xy(x, y)
        attr = cls._fix_attr(attr)
        if attr is None:
            return cls.WINDOW.addstr(y, x, s)
        else:
            return cls.WINDOW.addstr(y, x, s, attr)

    @classmethod
    def addnstr(cls, s, x=None, y=None, n=None, attr=None):
        '''
        write at most n characters at specified position or cursor.

        :param s: string to write
        :param x: optional x value
        :param y: optional y value
        :param n: max number of characters
        :param attr: optional attributes
        '''
        x, y = cls._fix_xy(x, y)
        attr = cls._fix_attr(attr)
        n = cls.WIDTH if n is None else n
        if attr is None:
            return cls.WINDOW.addnstr(y, x, s, n)
        else:
            return cls.WINDOW.addnstr(y, x, s, n, attr)

    @classmethod
    def getstr(cls, x=None, y=None, prompt=None):
        '''
        Get string input from user at position, with optional prompt message.

        :param x: optional x value
        :param y: optional y value
        :param prompt: message to prompt user with, example: "Name: "
        :return: the string the user input
        '''
        x, y = cls._fix_xy(x, y)
        if prompt is not None:
            cls.WINDOW.addstr(y, x, prompt)
            x += len(prompt)
        curses.echo()
        s = cls.WINDOW.getstr(y, x)
        curses.noecho()
        return s.decode('utf-8')

    @classmethod
    def hline(cls, x=None, y=None, char='-', n=None):
        '''
        Insert a horizontal line at position, at most n characters or width of
        window.

        :param x: optional x value
        :param y: optional y value
        :param char: the character to print, default '-'
        :param n: the number of characters, default rest of width of window
        '''
        x, y = cls._fix_xy(x, y)
        n = cls.WIDTH if n is None else n
        return cls.WINDOW.hline(y, x, char, n)

    @classmethod
    def vline(cls, x=None, y=None, char='|', n=None):
        '''
        Insert a vertical line at position, at most n characters or height of
        window.

        :param x: optional x value
        :param y: optional y value
        :param char: the character to print, default '|'
        :param n: the number of characters, default rest of height of window
        '''
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
    def cx(cls, *args):
        '''
        Either the x position of cursor, or sets the x position.
        Example:
        ::

            # gets the x position of cursor
            my_x = cls.cx()

            # set the x position to 20
            cls.cx(20)

            # moves right 2 spots
            cls.cx(cls.cx() + 2)

        :param x: optional x position to move to
        :return: if x not specified, returns the x position of cursor
        '''
        x, y = cls.getxy()
        if not args:
            return x
        return cls.move(args[0], y)

    @classmethod
    def cy(cls, *args):
        '''
        Either the y position of cursor, or sets the y position.
        Example:
        ::

            # gets the y position of cursor
            my_y = cls.cy()

            # set the y position to 20
            cls.cy(20)

            # moves down 2 spots
            cls.cy(cls.cy() + 2)

        :param y: optional y position to move to
        :return: if y not specified, returns the y position of cursor
        '''
        x, y = cls.getxy()
        if not args:
            return y
        return cls.move(x, args[0])

    @classmethod
    def move(cls, x, y):
        '''
        Moves cursor to x and y specified.

        :param x: the x value, required
        :param y: the y value, required
        '''
        x, y = cls._fix_xy(x, y)
        cls.WINDOW.move(y, x)

    @classmethod
    def pad_move(cls, x, y):
        '''
        Reorients where the top left of the PAD should be, so it knows which
        region to display to the user.

        :param x: the x element of the top left of the region to display
        :param y: the y element of the top left of the region to display
        '''
        cls.PAD_X, cls.PAD_Y = x, y

    @classmethod
    def _cw_setup_run(cls, app, window):
        cls.RUNNING = True
        cls.APP = app
        height, width = window.getmaxyx()
        if width < cls.WIDTH:
            raise CursedSizeError('terminal width is %d and window width is '
                                  '%d' % (width, cls.WIDTH))
        if height < cls.HEIGHT:
            raise CursedSizeError('terminal height is %d and window height '
                                  'is %d' % (height, cls.HEIGHT))
        if cls.PAD:
            cls.WINDOW = curses.newpad(cls.PAD_HEIGHT, cls.PAD_WIDTH)
        else:
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

    @classmethod
    def redraw(cls):
        '''
        Redraws the window.
        '''
        cls.erase()
        if cls.BORDERED:
            cls.WINDOW.border()
        if cls.MENU:
            cls._cw_menu_display()
        cls.refresh()

    @classmethod
    def refresh(cls):
        if cls.PAD:
            # First two arguments the top left of the pad region to be displayed
            # Next four arguments represent the minrow, mincol, maxrow, maxcol
            # which are the top left on the screen and bottom right.
            cls.WINDOW.refresh(
                # Which location on the pad we scrolled to
                cls.PAD_Y, cls.PAD_X,
                # The top left of the pad where it is on the screen
                cls.Y, cls.X,
                # The bottom right of the pad where it is on the screen
                cls.Y + cls.HEIGHT - 1, cls.X + cls.WIDTH - 1
            )
        else:
            cls.WINDOW.refresh()

    @classmethod
    def openmenu(cls):
        '''
        Opens the menu, if menu is specified for the window.
        '''
        if cls._OPENED_MENU:
            return
        if not Menu.size():
            return
        cls._OPENED_MENU = Menu.get_menu_at(0)
        cls.redraw()

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
                raise CursedCallbackError('%s has no function %s' % (
                    cls.__name__, func_name))
            func = getattr(cls, func_name)
            if not callable(func):
                raise CursedCallbackError('%s has no callable %s' % (
                    cls.__name__, func_name))
            cls.RESULTS.put(
                (func_name, args, kwargs, func(*args, **kwargs))
            )

    @classmethod
    def _cw_menu_display(cls):
        x = 0
        # Because cls with MENU will add 1 to y in _fix_xy, we need true origin
        y = -1
        # Makes the menu standout
        menu_attrs = curses.A_REVERSE | curses.A_BOLD
        saved_pos = cls.getxy()
        for menu in Menu.ALL:
            # double check we're not going to write out of bounds
            if x + len(menu.title) + 2 >= cls.WIDTH:
                raise CursedSizeError('Menu %s exceeds width of window: x=%d' %
                                      (menu.title, x))
            y = -1
            cls.addstr(menu.title + '  ', x, y, attr=menu_attrs)
            mxlen = max([len(str(i)) for i in menu.items])
            if menu is cls._OPENED_MENU:
                for item in menu.items:
                    y += 1
                    itemstr = str(item)
                    wspace = (mxlen - len(itemstr)) * ' '
                    itemstr = itemstr + wspace
                    if item is menu.selected:
                        attr = curses.A_UNDERLINE
                    else:
                        attr = curses.A_REVERSE
                    cls.addstr(itemstr, x, y, attr=attr)
            # For the empty space filler
            x += len(menu.title) + 2
        # color the rest of the top of the window
        extra = 2 if cls.BORDERED else 0
        cls.addstr(' ' * (cls.WIDTH - x - extra), x, -1, attr=menu_attrs)
        cls.move(*saved_pos)

    @classmethod
    def _cw_menu_down(cls):
        cls._OPENED_MENU.down()
        cls.redraw()

    @classmethod
    def _cw_menu_up(cls):
        cls._OPENED_MENU.up()
        cls.redraw()

    @classmethod
    def _cw_menu_left(cls):
        Menu.clear_select()
        cls._OPENED_MENU = Menu.left(cls._OPENED_MENU)
        cls.redraw()

    @classmethod
    def _cw_menu_right(cls):
        Menu.clear_select()
        cls._OPENED_MENU = Menu.right(cls._OPENED_MENU)
        cls.redraw()

    @classmethod
    def _cw_menu_key(cls, k):
        cb = cls._OPENED_MENU.get_cb(k)
        cls._OPENED_MENU = None
        Menu.clear_select()
        cls.redraw()
        if cb:
            # Run callback associated with menu item
            cls.trigger(cb)

    @classmethod
    def _cw_menu_enter(cls):
        cb = None
        if cls._OPENED_MENU.selected:
            cb = cls._OPENED_MENU.selected.cb
        cls._OPENED_MENU = None
        Menu.clear_select()
        cls.redraw()
        if cb:
            cls.trigger(cb)

    @classmethod
    def _cw_menu_update(cls):
        if cls.KEY_EVENTS.empty():
            return None
        c = cls.KEY_EVENTS.get()
        k = None
        if 0 < c < 256:
            k = chr(c)
        if cls._OPENED_MENU is None:
            if k:
                cls._OPENED_MENU = Menu.get_menu_from_key(k)
                Menu.clear_select()
                cls.redraw()
            if cls._OPENED_MENU is None:
                cls.KEY_EVENTS.put(c)
        else:
            # If a menu is open, check if they pressed a key or up/down/enter
            if k and c != 0xa:
                cls._cw_menu_key(k)
            elif c == 0x102:
                cls._cw_menu_down()
            elif c == 0x103:
                cls._cw_menu_up()
            elif c == 0x104:
                cls._cw_menu_right()
            elif c == 0x105:
                cls._cw_menu_left()
            elif c == 0xa:
                cls._cw_menu_enter()
            else:
                # clear the menu
                cls._OPENED_MENU = None
                Menu.clear_select()
                cls.redraw()

    @classmethod
    def _cw_run(cls, app, window):
        cls._cw_setup_run(app, window)
        cls.redraw()
        has_update = hasattr(cls, 'update') and callable(cls.update)
        if hasattr(cls, 'init') and callable(cls.init):
            cls.trigger('init')
        while cls.RUNNING:
            # Yield to others for a bit
            gevent.sleep(0)
            if cls.MENU and cls.RUNNING:
                cls._cw_menu_update()
            cls._cw_handle_events()
            if has_update and cls.RUNNING:
                cls.update()

    @classmethod
    def trigger(cls, func_name, *args, **kwargs):
        '''
        Triggers a class function to be run by that window.
        This can be run across gevent coroutines to trigger other CursedWindow
        classes to run functions in their context.

        This is also used to cause a window to "quit" by running something
        like:
        ::

            MainWindow.trigger('quit')

        :param func_name: the name of the function to run
        :param args: the positional arguments, *args
        :param kwargs: the keyword arguments, **kwargs
        '''
        cls.EVENTS.put((func_name, args, kwargs))


def _debug(s):
    '''
    It's pretty hard to debug with all the threads running updates constantly...
    remote-pdb is the best solution besides some debug log hackery.
    '''
    with open('debug.log', 'a') as f:
        f.write(s + '\n')

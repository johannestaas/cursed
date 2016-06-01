#!/usr/bin/env python
'''
Welcome to cursed!

This is a simplified wrapper around the curses library to provide an easy API
to create a curses application, with easy concurrency across windows. It
provides a simple menu implementation as well.

The best way to get started is to look at an example. Here's the
examples/menu.py example from the main repository, with extra comments to
explain the various parts:

::

    from cursed import CursedApp, CursedWindow, CursedMenu

    # You instanciate the application through instanciating a CursedApp
    app = CursedApp()

    # The way to create windows is by creating classes derived from the
    # CursedWindow class. These must have X, Y, WIDTH, and HEIGHT specified
    # as class variables. 'max' or an integer value are valid for WIDTH and
    # HEIGHT.
    # A new gevent thread will be spawned for each window class.
    # These act like singletons, and all functions should be class methods.
    # The class itself will never be instanciated.
    class MainWindow(CursedWindow):
        X, Y = (0, 0)
        WIDTH, HEIGHT = 'max', 23

        # To create a menubar, you create a CursedMenu instance in a MENU
        # class variable.
        # You add a menu to it with the add_menu function, and specify the
        # title, optional hotkey, and a list of menu items in the form of
        # (name, hotkey, callback) or (name, callback).
        # Menu items can be chosen by hotkeys or by the arrow keys and enter.
        MENU = CursedMenu()
        MENU.add_menu('File', key='f', items=[
            ('Save', 's', 'save'),
            ('Quit', 'q', 'quit'),
        ])
        MENU.add_menu('Edit', key='e', items=[
            ('Copy', 'c', 'copy'),
            ('Delete', 'delete')
        ])

        # Decorate your methods with @classmethod since no instance will ever
        # be instanciated.
        @classmethod
        def save(cls):
            # cls.addstr will write a string to x and y location (5, 5)
            cls.addstr('File->Save', 5, 5)

        @classmethod
        def quit(cls):
            # The quit function will run before the window exits.
            # Killing the window is triggered with cls.trigger('quit'),
            # which is the same way to trigger any other function in the
            # CursedWindow.
            cls.addstr('Quitting', 5, 5)

        @classmethod
        def copy(cls):
            cls.addstr('edit->copy', 5, 5)

        @classmethod
        def delete(cls):
            cls.addstr('edit->delete', 5, 5)

        @classmethod
        def update(cls):
            # The update function will be looped upon, so this is where you
            # want to put the main logic. This is what will check for key
            # presses, as well as trigger other functions through
            # cls.trigger.
            # Handle input here, other than what the menu will handle through
            # triggering callbacks itself.
            cls.addstr('x=10, y=12', 10, 12)
            # Press spacebar to open menu
            k = cls.getch()
            if k == 32:
                cls.openmenu()


    class FooterWindow(CursedWindow):
        # This window will appear on the bottom, print the string
        # "Press f then q to exit", then quit. The message will stay on the
        # screen.
        # All windows must have called 'quit' to exit out of the program, or
        # simply ctrl-C could be pressed.
        X, Y = (0, 23)
        WIDTH, HEIGHT = 'max', 1

        @classmethod
        def init(cls):
            cls.addstr('Press f then q to exit')
            cls.refresh()
            cls.trigger('quit')


    # You need to call app.run() to start the application, which handles
    # setting up the windows.
    result = app.run()
    print(result)
    # This checks if ctrl-C or similar was pressed to kill the application.
    if result.interrupted():
        print('Ctrl-C pressed.')
    else:
        # This will reraise exceptions that were raised in windows.
        result.unwrap()

That's the essentials of it. Just remember to trigger('quit') to all your
windows if you want it to exit cleanly.

New in 2.0
----------

Added pads!

Now, you can specify a pad CursedWindow like so::

    class MyPad(CursedWindow):
        X, Y = 0, 0
        WIDTH, HEIGHT = 40, 40

        # set PAD to True
        PAD = True

        # the top left of the region to display
        PAD_X, PAD_Y = 0, 0

        # the virtual width and height, which you can scroll around to
        PAD_WIDTH, PAD_HEIGHT = 500, 500

        @classmethod
        def update(cls):
            ...
            # get new coordinates for top left of region
            ...
            cls.PAD_X, cls.PAD_Y = top_left_x, top_left_y
            ...
            # will now display the correct region in a smaller 40x40 display
            cls.refresh()

This is useful for when you might want to do something like scroll through a
map. See examples/pad.py for an example which scrolls through text using the
arrow keys.
'''

import sys
import traceback
import gevent
import six
import curses

from cursed.window import CursedWindowClass


class Result(object):
    '''
    Result represents the object returned by `app.run()`, which may contain
    exception information.
    '''

    def __init__(self):
        self.exc_type, self.exc, self.tb = None, None, None

    def _extract_exception(self):
        self.exc_type, self.exc, self.tb = sys.exc_info()

    def _extract_thread_exception(self, thread):
        self.exc_type, self.exc, self.tb = thread.exc_info

    def unwrap(self):
        '''
        Unwraps the `Result`, raising an exception if one exists.
        '''
        if self.exc:
            six.reraise(self.exc_type, self.exc, self.tb)

    def ok(self):
        '''
        Return True if no exception occurred.
        '''
        return not bool(self.exc)

    def err(self):
        '''
        Returns the exception or None.
        '''
        return self.exc if self.exc else None

    def interrupted(self):
        '''
        Returns True if the application was interrupted, like through Ctrl-C.
        '''
        return self.exc_type is KeyboardInterrupt

    def print_exc(self):
        '''
        Prints the exception traceback.
        '''
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
    '''
    The CursedApp is the main class which is used to track windows that are
    created and finally run the application.

    The CursedApp is initialized then run in the main function to build the
    windows.

    Example:
    ::

        from cursed import CursedApp, CursedWindow

        app = CursedApp()

        class MainWindow(CursedWindow):
            X, Y = (0, 0)
            WIDTH, HEIGHT = ('max', 'max')

            ...

        result = app.run()
        result.unwrap()
    '''

    def __init__(self):
        '''
        Initializes the CursedApp. No parameters are required.
        '''
        self.scr = None
        self.menu = None
        self.threads = []
        self.windows = None
        self.running = True

    def _run_windows(self):
        CursedWindowClass._fix_windows(self.MAX_WIDTH, self.MAX_HEIGHT)
        self.windows = CursedWindowClass.WINDOWS
        self.active_window = None
        for i, cw in enumerate(self.windows):
            thread = gevent.spawn(cw._cw_run, self, self.window)
            cw.THREAD = thread
            self.threads += [thread]

    def _input_loop(self):
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
        '''
        Runs all the windows added to the application, and returns a `Result`
        object.

        '''
        result = Result()
        try:
            self.scr = curses.initscr()
            self.MAX_HEIGHT, self.MAX_WIDTH = self.scr.getmaxyx()
            curses.noecho()
            curses.cbreak()
            curses.start_color()
            curses.use_default_colors()
            self.window = self.scr.subwin(0, 0)
            self.window.keypad(1)
            self.window.nodelay(1)
            self._run_windows()
            self.threads += [gevent.spawn(self._input_loop)]
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

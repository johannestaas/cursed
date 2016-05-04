#!/usr/bin/env python
import traceback
import curses


class CursedApp(object):

    def __init__(self):
        self.scr = None
        self.menu = None
        self.windows = []

    def run(self):
        try:
            self.scr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.window = self.scr.subwin(0, 0)
            self.window.keypad(1)
        except Exception:
            traceback.print_exc()
        finally:
            if self.scr is not None:
                self.scr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

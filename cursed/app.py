#!/usr/bin/env python
import traceback
import curses


class CursedApp(object):

    def __init__(self):
        self.scr = None

    def __enter__(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.window = self.scr.subwin(0, 0)
        self.window.keypad(1)
        self.menu_panel = curses.panel.new_panel(self.window)
        self.panel.hide()
        curses.panel.update_panels()
        return self

    def __exit__(self, *excs):
        if self.scr is None:
            return
        self.scr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()

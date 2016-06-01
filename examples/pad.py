#!/usr/bin/env python

import os
import random
import curses
from cursed import CursedApp, CursedWindow

this_dir = os.path.dirname(__file__)
text_path = os.path.join(this_dir, 'pad.txt')

with open(text_path) as f:
    cursed_text = f.read()

app = CursedApp()


def old_generate_map(width, height):
    noise = [[r for r in range(width)] for i in range(height)]
    for y in range(0, height):
        for x in range(0, width):
            noise[y][x] = ' ' if random.randint(0, 1) == 0 else '#'
    return noise


def generate_map(width, height):
    text = [[r for r in range(width)] for i in range(height)]
    ctext = cursed_text.splitlines()
    ctext = [x + '  ' for x in ctext]
    ctext_w = max(len(s) for s in ctext)
    ctext += [' ' * ctext_w]
    ctext_h = len(ctext)
    for y in range(0, height):
        for x in range(0, width):
            ym = y % ctext_h
            xm = x % ctext_w
            line = ctext[ym]
            if xm >= len(line):
                text[y][x] = ' '
            else:
                text[y][x] = line[xm]
    return text


class MainWindow(CursedWindow):

    X, Y = 0, 0
    WIDTH, HEIGHT = 56, 24
    BORDERED = True

    @classmethod
    def update(cls):
        cls.write(
            '''This is a sample application with a Pad.
A Pad can be drawn on the screen but represent a small
region of a much wider area, so you can effectively
navigate something like a map. This one on the right
is 100 by 100 even though it's 24x24 size on the
screen. It has random elements drawn on it, and you
can navigate with the arrow keys.''', x=0, y=0)
        cls.trigger('quit')


class MainPad(CursedWindow):

    X, Y = 56, 0
    WIDTH, HEIGHT = 24, 24
    PAD = True
    PAD_WIDTH, PAD_HEIGHT = 100, 100
    PAD_X, PAD_Y = 0, 0

    MAP = generate_map(PAD_WIDTH, PAD_HEIGHT)

    @classmethod
    def update(cls):
        key = cls.getch()
        if key is not None:
            if key == curses.KEY_UP:
                cls.PAD_Y = max(cls.PAD_Y - 1, 0)
            elif key == curses.KEY_DOWN:
                cls.PAD_Y = min(
                    cls.PAD_Y + 1,
                    cls.PAD_HEIGHT - (cls.HEIGHT + 1)
                )
            elif key == curses.KEY_LEFT:
                cls.PAD_X = max(cls.PAD_X - 1, 0)
            elif key == curses.KEY_RIGHT:
                cls.PAD_X = min(
                    cls.PAD_X + 1,
                    cls.PAD_WIDTH - (cls.WIDTH + 1)
                )
            elif key == ord('q'):
                cls.trigger('quit')
        for y in range(cls.PAD_Y, cls.PAD_Y + cls.HEIGHT):
            s = cls.MAP[y][cls.PAD_X:cls.PAD_X + cls.PAD_HEIGHT]
            s = ''.join(x for x in s)
            cls.addstr(s, cls.PAD_X, y)
        cls.refresh()


result = app.run()
result.unwrap()

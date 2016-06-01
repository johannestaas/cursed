#!/usr/bin/env python

from cursed import CursedWindow, CursedApp

app = CursedApp()


class LeftWindow(CursedWindow):
    X, Y = 0, 0
    WIDTH = 24
    HEIGHT = 24
    BORDERED = True

    @classmethod
    def update(cls):
        cls.write('N,N', x=None, y=None)
        cls.write('0,0', x=0, y=0)
        cls.write('1,1', x=1, y=1)
        cls.write('2,2', x=2, y=2)
        cls.write('N,N', x=None, y=3)


class RightWindow(CursedWindow):
    X, Y = 24, 0
    WIDTH, HEIGHT = 24, 24
    BORDERED = True

    @classmethod
    def update(cls):
        cls.write('N,N', x=None, y=None)
        cls.write('0,0', x=0, y=0)
        cls.write('1,1', x=1, y=1)
        cls.write('2,2', x=2, y=2)
        cls.write('N,N', x=None, y=3)


class BottomLeftWindow(CursedWindow):
    X, Y = 0, 24
    WIDTH, HEIGHT = 24, 24
    BORDERED = True

    @classmethod
    def update(cls):
        cls.write('N,N', x=None, y=None)
        cls.write('0,0', x=0, y=0)
        cls.write('1,1', x=1, y=1)
        cls.write('2,2', x=2, y=2)
        cls.write('N,N', x=None, y=3)


class BottomRightWindow(CursedWindow):
    X, Y = 24, 24
    WIDTH, HEIGHT = 24, 24
    BORDERED = True

    @classmethod
    def update(cls):
        cls.write('N,N', x=None, y=None)
        cls.write('0,0', x=0, y=0)
        cls.write('1,1', x=1, y=1)
        cls.write('2,2', x=2, y=2)
        cls.write('N,N', x=None, y=3)


app.run().unwrap()


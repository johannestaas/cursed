#!/usr/bin/env python
import os
import socket
from datetime import datetime
from cursed import CursedApp, CursedWindow
import requests

app = CursedApp()
last_time = None
last_ip = None
hostname = socket.gethostname()
username = os.getlogin()
cwd = os.getcwd()


def my_ip():
    global last_time, last_ip
    now = datetime.now()
    if last_time is None or (now - last_time).seconds >= 10:
        response = requests.get('http://icanhazip.com')
        last_time = now
        last_ip = response.content.strip()
    return last_ip


def my_mem():
    with open('/proc/meminfo') as f:
        lines = f.readlines()
    return [x.strip() for x in lines if x.startswith('Mem')]


class MainWindow(CursedWindow):
    X, Y = (0, 0)
    WIDTH, HEIGHT = ('max', 23)
    BORDERED = True

    @classmethod
    def update(cls):
        cls.erase()
        cls.border()
        c = cls.getch()
        if c == 27:
            cls.trigger('quit')
            return
        cls.addstr('username: %s' % username, 0, 0)
        cls.nextline()
        cls.addstr('hostname: %s' % hostname)
        cls.nextline()
        cls.addstr('cwd: %s' % cwd)
        cls.nextline()
        cls.addstr('IP addr: %s' % my_ip())
        cls.nextline()
        for mem_line in my_mem():
            cls.addstr(mem_line)
            cls.nextline()
        cls.refresh()


class BottomMessage(CursedWindow):
    X, Y = (0, 23)
    WIDTH, HEIGHT = ('max', 1)
    BORDERED = False

    @classmethod
    def init(cls):
        cls.addstr('Press ESCAPE to quit')
        cls.refresh()
        cls.trigger('quit')


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

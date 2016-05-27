#!/usr/bin/env python
import requests
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class HeaderWindow(CursedWindow):
    HEIGHT = 3

    @classmethod
    def update(cls):
        cls.addstr('Cursed Browser', 0, 0)
        cls.hline(0, 1)
        url = cls.getstr(0, 2, prompt='URL: ')
        if url:
            DisplayWindow.trigger('get_request', url)


class DisplayWindow(CursedWindow):
    Y = 3
    HEIGHT = 21
    BORDERED = True

    @classmethod
    def get_request(cls, url):
        cls.response = requests.get(url)
        cls.redraw()
        cls.write(cls.response.content, 0, 0)


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

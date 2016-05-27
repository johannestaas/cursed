#!/usr/bin/env python
import requests
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class HeaderWindow(CursedWindow):
    HEIGHT = 24

    @classmethod
    def update(cls):
        cls.addstr('Cursed Browser', 0, 0)
        cls.hline(0, 1)
        url = cls.getstr(0, 2, prompt='URL: ')
        if url:
            HeaderWindow.trigger('get_request', url)

    @classmethod
    def get_request(cls, url):
        cls.response = requests.get(url)
        # cls.redraw()
        cls.write(cls.response.content, 0, 3)

'''
# Fix - seems not to getstr with other window
class DisplayWindow(CursedWindow):
    HEIGHT = 21

    @classmethod
    def get_request(cls, url):
        cls.response = requests.get(url)
        # cls.redraw()
        cls.write(cls.response.content)
'''

result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

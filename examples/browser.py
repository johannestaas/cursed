#!/usr/bin/env python
import os
import requests
from cursed import CursedApp, CursedWindow, CursedMenu
app = CursedApp()


class HeaderWindow(CursedWindow):
    X, Y = (0, 0)
    WIDTH, HEIGHT = ('max', 3)
    MENU = CursedMenu()
    MENU.add_menu('File', 'f')
    MENU.add_items(('Save response', 's', 'save'))
    MENU.add_items(('Quit', 'q', 'quit'))
    MENU.add_menu('Browse', 'b')
    MENU.add_items(('Open URL', 'o', 'open_url'))

    @classmethod
    def update(cls):
        k = cls.getch()
        # space bar
        if k == 32:
            cls.openmenu()
        # tab
        elif k == 9:
            cls.open_url()

    @classmethod
    def open_url(cls):
        cls.redraw()
        url = cls.getstr(0, 1, prompt='URL: ')
        if url:
            DisplayWindow.trigger('get_request', url)

    @classmethod
    def save(cls):
        cls.redraw()
        if not (
            hasattr(DisplayWindow, 'response') and
            DisplayWindow.response.content
        ):
            cls.addstr('Error: No response content to save yet', 0, 1)
        else:
            path = cls.getstr(0, 1, prompt='save to file: ')
            if path:
                cls.redraw()
                if os.path.exists(path):
                    cls.addstr('Error: {0} exists! please save to a new path.'
                               .format(path), 0, 1)
                else:
                    with open(path, 'wb') as f:
                        f.write(DisplayWindow.response.content)
                    cls.addstr('Saved to {0}'.format(path), 0, 1)
            else:
                cls.redraw()
                cls.addstr('Error: please enter a path to a new file.', 0, 1)

    @classmethod
    def quit(cls):
        DisplayWindow.trigger('quit')


class DisplayWindow(CursedWindow):
    X, Y = (0, 3)
    WIDTH, HEIGHT = ('max', 'max')
    BORDERED = True

    @classmethod
    def get_request(cls, url):
        cls.redraw()
        try:
            cls.response = requests.get(url)
        except Exception as e:
            cls.addstr('Error: {0}'.format(e), 0, 0)
        else:
            cls.write(cls.response.content, 0, 0)


result = app.run()
print(result)
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    result.unwrap()

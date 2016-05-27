cursed
======

Simplified curses interface with concurrency, for quick and sane curses apps.

Allows easy creation of windows and menus. Code for each window runs concurrently.

Installation
------------

With pip, for the latest stable::

    $ pip install cursed

Or from the project root directory::

    $ python setup.py install

Usage
-----

Example::

    from cursed import CursedApp, CursedWindow

    app = CursedApp()
    
    class MainWindow(CursedWindow):
        WIDTH=80
        BORDERED = True

        @classmethod
        def update(cls):
            ''' update runs every tick '''
            # Hello world printed at x,y of 0,0
            cls.addstr('Hello, world!', 0, 0)
            if cls.getch() == 27:
                # Escape was pressed. Quit.
                cls.trigger('quit')

    result = app.run()
    if result.interrupted():
        # check if ctrl-C was pressed
        print('Quit!')
    else:
        # Raises an exception if any thread ran into a different exception.
        result.unwrap()

Release Notes
-------------

:0.1.4:
    - Implemented getstr
:0.1.3:
    - Fixed menu to fill up right side with whitespace
:0.1.2:
    - fixed menus stealing keypresses
:0.1.1:
    - left and right open menus to sides
    - refactored menus
:0.1.0:
    - implemented menus!
:0.0.2:
    - implemented lots from the following:
        1. https://docs.python.org/2/library/curses.html
        2. https://docs.python.org/2/howto/curses.html
:0.0.1:
    - Project created

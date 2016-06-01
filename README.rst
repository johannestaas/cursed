cursed!::

      ______     __  __     ______     ______     ______     _____    
     /\  ___\   /\ \/\ \   /\  == \   /\  ___\   /\  ___\   /\  __-.  
     \ \ \____  \ \ \_\ \  \ \  __<   \ \___  \  \ \  __\   \ \ \/\ \ 
      \ \_____\  \ \_____\  \ \_\ \_\  \/\_____\  \ \_____\  \ \____- 
       \/_____/   \/_____/   \/_/ /_/   \/_____/   \/_____/   \/____/ 
                                                                     

Simplified curses interface with concurrency, for quick and sane curses apps.

Allows easy creation of windows and menus. Code for each window runs concurrently.

Please see full documentation available here: http://pythonhosted.org/cursed/

cursed was tested with Python 3.4 and 2.7, and depends on the Python package six for compatibility.

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

    # the main context of the curses application
    app = CursedApp()
    
    # Derive from CursedWindow to declare curses windows to be created after app.run()
    # It is required to declare X, Y, WIDTH, and HEIGHT for each window.
    # You'll want to put the main looping code for each window thread in the `update` class function.
    
    class MainWindow(CursedWindow):
    
        # Coordinate for top-left of window.
        X, Y = (0, 0)
        
        # WIDTH and HEIGHT can be 'max' or integers.
        WIDTH, HEIGHT = ('max', 'max')
        
        # Create a default border around the window.
        BORDERED = True

        @classmethod
        def update(cls):
            ''' update runs every tick '''
            
            # Hello world printed at x,y of 0,0
            cls.addstr('Hello, world!', 0, 0)
            
            # Get character keycode of keypress, or None.
            if cls.getch() == 27:
                # Escape was pressed. Quit.
                # 'quit' must be triggered for each open window for the program to quit.
                # Call cls.trigger('quit') to quit the window you're in, and to quit the other
                # declared windows, call OtherWindow.trigger('quit') which will run in that
                # window's thread, regardless of where it's called.
                cls.trigger('quit')

    # To trigger app to start
    result = app.run()
    
    # check if ctrl-C was pressed
    if result.interrupted():
        print('Quit!')
    else:
        # Raises an exception if any thread ran into a different exception.
        result.unwrap()

Many more examples are available in the root of the repository at examples/

Release Notes
-------------

:0.2.0:
    - exposed gevent.sleep through a classmethod ``cls.sleep(seconds=0)``.
      This allows users to fix issues with long running update functions causing other windows to
      not respond.
    - Added a CursedWindow PAD, like the curses pad. This can have a huge width and height greater than
      the terminal width, but allow you to scroll around it. Useful for windows which need only display
      a smaller rectange of a larger window, like a map that scrolls around with arrow keys.
:0.1.9:
    - fixed the ``write`` and ``getstr`` classmethods, since they called _fix_xy twice
    - added info to menu example to explain ``addstr`` in update will overwrite menu display
:0.1.8:
    - added tons of documentation and examples
:0.1.7:
    - Better CursedMenu API
:0.1.6:
    - WIDTH or HEIGHT specified as 'max' will stretch to the full width or height of the terminal
:0.1.5:
    - patched issue with returning bytes in getstr
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

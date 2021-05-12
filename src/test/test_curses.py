import curses
import datetime
import time


def start_demo():
    # -- Initialize --
    stdscr = curses.initscr()  # initialize curses screen
    try:

        curses.noecho()  # turn off auto echoing of keypress on to screen
        curses.cbreak()  # enter break mode where pressing Enter key
        #  after keystroke is not required for it to register
        stdscr.keypad(True)  # enable special Key values such as curses.KEY_LEFT etc

        # -- Perform an action with Screen --
        stdscr.border(0)
        stdscr.addstr(5, 5, 'Hello from Curses!', curses.A_BOLD)
        stdscr.addstr(6, 5, 'Press q to close this screen', curses.A_NORMAL)

        while True:
            ti = str((datetime.datetime.now().time()))
            stdscr.addstr(8, 5, 'Time: ' + ti, curses.A_NORMAL)
            time.sleep(3)
            stdscr.refresh()
            ch = stdscr.getch()
            if ch == ord('q'):
                break

    except Exception as e:
        print(str(e))

    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


start_demo()

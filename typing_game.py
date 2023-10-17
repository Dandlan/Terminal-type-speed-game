import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Hello there")
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
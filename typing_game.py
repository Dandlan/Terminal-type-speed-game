import curses
from curses import wrapper
import time
import random

used_texts = set()

def start_screen(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    center_y = height // 2
    center_x = (width - len("Welcome to the Speed Typing Test!")) // 2
    
    stdscr.addstr(center_y, center_x, "Welcome to the Speed Typing Test!")
    stdscr.addstr(center_y + 1, center_x, "Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    height, width = stdscr.getmaxyx()
    center_y = height // 2
    center_x = (width - len(target)) // 2
    
    stdscr.addstr(center_y, center_x, target)
    stdscr.addstr(center_y + 1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(center_y, center_x + i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        unused_texts = list(set(lines) - used_texts)
        if not unused_texts:
            used_texts.clear()
            unused_texts = lines
        selected_text = random.choice(unused_texts).strip()
        used_texts.add(selected_text)
        return selected_text

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)
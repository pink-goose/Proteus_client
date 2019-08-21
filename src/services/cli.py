import os
import io
import sys
import time
import signal
import logging
import subprocess
from threading import Thread

import curses
from curses.textpad import Textbox


logger = logging.getLogger(__name__)


##########################################################################
# Log file monitoring

class LogMonitor(Thread):
    def __init__(self, filename, drawer_object):
        self.filename = filename
        self.st_results = os.stat(filename)
        Thread.__init__(self)
        self.drawer_object = drawer_object

    def run(self):
        while True:
            try:
                st_results = os.stat(self.filename)

                # Check if file has been modified since last read
                if not st_results.st_mtime == self.st_results.st_mtime:
                    self.read_file_from(self.st_results.st_size)
                    self.st_results = st_results

            except OSError:
                # ignore any file IO exceptions, just try again
                pass
            time.sleep(0.1)

    def read_file_from(self, frombytes):
        with io.open(self.filename) as f:
            f.seek(frombytes)
            while True:
                line = f.readline()
                if line == "":
                    break

                # append to log
                # print(line)
                self.drawer_object.print_to_logger('Client', line)


def start_log_monitor(filename, drawer_object):
    if os.path.isfile(filename):
        thread = LogMonitor(filename, drawer_object)
        thread.setDaemon(True)  # this thread won't prevent prog from exiting
        thread.start()

##########################################################################
# Screen drawing


class DrawScreen:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def init_curses_colors(self):
        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def main(self):
        self.init_curses_colors()
        signal.signal(signal.SIGINT, self.signal_handler)
        height, width = self.stdscr.getmaxyx()

        header_win = self.draw_header_window(height=1, width=width)
        self.logger_win = self.draw_logger_window(height, width)
        footer_win = self.draw_footer_window(height, width)
        self.editor_win = self.draw_editor_window(height, width)

        self.logger_win.scrollok(True)
        self.logger_win.idlok(True)
        self.logger_win.leaveok(True)

        edit_box = self.create_textbox(self.editor_win)

        self.edit_loop(edit_box, self.editor_win)

    def draw_header_window(self, height, width):
        header_win_width = width
        header_win_height = height

        header_win = curses.newwin(header_win_height, header_win_width, 0, 0)
        # header
        header_win.addstr(0, 1, '=' * (header_win_width - 2), curses.color_pair(2))
        header_win.addstr(0, 3, ' Proteus ', curses.color_pair(1))
        header_win.refresh()
        return header_win

    def draw_logger_window(self, height, width):
        log_win_width = width
        log_win_height = height - 4

        # win = curses.newwin(height, width, begin_y, begin_x)
        log_win = curses.newwin(log_win_height, log_win_width, 1, 0)

        # log_win.addstr(2, 2, 'Sample input')
        log_win.refresh()
        return log_win

    def draw_footer_window(self, height, width):
        # footer_splitter
        footer_win = curses.newwin(2, width, height - 2, 0)
        footer_win.addstr(0, 1, '=' * (width - 2), curses.color_pair(2))
        footer_win.addstr(0, 3, ' Input: ', curses.color_pair(1))
        footer_win.addstr(1, 0, ' > ')
        footer_win.refresh()
        return footer_win

    def draw_editor_window(self, height, width):
        # footer_editor
        edit_win = curses.newwin(1, width, height - 1, 3)
        edit_win.refresh()
        return edit_win

    def create_textbox(self, win):
        edit_box = Textbox(win)
        return edit_box

    def edit(self, box, edit_win):
        box.edit()
        message = box.gather()
        edit_win.clear()
        edit_win.refresh()
        return message

    def edit_loop(self, box, editor_win):
        message = self.edit(box, editor_win)
        source = 'You'
        self.print_to_logger(source, message)
        ######

        from .main import text_request
        text_request(message)

        ######
        self.edit_loop(box, editor_win)

    # TODO place into a decorator
    def print_to_logger(self, source, message):
        formatted_mesage = f'{source}: {message}'
        self.logger_win.addstr(f'\n {formatted_mesage}')
        self.logger_win.refresh()

        # TODO just zaglushka, peredelat
        # self.editor_win.clear()
        self.editor_win.addstr(0, 0, '')
        self.editor_win.refresh()

    def signal_handler(self, sig, frame):
        # pressed Ctrl+C
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        # TODO find a way to close processes normally
        p = subprocess.Popen(['pgrep', 'python'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print(line)
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
        sys.exit(0)


if __name__ == '__main__':
    drawer = DrawScreen()
    # start_log_monitor('sample.log', drawer)
    drawer.main()

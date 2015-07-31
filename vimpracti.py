#!/usr/bin/env python

import signal
import sys, tty, termios


QUESTION_VAULT = [
    {
        'k': 'Move cursor one character top',
        'j': 'Move cursor one character down',
        'l': 'Move cursor one character right',
        'h': 'Move cursor one character left',
        'w': 'Move one word',
        'e': 'Move to the end of the word',
        'b': 'Move to the beginning of the word',
        'h': 'Move cursor one character left',
        'h': 'Move cursor one character left',
        'h': 'Move cursor one character left',
        'h': 'Move cursor one character left',
    },
]

class AlarmException(Exception):
    pass


class GetchUnix:
    """This class simulates Windows getch call. It simply reads specific number of characters
       without need to type enter. Time to type characters is limited by timeout, which is 
       increased by a second for every extra character."""

    def __call__(self, keypresses=1, timeout=4):
        timeout += 1 * keypresses
        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(timeout)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(keypresses)
            signal.alarm(0)
        except AlarmException:
            signal.signal(signal.SIGALRM, self.alarm_handler)
            char = None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return char

    def alarm_handler(self, signum, frame):
        raise AlarmException


getch = GetchUnix()
x = getch(1)
if x:
    print('You pressed {}'.format(x))

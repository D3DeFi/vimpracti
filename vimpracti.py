#!/usr/bin/env python

import signal
import sys, tty, termios


SHORTCUT_ESC = '\x1b'
QUESTION_VAULT = [
    {
        ## navigation
        'h': 'Move cursor one character left',
        'j': 'Move cursor one character down',
        'k': 'Move cursor one character up',
        'l': 'Move cursor one character right',
        'w': 'Jump by start of words (punctuation considered words)',
        'W': 'Jump by words (spaces separate words)',
        'e': 'jump to end of words (punctuation considered words)',
        'E': 'jump to end of words (no punctuation)',
        'b': 'jump backward by words (punctuation considered words)',
        'B': 'jump backward by words (no punctuation)',
        '0': 'start of line',
        '^': 'first non-blank character of line',
        '$': 'end of line',
        'G': 'Go To command (prefix with number)',
        'i': 'start insert mode at cursor',
        'I': 'insert at the beginning of the line',
        'a': 'append after the cursor',
        'A': 'append at the end of the line',
        'o': 'open (append) blank line below current line (no need to press return)',
        'O': 'open blank line above current line',
        'ea': 'append at end of word',
        'Esc': 'exit insert mode',
    },
    {
        ## editing
        'r': 'replace a single character (does not use insert mode)',
        'J': 'join line below to the current one',
        'cc': 'change (replace) an entire line',
        'cw': 'change (replace) to the end of word',
        'c$': 'change (replace) to the end of line',
        's': 'delete character at cursor and subsitute text',
        'S': 'delete line at cursor and substitute text (same as cc)',
        'xp': 'transpose two letters (delete and paste, technically)',
        'u': 'undo',
        '.': 'repeat last command',
    },
    {
        ## marking text (in visual mode)
         'v': 'start visual mode, mark lines, then do command (such as y-yank)',
         'V': 'start Linewise visual mode',
         'o': 'move to other end of marked area',
         'O': 'move to Other corner of',
         'aw': 'mark a word',
         'ab': 'mark a () block (with braces)',
         'aB': 'mark a {} block (with brackets)',
         'ib': 'mark inner () block',
         'iB': 'mark inner {} block',
         'Esc': 'exit visual mode',
    },
    {
        ## visual commands
        '>': 'shift right',
        '<': 'shift left',
        'y': 'yank (copy) marked text',
        'd': 'delete marked text',
        '~': 'switch case',
    },
    {
        ## cut and paste
        'yy': 'yank (copy) a line',
        '2yy': 'yank 2 lines',
        'yw': 'yank word',
        'y$': 'yank to end of line',
        'p': 'put (paste) the clipboard after cursor',
        'P': 'put (paste) before cursor',
        'dd': 'delete (cut) a line',
        'dw': 'delete (cut) the current word',
        'x': 'delete (cut) current character',
    },
    {
        ## exiting
        ':w': 'write (save) the file, but don\'t exit',
        ':wq': 'write (save) and quit',
        ':q': 'quit (fails if anything has changed)',
        ':q!': 'quit and throw away changes',
    },
    {
        # search/replace
        '/': 'search for pattern',
        '?': 'search backward for pattern',
        'n': 'repeat search in same direction',
        'N': 'repeat search in opposite direction',
    },
    {
        # working with multiple files
        ':e filename': 'Edit a file in a new buffer',
        ':bn': 'go to next buffer',
        ':bp': 'go to previous buffer',
        ':bd': 'delete a buffer (close a file)',
        ':sp': 'Open a file in a new buffer and split window'
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
    if x == SHORTCUT_ESC:
        print('you pressed ESC')
    else:
        print('You pressed {}'.format(x))

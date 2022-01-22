#!/usr/bin/env python
import signal
import sys
from blessed import Terminal
import engine
import time 

def signal_handler(sig, frame):
    engine.on_exit()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

term = Terminal()


def main():
    engine.render()
    
    while True:
        with term.cbreak():
            inp = term.inkey()
        engine.route_command(inp)

    # print(term.home + term.clear + term.move_y(term.height // 2))
    # print(term.black_on_darkkhaki(term.center('press any key to continue.')))

    # with term.cbreak(), term.hidden_cursor():
    #     inp = term.inkey()

    # print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))


with term.hidden_cursor():
    main()

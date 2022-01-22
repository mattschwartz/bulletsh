import sys
from blessed import Terminal
from color_scheme import *
from tools import help_tool, browse_years

term = Terminal()

TITLE = 'bulletsh v0.1'


def render():
    reset_color()
    print(term.home +
          term.color_rgb(*COLOR_FG) +
          term.on_color_rgb(*COLOR_BG) +
          term.clear)

    print_curr_tool()
    print_title()


def print_title():
    with term.location(term.width - len(TITLE) - 1, term.height - 2):
        print(term.color_rgb(*COLOR_PRIMARY) + TITLE)


def print_curr_tool():
    with term.location(0, term.height - 2):
        print('press h for commands')


def route_command(ch):
    if ch == 'h':
        with term.fullscreen(), term.hidden_cursor():
            help_tool.on_tool_enable()
    elif ch == 'Y':
        with term.fullscreen(), term.hidden_cursor():
            browse_years.on_tool_enable()
    elif ch == 'q':
        on_exit()
        sys.exit(0)
    else:
        print('You pressed: ' + repr(ch))


def on_exit():
    print(term.home +
          term.clear +
          'Goodbye!')


def reset_color():
    print(term.color_rgb(*COLOR_FG) + term.on_color_rgb(*COLOR_BG))

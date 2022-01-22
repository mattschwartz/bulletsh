import sys
from blessed import Terminal
from color_scheme import *
from tools import help_tool, browse_years, page_viewer

term = Terminal()

TITLE = 'jacket v0.1'


def start():
    with term.hidden_cursor():
        while True:
            render()
            with term.cbreak():
                inp = term.inkey()
            if route_command(inp) == -1:
                stop_engine()
                break


def render():
    reset_color()
    print(term.home +
          term.color_rgb(*COLOR_FG) +
          term.on_color_rgb(*COLOR_BG) +
          term.clear)

    print_curr_tool()
    print_title()


def print_title():
    with term.location(term.width - len(TITLE) - 1, term.height - 1):
        print(term.color_rgb(*COLOR_PRIMARY) + TITLE + term.move_up)


def print_curr_tool():
    with term.location(0, term.height - 1):
        print('press h for commands' + term.move_up)


def route_command(ch):
    if ch == 'h':
        with term.fullscreen(), term.hidden_cursor():
            res = help_tool.on_tool_enable()
            if res != 'q':
                return route_command(res)
    elif ch == 'Y':
        with term.fullscreen(), term.hidden_cursor():
            browse_years.on_tool_enable()
    elif ch == 'q':
        return -1
    elif ch == 'd':
        with term.fullscreen(), term.hidden_cursor():
            page_viewer.on_render()
    else:
        print('You pressed: ' + repr(ch))


def stop_engine():
    print(term.home +
          term.clear +
          'Goodbye!')


def reset_color():
    print(term.color_rgb(*COLOR_FG) + term.on_color_rgb(*COLOR_BG))

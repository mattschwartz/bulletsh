import itertools
from blessed import Terminal

from color_scheme import TERM_COLOR_PRIMARY, TERM_COLOR_SECONDARY

term = Terminal()


def on_render():
    print(term.move_xy(0, 0) + term.clear +
          term.color_rgb(80, 80, 80) + term.move_up)

    print_title(' Jan 20 ')
    print('║ [x] Do nothing all day')
    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('╚' + '═' * (term.width - 2) + '╝' + term.move_down)

    print_title(' Jan 21 ')
    print('║ [x] Come up with better name')
    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('║ [x] Set up git repo')

    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('║ [-] Go to sleep')

    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('║ [ ] Finish project')

    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('╚' + '═' * (term.width - 2) + '╝')

    print(TERM_COLOR_PRIMARY)
    print_title(' Jan 22 ')
    print('║ [ ] Keep writing python')

    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('║ [ ] Figure out how tf to do this shit')

    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')
    print('╚' + '═' * (term.width - 2) + '╝')

    print_help()

    with term.cbreak():
        return term.inkey()


def print_title(str):
    print(term.move_up + '╔' + '═' * (term.width-2) + '╗')

    (y, x) = term.get_location()

    x = (term.width - len(str)) // 2
    with term.location(x, y-1):
        print(str)


def print_help():
    with term.location(0, term.height - 1):
        print('<↑>: prev day\t<↓>: next day\t<e>: edit day\t<t>: edit today\t<r>: return home' + term.move_up)

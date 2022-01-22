import itertools
from blessed import Terminal

from color_scheme import TERM_COLOR_PRIMARY, TERM_COLOR_SECONDARY

term = Terminal()


def on_render():
    sep = '╚' + '═' * (term.width - 2) + '╝' + term.move_down + term.move_x(0)
    
    view = term.move_xy(0, 0) + term.clear + \
        term.color_rgb(80, 80, 80) + term.move_up
    view += print_title(' Jan 20 ')

    view += term.move_x(0)
    view += '║ [x] Do nothing all day\n'
    view += sep

    view += print_title(' Jan 21 ')
    view += term.move_x(0)
    view += '║ [x] Come up with better name\n║ [x] Set up git repo\n║ [-] Go to sleep\n║ [ ] Finish project\n'
    view += sep

    view += TERM_COLOR_PRIMARY
    view += print_title(' Jan 22 ')
    view += term.move_x(0)
    view += '║ [ ] Keep writing python\n║ [ ] Figure out how tf to do this shit\n'
    view += sep
    
    view += print_help()

    print(view, end='')

    with term.cbreak():
        return term.inkey()


def print_border():
    (y, x) = term.get_location()
    with term.location(term.width - 1, y - 1):
        print('║')


def print_title(str):
    res = '╔' + '═' * (term.width - 2) + '╗'
    x = (term.width - len(str)) // 2
    return res + term.move_x(x) + str + term.move_down


def print_help():
    return term.move_xy(0, term.height - 1) + '<↑>: prev day\t<↓>: next day\t<e>: edit day\t<t>: edit today\t<r>: return home'

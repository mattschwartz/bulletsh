import utils
from blessed import Terminal
from data_manager import DataAccessor

term = Terminal()
data_accessor = DataAccessor()

def on_render():
    view = term.home + term.clear
    view += utils.print_title(term, ' Select a year ')
    view += print_years()
    
    print(view, end='')


def print_years():
    result = '' 
    pages_by_year = data_accessor.get_data().pages_by_year
    for year in pages_by_year.keys():
        result += utils.print_framed_line(term, f' {year} ({len(pages_by_year[year])})')
    return result 

def on_enabled():
    selection_choice = 0

    on_render()
    print_choice_marker(selection_choice, '>')

    while True:
        with term.cbreak():
            inp = term.inkey()

        print_choice_marker(selection_choice, ' ')

        if (inp == 'q'):
            break
        elif (inp.is_sequence and inp.code == term.KEY_DOWN):
            selection_choice = (selection_choice + 1) % 3
        elif (inp.is_sequence and inp.code == term.KEY_UP):
            selection_choice = (selection_choice - 1) % 3


        print_choice_marker(selection_choice, '>')


def print_choice_marker(i, ch):
    y_offs = 1
    with term.location(1, i + y_offs):
        print(ch)


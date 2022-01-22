from blessed import Terminal

term = Terminal()


def on_tool_enable():
    print(term.home + term.clear)
    selection_choice = 0

    while True:
        with term.location(0, 0):
            print('Select a year')
            
        print_years()
        print_choice_marker(selection_choice)

        with term.cbreak():
            inp = term.inkey()

        if (inp == 'q'):
            break
        elif (inp.is_sequence and inp.code == term.KEY_DOWN):
            selection_choice = (selection_choice + 1) % 3
        elif (inp.is_sequence and inp.code == term.KEY_UP):
            selection_choice = (selection_choice - 1) % 3


def print_choice_marker(i):
    y_offs = 1
    with term.location(0, i + y_offs):
        print('>')


def print_years():
    y_offs = 1
    with term.location(0, y_offs):
        print(' 2020\n 2021\n 2022')

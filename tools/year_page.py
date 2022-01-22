from blessed import Terminal

term = Terminal()

def on_tool_enable(year):
    print(term.move_xy(0, 0), 'Pages for year ' + year)
    print(' Jan 01\n Jan 02\n Jan 03\n Jan 04')

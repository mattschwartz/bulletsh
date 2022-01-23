from blessed import Terminal


def print_title(term: Terminal, text: str):
    res = '╔' + '═' * (term.width - 2) + '╗'
    x = (term.width - len(text)) // 2
    return (res + 
            term.move_x(x) + 
            text + 
            term.move_down + 
            term.move_x(0))


FRAME_BAR_HORIZONTAL = '║'


def print_framed_line(term: Terminal, text: str):
    return (FRAME_BAR_HORIZONTAL +
            text +
            term.move_x(term.width - 1) +
            FRAME_BAR_HORIZONTAL)


def print_frame_bottom(term: Terminal):
    return ('╚' + '═' * (term.width - 2) +
            '╝' + term.move_down + term.move_x(0))

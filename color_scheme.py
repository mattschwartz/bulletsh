from blessed import Terminal

term = Terminal()

COLOR_PRIMARY = (200, 75, 49)
COLOR_SECONDARY = (45, 66, 99)
COLOR_FG = (236, 219, 186)
COLOR_BG = (25, 25, 25)

TERM_COLOR_PRIMARY = term.color_rgb(*COLOR_PRIMARY)
TERM_COLOR_SECONDARY = term.color_rgb(*COLOR_SECONDARY)
TERM_COLOR_FG = term.color_rgb(*COLOR_FG)
TERM_COLOR_BG = term.on_color_rgb(*COLOR_BG)

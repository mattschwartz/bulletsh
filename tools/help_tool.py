from tools.tool_mapping import TOOLS_BY_COMMAND
import utils
from blessed import Terminal
from color_scheme import TERM_COLOR_FG

term = Terminal()


def on_enabled():
    view = term.home + term.clear + TERM_COLOR_FG
    view += utils.print_title(term, ' Help Menu ')

    for tool in TOOLS_BY_COMMAND.values():
        view += utils.print_framed_line(term,
                                        f' <{tool.command}>: {tool.description}')

    view += utils.print_frame_bottom(term)

    print(view, end='')

    with term.cbreak():
        return term.inkey()

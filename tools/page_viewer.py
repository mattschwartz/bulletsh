import utils
from datetime import date
from enum import Enum
from blessed import Terminal
from color_scheme import TERM_COLOR_FG, TERM_COLOR_SECONDARY
from data_manager import (DataAccessor,
                          JacketData,
                          TaskType)

term = Terminal()
data_accessor = DataAccessor()

EOL_BAR = term.move_x(term.width - 1) + '║\n'


def on_enabled():
    view = term.move_xy(0, 0) + term.clear
    view += render_days(data_accessor.get_data())

    view += print_help()

    print(view, end='')

    with term.cbreak():
        return term.inkey()


def render_days(data: JacketData):
    res = ''
    today_date = date.today()

    for page in data.sorted_pages():
        title = f' {page.date_str()} '

        is_current_day = today_date == page.date
        if is_current_day:
            res += TERM_COLOR_FG
        else:
            res += term.color_rgb(80, 80, 80)

        res += utils.print_title(term, title) + term.move_x(0)

        for task in page.tasks:
            if task.task_type == TaskType.TASK:
                if task.is_completed:
                    type_text = '║ × '
                elif is_current_day:
                    type_text = '║ ∘ '
                else:
                    type_text = '║ > '

            if task.task_type == TaskType.NOTE:
                type_text = '║ ─ '

            if task.is_cancelled:
                res += ('║ ' +
                        term.color_rgb(50, 50, 50) +
                        '× ' +
                        task.text +
                        term.color_rgb(80, 80, 80) +
                        EOL_BAR)
            else:
                res += type_text + task.text + EOL_BAR

        res += utils.print_frame_bottom(term)

    return res


def print_help():
    return (term.move_xy(0, term.height - 1) +
            TERM_COLOR_SECONDARY +
            '<↑>: prev day\t<↓>: next day\t<e>: edit day\t<t>: edit today\t<r>: return home')

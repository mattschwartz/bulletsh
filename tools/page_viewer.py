from datetime import date
from enum import Enum
from blessed import Terminal
from color_scheme import TERM_COLOR_FG, TERM_COLOR_PRIMARY, TERM_COLOR_SECONDARY
import data_manager

term = Terminal()

EOL_BAR = term.move_x(term.width - 1) + '║\n'


class TaskType(Enum):
    TASK = 'task'
    NOTE = 'note'
    CANCELLED = 'cancelled'


def on_render():
    data = data_manager.get_data()
    view = term.move_xy(0, 0) + term.clear
    view += render_days(data)

    view += print_help()

    print(view, end='')

    with term.cbreak():
        return term.inkey()


def print_title(str):
    res = '╔' + '═' * (term.width - 2) + '╗'
    x = (term.width - len(str)) // 2
    return res + term.move_x(x) + str + term.move_down


def render_days(data):
    day_separator = '╚' + '═' * (term.width - 2) + \
        '╝' + term.move_down + term.move_x(0)
    res = ''
    data["days"].reverse()
    today_date = date.today()

    for day in data["days"]:
        page_date = date.fromisoformat(day["date"])
        title = f' {page_date.strftime("%a %d %b")} '

        is_current_day = today_date == page_date
        if is_current_day:
            res += TERM_COLOR_FG
        else:
            res += term.color_rgb(80, 80, 80)

        res += print_title(title) + term.move_x(0)

        for task in day["tasks"]:
            task_type = task["type"]
            if task_type == TaskType.TASK.value:
                if task["isCompleted"]:
                    type_text = '║ × '
                elif is_current_day:
                    type_text = '║ ∘ '
                else:
                    type_text = '║ > '

            if task_type == TaskType.NOTE.value:
                type_text = '║ ─ '

            if (task_type == TaskType.CANCELLED.value):
                res += ('║ ' +
                        term.color_rgb(50, 50, 50) +
                        '× ' +
                        task["text"] +
                        term.color_rgb(80, 80, 80) +
                        EOL_BAR)
                # res += (term.on_color_rgb(72, 24, 24) +
                #         term.underline +
                #         task["text"] +
                #         engine.reset_on_color() +
                #         term.no_underline +
                #         EOL_BAR)
            else:
                res += type_text + task["text"] + EOL_BAR

        res += day_separator

    return res


def print_help():
    return (term.move_xy(0, term.height - 1) +
            TERM_COLOR_SECONDARY +
            '<↑>: prev day\t<↓>: next day\t<e>: edit day\t<t>: edit today\t<r>: return home')

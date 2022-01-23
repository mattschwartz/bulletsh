from dataclasses import dataclass
from typing import List
from color_scheme import COLOR_PRIMARY, TERM_COLOR_BG, TERM_COLOR_FG, TERM_COLOR_FG_LIGHT, TERM_COLOR_PRIMARY, TERM_COLOR_SECONDARY
import utils
from blessed import Terminal
from data_manager import DataAccessor, JacketData


@dataclass
class PanelTabItem:
    text: str
    is_selected: bool


@dataclass
class PanelTab:
    title: str
    is_selected: bool
    items: List[PanelTabItem]


class PageBrowserTool:

    term = Terminal()
    data_accessor = DataAccessor()
    selected_line = 0
    panel_tabs: List[PanelTab]

    def on_enabled(self):
        self.panel_tabs = [
            PanelTab(
                'years',
                True,
                (PanelTabItem('2021', True),
                 PanelTabItem('2022', False))
            ),
            PanelTab(
                'months',
                False,
                (PanelTabItem('Jan', False),
                 PanelTabItem('Feb', True))
            ),
            PanelTab(
                'days',
                False,
                (PanelTabItem('Wed Jan 19', False),
                 PanelTabItem('Thu Jan 20', False),
                 PanelTabItem('Fri Jan 21', True),
                 PanelTabItem('Sat Jan 22', False))
            )
        ]

        self.selected_line = 0
        while True:
            self.render_panel()

            with self.term.cbreak():
                inp = self.term.inkey()

            if (inp == 'q'):
                break
            elif inp.is_sequence and inp.code == self.term.KEY_TAB:
                self.panel_tabs[self.selected_line].is_selected = False
                self.selected_line = (self.selected_line + 1) % 3
                self.panel_tabs[self.selected_line].is_selected = True
            elif inp.is_sequence and inp.code == self.term.KEY_BTAB:
                self.panel_tabs[self.selected_line].is_selected = False
                self.selected_line = (self.selected_line - 1) % 3
                self.panel_tabs[self.selected_line].is_selected = True

    def render_panel(self):
        view = self.term.home + self.term.clear + TERM_COLOR_SECONDARY
        view += utils.print_title(self.term, ' Page Browser ')

        view += TERM_COLOR_FG
        view += self.print_tabbed_frames(self.panel_tabs,
                                         self.term.width - 2,
                                         self.term.height - 3,
                                         2)
        view += TERM_COLOR_SECONDARY
        for y in range(1, self.term.height - 1):
            view += (self.term.move_xy(0, y) +
                     utils.FRAME_BAR_HORIZONTAL +
                     self.term.move_xy(self.term.width - 1, y) +
                     utils.FRAME_BAR_HORIZONTAL)

        view += (self.term.move_xy(0, self.term.height - 3) +
                 '╠' +
                 '═' * (self.term.width - 2) +
                 '╣')

        view += (self.term.move_xy(0, self.term.height - 1) +
                 '╚' +
                 '═' * (self.term.width - 2) +
                 '╝')

        view += (TERM_COLOR_SECONDARY +
                 self.term.move_y(self.term.height - 2) +
                 utils.center_string(self.term, self.term.width,
                                    '<TAB>: switch panel select right    <BTAB>: switch panel select left    <q>: return to main',
                                    1))

        print(view, end='')

    def print_tabbed_frames(self,
                            tabs: List[PanelTab],
                            panel_width: int,
                            panel_height: int,
                            x_start: int):
        tab_width = panel_width // len(tabs)

        # Render tab title bar
        result = (self.term.move_x(x_start) +
                  self.term.move_down +
                  '│' +
                  self.term.move_up)

        x_offs = x_start
        for tab in tabs:
            far_right_x = x_offs + tab_width
            if (far_right_x + 2) >= panel_width:
                far_right_x = panel_width

            result += (self.term.move_x(x_offs) +
                       '─' * (far_right_x - x_offs - 1) +
                       '┬' +
                       self.term.move_down)

            if tab.is_selected:
                result += (self.term.bold +
                           utils.center_string(self.term, tab_width, f'{tab.title.upper()}', x_offs) +
                           self.term.normal +
                           TERM_COLOR_FG +
                           TERM_COLOR_BG)
            else:
                result += (TERM_COLOR_FG_LIGHT +
                           utils.center_string(self.term, tab_width, tab.title, x_offs) +
                           TERM_COLOR_FG)
            result += (self.term.move_x(far_right_x - 1) +
                       '│' +
                       self.term.move_down)

            result += (self.term.move_x(x_offs) +
                       '─' * (far_right_x - x_offs - 1) +
                       '┼' +
                       self.term.move_up(2))
            x_offs += tab_width

        # render border top corners
        result += (self.term.move_x(x_start) +
                   '┌' +
                   self.term.move_x(panel_width - 1) +
                   '┐')

        # render bottom border corners
        result += (self.term.move_x(x_start) +
                   self.term.move_down(2) +
                   '├' +
                   self.term.move_x(panel_width - 1) +
                   '┤\n')

        # Render tab content
        x_offs = x_start
        for tab in tabs:
            far_right_x = x_offs + tab_width
            if (far_right_x + 2) >= panel_width:
                far_right_x = panel_width

            for item in tab.items:
                if tab.is_selected:
                    if item.is_selected:
                        result += utils.center_string(self.term, tab_width,
                                                     f'> {item.text} <', x_offs)
                    else:
                        result += utils.center_string(self.term, tab_width,
                                                     item.text, x_offs)
                else:
                    result += (TERM_COLOR_FG_LIGHT +
                               utils.center_string(self.term, tab_width, item.text, x_offs) +
                               TERM_COLOR_FG)
                result += self.term.move_down
            result += self.term.move_up(len(tab.items))
            x_offs += tab_width

        tab_separator = ''
        x_offs = x_start
        for _ in tabs:
            far_right_x = x_offs + tab_width
            if (far_right_x + 2) >= panel_width:
                far_right_x = panel_width
            tab_separator += (self.term.move_x(x_offs) +
                              '' +
                              self.term.move_x(far_right_x - 1) +
                              '│')
            x_offs += tab_width

        result += (self.term.move_xy(x_start, panel_height - 1) +
                   '─' * (panel_width - x_start))

        for y in range(4, panel_height):
            result += (self.term.move_xy(x_start, y) +
                       '│' +
                       tab_separator)
        result += tab_separator.replace('│', '┴')

        # bottom bottom border
        result += (self.term.move_xy(x_start, panel_height - 1) +
                   '└' +
                   self.term.move_x(panel_width - 1) +
                   '┘')

        return result

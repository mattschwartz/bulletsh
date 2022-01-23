from dataclasses import dataclass
from tools import page_viewer, help_tool
from tools.page_browser import PageBrowserTool

@dataclass
class ToolDefinition:
    command: str
    description: str
    run = None

TOOLS_BY_COMMAND = {
    'h': ToolDefinition('h', 'displays info about available tools'),
    'q': ToolDefinition('q', 'exits the current tool or quits the program'),
    'b': ToolDefinition('b', 'view all pages'),
    'd': ToolDefinition('d', 'view latest pages')
}

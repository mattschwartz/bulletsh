from blessed import Terminal

term = Terminal()


def on_tool_enable():
    print(term.home + term.clear +
            '<h>: runs this tool\n' +
            '<q>: Exits the current tool\n' +
            '<d>: view day page\n' +
            '<m>: view month page\n' +
            '<y>: view year page\n' +
            '<Y>: browse years')
    with term.cbreak(), term.hidden_cursor():
        term.inkey()

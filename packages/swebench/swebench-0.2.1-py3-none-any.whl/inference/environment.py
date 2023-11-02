import json
import os
import subprocess
import sys
from pathlib import Path


    # <notes command>
    # The notes command tracks your notes. It supports the following commands:
    # notes append "This is an example note.
    # It spans multiple lines.
    # ---" - appends the given note to the notes. Notes are terminated by "---" on a line by itself.
    # notes erase - erases the notes
    # notes remove <n> - removes the nth line from the notes
    # </notes command>

EXAMPLE_ISSUE = """SkyCoord in Table breaks aggregate on group_by
### Description, actual behaviour, reproduction
When putting a column of `SkyCoord`s in a `Table`, `aggregate` does not work on `group_by().groups`:

```python
from astropy.table import Table
import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np

ras = [10, 20] * u.deg
decs = [32, -2] * u.deg

str_col = ['foo', 'bar']
coords = SkyCoord(ra=ras, dec=decs)

table = Table([str_col, coords], names=['col1', 'col2'])
table.group_by('col1').groups.aggregate(np.mean)
```

 fails with

```
Traceback (most recent call last):
  File "repro.py", line 13, in <module>
    table.group_by('col1').groups.aggregate(np.mean)
  File "astropy/table/groups.py", line 357, in aggregate
    new_col = col.groups.aggregate(func)
  File "astropy/coordinates/sky_coordinate.py", line 835, in __getattr__
    raise AttributeError("'{}' object has no attribute '{}'"
AttributeError: 'SkyCoord' object has no attribute 'groups'
```
This happens irregardless of the aggregation function.

### Expected behavior
Aggregation works, only fails to aggregate columns where operation does not make sense.


### System Details
```
Linux-5.14.11-arch1-1-x86_64-with-glibc2.33
Python 3.9.7 (default, Aug 31 2021, 13:28:12)
[GCC 11.1.0]
Numpy 1.21.2
astropy 5.0.dev945+g7dfa1edb2
(no scipy or matplotlib)
```
and
```
Linux-5.14.11-arch1-1-x86_64-with-glibc2.33
Python 3.9.7 (default, Aug 31 2021, 13:28:12)
[GCC 11.1.0]
Numpy 1.21.2
astropy 4.3.1
Scipy 1.7.1
Matplotlib 3.4.3
```"""


f"""<INSTRUCTIONS>
    You are an autonomous programmer, and you're working directly in the command line with a special interface.
    We're currently solving the following issue within our repository. Here's the issue text:
    <issue>
    {issue}
    </issue>

    The special interface consists of a file editor that shows you {window} lines of a file at a time.
    In addition to typical bash commands, you can also use the following commands to help you navigate and edit files.
    COMMANDS
    open <path> - opens the file at the given path in the editor
    scroll_up - moves the window up {window} lines
    scroll_down - moves the window down {window} lines
    goto <n> - moves the window to centered on line n
    search <string> - searches for the given (case sensitive) string in the open file
    search_all <string> - searches for the given (case sensitive) string in all files in the current working directory
    next - moves to the next search result
    prev - moves to the previous search result
    edit <n>:<m>
    <replacement text>
    END_OF_EDIT - replaces lines [n,m) with the given text in the open file. The replacement text is terminated by a line with only END_OF_EDIT on it.

    Your shell prompt is formatted as follows:
    (Open file: <path>) <cwd> $

    You're free to use any other bash commands you want e.g. find, grep, cat, ls, cd, etc.
    </INSTRUCTIONS>
    """


def get_instructions(issue):
    return f"""<INSTRUCTIONS>
    You are a genius programmer, and you're programming in the given interface that includes an editor,
    a terminal, and a scratchpad that you can use to summarize your ideas, plans, and changes so far.
    We're currently solving the following issue within our repository. Here's the issue text:
    <issue>
    {issue}
    </issue>

    In addition to general bash commands, you can also use the following commands.
    <fileviewer command>
    The fileviewer is your interface to the files in the repository. It shows 40 lines at a time.
    fileviewer supports the following commands:
    open file <path> - opens the file at the given path
    scroll up - moves the window up 40 lines
    scroll down - moves the window down 40 lines
    move to line <n> - moves the window to line n
    </fileviewer command>

    <edit command>
    The edit command can be used to edit the file in the fileviewer. It has a simple format as follows:
    edit lines <n>:<m>
    this is the text that will replace lines n through m
    ---
    The above replaces lines n through m with the given text, followed by a --- on a line by itself.
    Here's an example of how you might use it to make multiple edits.
    edit lines 1:7
    def bresenham(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0 # add a comment

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1
    ---
    edit lines 19:26

        for x in range(dx + 1):
            yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
    ---
    </edit command>

    You're free to use any other bash commands you want e.g. find, grep, cat, ls, cd, etc.
    </INSTRUCTIONS>
    """


class FileViewer:
    def __init__(self, current_filepath=None):
        self.current_filepath = current_filepath
        self.current_file = None
        self.start_line = 0
        self.window = 40
        if current_filepath is not None:
            self.open_file(current_filepath)

    def get_view(self):
        content = self.current_file[self.start_line:self.start_line+self.window]
        return "\n".join(self.add_lines_list(content))

    def add_lines_list(self, content):
        content_with_lines = list()
        for ix, line in enumerate(content.split("\n"), start=self.start_line):
            content_with_lines.append(f"{ix} {line}")
        return content_with_lines

    def open_file(self, filepath):
        self.current_filepath = filepath
        self.current_file = Path(self.current_filepath).read_text() + '\n[END OF FILE]'
        self.update_fileviewer()

    def scroll_up(self):
        self.start_line = max(0, self.start_line - self.window)
        self.update_fileviewer()

    def scroll_down(self):
        self.start_line = min(len(self.current_file), self.start_line + self.window)
        self.update_fileviewer()

    def move_to_line(self, line):
        self.start_line = line
        self.update_fileviewer()

    def update_fileviewer(self):
        if self.current_file is not None:
            self.fileviewer = self.get_view()
        else:
            self.fileviewer = 'No file open.'
        self.fileviewer = f'<fileviewer at {self.root_dir}>\n{self.fileviewer}\n</fileviewer at {self.root_dir}>'
    
    def __repr__(self) -> str:
        return self.fileviewer


class Terminal:
    def __init__(self, cwd):
        self.cwd = cwd
        self.terminal = None

    def update_terminal(self):
        """get the last 40 lines of the terminal and append a new prompt"""
        if self.terminal is not None:
            self.terminal = self.terminal[-40:]
        else:
            self.terminal = f'{self.cwd}$ '
        self.terminal = f'<terminal>\n{self.terminal}\n</terminal>'

    def run_command(self, command):
        command = command.split(" ")
        if command[0] == 'cd':
            self.cwd = Path(self.cwd, command[1]).as_posix()
            self.update_terminal()
        else:
            try:
                output = subprocess.check_output(command, cwd=self.cwd)
                self.terminal += f'{output}\n'
                self.update_terminal()
            except subprocess.CalledProcessError as e:
                self.terminal += f'{e.output}\n'
                self.update_terminal()
    
    def __repr__(self) -> str:
        return self.terminal
    

# class Notes:
#     def __init__(self):
#         self.notes = None

#     def update_notes(self):
#         if self.notes is not None:
#             self.notes = self.notes[-40:]
#         else:
#             self.notes = ''
#         self.notes = f'<notes>\n{self.notes}\n</notes>'

#     def append(self, note):
#         self.notes += f'{note}\n'
#         self.update_notes()

#     def erase(self):
#         self.notes = ''
#         self.update_notes()

#     def remove(self, line):
#         self.notes = '\n'.join(self.notes.split("\n")[:line] + self.notes.split("\n")[line+1:])
#         self.update_notes()
    
#     def __repr__(self) -> str:
#         return self.notes


def edit(filename, start_line, end_line, replacement):
    new_file = Path(filename).read_text().split("\n")
    new_file[start_line:end_line] = replacement.split("\n")
    Path(filename).write_text("\n".join(new_file))


class SweEnvironment:
    def __init__(self, root_dir, cwd, instance):
        issue_text = instance['problem_statement']
        self.root_dir = root_dir
        self.instructions = get_instructions(issue_text)
        self.cwd = Path(cwd).relative_to(root_dir).as_posix()
        self.fileviewer = FileViewer()
        self.terminal = Terminal(self.cwd)

    def add_lines_list(self, content):
        content_with_lines = list()
        for ix, line in enumerate(content.split("\n"), start=self.start_line):
            content_with_lines.append(f"{ix} {line}")
        return content_with_lines

    def observe(self):
        prompt = '\n'.join([self.instructions, self.fileviewer, self.terminal])
        return prompt

    def step(self, response):
        cmds = list()
        for line in response.split("\n"):
            if line.startswith('open file'):
                pass
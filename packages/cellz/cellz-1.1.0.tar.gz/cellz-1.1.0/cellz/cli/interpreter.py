import cmd
import sys
import os
import traceback
from collections import OrderedDict


def parse_blocks(file_content):
    blocks = OrderedDict()
    current_block = "top"
    block_lines = []
    for line in file_content:
        if line.startswith("#%%"):
            if block_lines:
                blocks[current_block.replace(" ", "_")] = "".join(block_lines)
                block_lines = []
            current_block = line.strip().lstrip("#%%").strip()
        else:
            block_lines.append(line)
    if block_lines:
        blocks[current_block] = "".join(block_lines)

    return blocks


def read_file(file_path):
    return open(file_path).readlines()


def run_block(block_code, file_path, variables):
    exec(compile(block_code, file_path, "exec"), variables)


def read_parse_file(file_path):
    file_content = read_file(file_path)
    cells = parse_blocks(file_content)
    return cells


def parse_args(arg):
    "Convert a series of zero or more inputs to an argument tuple"
    return tuple(map(str, arg.split(" ")))


def error_exc():
    exc_info = sys.exc_info()[:2]
    msg = traceback.format_exception_only(*exc_info)[-1].strip()
    print("***", msg)


class CellShell(cmd.Cmd):
    intro = "Welcome to the cell shell.   Type help or ? to list commands.\n"
    prompt = "(cellz)> "

    def __init__(self, filename):
        super().__init__()
        sys.path.append(os.getcwd())
        self.file = filename
        self.shell_vars = {}

    def do_example(self, arg):
        """The cell shell is interactive, so you can continue to develop your code while running the shell. 
        To add a cell, use the token '#%%' followed by a name for the cell. e.g. 

        #%% cell1
        def func(x):
            y = x**2
            return y
        #%% cell2
        f = 768
        print(func(4))
        #%% cell3
        print("hello")
        """
        pass

    def do_run(self, arg):
        "Run a cell, or sequence of cells, from the source file"
        args = parse_args(arg)
        cells = read_parse_file(self.file)
        for a in args:
            if a in cells.keys():
                try:
                    run_block(cells[a], self.file, self.shell_vars)
                except:
                    error_exc()
            else:
                print(f"{a} not in list of available cells, try one of {list(cells.keys())}")

    def do_exit(self, arg):
        "Exit the shell"
        return True

    def do_cells(self, arg):
        "Display all available cells"
        cells = read_parse_file(self.file)
        print(list(cells.keys()))

    def do_show(self, arg):
        "Display the contents of a particular cell"
        args = parse_args(arg)
        cells = read_parse_file(self.file)
        for a in args:
            if a in cells.keys():
                print(cells[a])
            else:
                print(f"{a} not in list of available cells, try one of {list(cells.keys())}")

    def do_print(self, arg):
        "Print the value of a variable or expression"
        try:
            val = eval(arg, self.shell_vars)
            print(repr(val))
        except:
            error_exc()

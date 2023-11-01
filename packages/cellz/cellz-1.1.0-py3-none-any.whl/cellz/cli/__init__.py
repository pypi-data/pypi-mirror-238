# SPDX-FileCopyrightText: 2023-present Henry Watkins <h.watkins@ucl.ac.uk>
#
# SPDX-License-Identifier: MIT
import click

from cellz.__about__ import __version__
from cellz.cli.interpreter import CellShell


@click.command(context_settings={"help_option_names": ["-h", "--help"]})  # , invoke_without_command=True)
@click.version_option(version=__version__, prog_name="cell")
@click.argument("file", type=click.Path(exists=True))
def cellz(file):
    """Run cell shell. 

    Cell is a python cell runner, allowing you to run python code separated into cells, similar 
    to jupyter or other interactive python notebooks. To create a cell, just add '#%%' followed
    by a name to identify the cell. e.g. 

    #%% cell1
    
    print('hello!')
    """
    CellShell(file).cmdloop()

from collections import OrderedDict
from pathlib import Path

import pytest

from cellz.cli.interpreter import *


def test_parse_blocks():
    # Create a temporary Python file for testing
    file_content = open(Path().cwd() / "tests" / "block_file.py").readlines()

    # Call the function to split the blocks
    result = parse_blocks(file_content)

    # Define the expected OrderedDict
    expected = OrderedDict(
        [
            ("top", 'print("default start block")\n\n\n'),
            ("Block_1", 'print("This is block 1")\n\n'),
            ("Block_2", 'print("This is block 2")\n\n'),
            ("Block_3", 'print("This is block 3")'),
        ]
    )

    # Check if the result matches the expected output
    assert result == expected

from textwrap import dedent
from sphinxcontrib.console.python import interpret_python

def test_interpret_python():
    header, output = interpret_python(['from math import e', 'e'])
    assert output == dedent(
        '''
        >>> from math import e
        >>> e
        2.718281828459045
        '''
    ).strip()

def test_for_loop():
    header, output = interpret_python(['for i in range(10):', '    print(i)'])

    assert output == dedent(
        '''
        >>> for i in range(10):
        ...     print(i)
        ...
        0
        1
        2
        3
        4
        5
        6
        7
        8
        9
        '''
    ).strip()

def test_exit():
    header, output = interpret_python(['1 + 1', 'exit()', '1 + 2'])

    assert output == dedent(
        '''
        >>> 1 + 1
        2
        >>> exit()
        '''
    ).strip()

def test_exit_in_for():
    header, output = interpret_python(['for i in range(10):', '    exit()'])

    assert output == dedent(
        '''
        >>> for i in range(10):
        ...     exit()
        ...
        '''
    ).strip()

def test_rich():
    header, output = interpret_python(
        [
            'from rich.console import Console',
            'console = Console()',
            'console.print({"name": "kinopico", "age": 233})'
        ]
    )

    assert output == '\n'.join(
        [
            '>>> from rich.console import Console',
            '>>> console = Console()',
            '>>> console.print({"name": "kinopico", "age": 233})',
            '\x1b[1m{\x1b[0m\x1b[32m\'name\'\x1b[0m: \x1b[32m\'kinopico\'\x1b[0m, \x1b[32m\'age\'\x1b[0m: \x1b[1;36m233\x1b[0m\x1b[1m}\x1b[0m'
        ]
    )

def test_sleep():
    header, output = interpret_python(
        [
            'from time import sleep',
            '1 + 3',
            'print(_)',
            '',
            'sleep(1)',
            'while True:',
            '    break',
        ]
    )

    assert output == dedent(
        '''
        >>> from time import sleep
        >>> 1 + 3
        4
        >>> print(_)
        4
        >>>
        >>> sleep(1)
        >>> while True:
        ...     break
        ...
        '''
    ).strip()

def test_timeout():
    header, output = interpret_python(
        lines=['from time import sleep', 'sleep(2)', 'print("hello, world")'],
        timeout=1,
    )
    assert output == dedent(
        '''
        >>> from time import sleep
        >>> sleep(2)
        '''
    ).strip()

def test_windows_size():
    header, output = interpret_python(lines=['from os import get_terminal_size', 'get_terminal_size()'], window_height=10, window_width=40)

    assert output == dedent(
        '''
        >>> from os import get_terminal_size
        >>> get_terminal_size()
        os.terminal_size(columns=40, lines=10)
        '''
    ).strip()

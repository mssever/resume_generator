import shutil
from textwrap import dedent, fill

def str_wrap(string, kind='normal'):
    cols, lines = shutil.get_terminal_size()
    if kind == 'help':
        # The width of argparse's left margin for help text, minus 1 for
        # scrollbar padding on Windows' cmd.exe.
        cols = max(cols-23-1, 10)
    return '\n\n'.join(fill(p, width=cols) for p in dedent(string).split('\n\n'))

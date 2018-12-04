import re
import shutil
from textwrap import dedent, wrap

def str_wrap(string, kind='normal'):
    cols, lines = shutil.get_terminal_size()
    if kind == 'help':
        # The width of argparse's left margin for help text, minus 1 for
        # scrollbar padding on Windows' cmd.exe.
        cols = max(cols-23-1, 10)
    out = []
    for paragraph in re.split(r'\r?\n\r?\n', dedent(string)):
        paragraph = re.sub(r'[\s]+', ' ', paragraph.strip())
        lines = wrap(paragraph, width=cols,
                     replace_whitespace=True, break_long_words=False)
        out.append('\n'.join(lines))
    out = '\n\n'.join(out)
    if kind == 'help':
        return out
    else:
        return out + '\n'

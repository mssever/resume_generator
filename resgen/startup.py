'''
Usage: {prog} mode [options]

For help on any of the modes, run `{prog} <mode> --help`.

Modes
=====
new         Create a new project or resume style.
generate    Generate a resume.
show        Show an example file to see the available documentation.

Global options
==============

-d/--project-dir    Specify a project directory. Default: the current directory.
-h/--help           Show a help message.
--version           Show the version number.
'''

import importlib
import sys

from resgen.config import get_config

def main():
    modes = ('new', 'generate', 'show')
    if len(sys.argv) > 1 and sys.argv[1] in modes:
        mode = sys.argv[1]
        del sys.argv[1]
        mod = importlib.import_module(f'resgen.mode.{mode}')
        return mod.run()
    elif '--version' in sys.argv:
        print(get_config().version_string)
        return 0
    elif '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__.format(prog=get_config().progname))
        return 0
    else:
        print(__doc__.format(prog=get_config().progname))
        return 1

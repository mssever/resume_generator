'''
Usage: {prog} mode [options]

For help on any of the modes, run `{prog} <mode> --help`.

Modes:

  new         Create a new project or résumé style.
  build       Generate a résumé.
  show        Show an example file to see the available documentation.

Global options

  -d/--project-dir    Specify a project directory. Default: the current directory.
  -h/--help           Show a help message.
  --version           Show the version number.
'''

import importlib
import os
import sys

from resgen.config import get_config

def main():
    config = get_config()
    config.progname = os.path.basename(sys.argv[0])
    with open(os.path.join(config.basedir, 'resgen', 'data', 'version.txt')) as f:
        config.version = f.read().strip()
    config.version_string = f'{config.progname} {config.version}'
    config.resume_part_ids = {}
    config.output_config_files = [os.path.join(config.basedir, 'resgen', 'data', 'config.yaml')]
    config.output = {}
    modes = ('new', 'build', 'show')
    if len(sys.argv) > 1 and sys.argv[1] in modes:
        mode = sys.argv[1]
        del sys.argv[1]
        mod = importlib.import_module(f'resgen.mode.{mode}')
        return mod.run()
    elif '--version' in sys.argv:
        print(get_config().version_string)
        exit(0)
    elif '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__.format(prog=config.progname))
        return 0
    else:
        sys.stderr.write(__doc__.format(prog=config.progname).rstrip() + '\n')
        return 1

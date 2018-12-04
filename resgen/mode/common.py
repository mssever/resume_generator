import argparse
import os

from resgen.config import get_config
from resgen.lib.collection import Collection
from resgen.util import str_wrap

def parse_common_args(parser):
    def directory(d):
        config = get_config()
        if os.path.sep not in d:
            d = os.path.join(os.path.curdir, d)
        if os.path.isdir(d):
            return d
        elif os.path.isfile(d) or os.path.islink(d):
            raise argparse.ArgumentTypeError('File given instead of directory')
        elif os.path.isdir(os.path.dirname(d)):
            return d
        else:
            raise argparse.ArgumentTypeError(f'Improper dirname: "{os.path.dirname(d)}"')
    
    def is_file(f):
        if os.path.sep not in f:
            f = os.path.join(os.path.curdir, f)
        if f is None:
            return f
        elif not os.path.isfile(f) and not os.path.islink(f):
            raise argparse.ArgumentTypeError(f"The specified config file ({f}) doesn't exist.")
        else:
            return f
    
    config = get_config()
    group = parser.add_argument_group(title="Common Options", description=str_wrap("These arguments apply to all modes.", kind='help'))
    add = group.add_argument
    pdir = str_wrap('Specify a project directory. Default: The current directory.', kind='help')
    recipe = str_wrap('Use this recipe instead of the default.', kind='help')
    resume = str_wrap('Use this resume instead of the default.', kind='help')
    ver = str_wrap('Show the version number and exit.', kind='help')
    hp = str_wrap('Show this help message and exit.', kind='help')
    cnf = str_wrap('Use this config file instead of the default.', kind='help')
    add('-d', '--project-dir', metavar='DIRECTORY', default=os.getcwd(), type=directory, help=pdir)
    add('-R', '--use-recipe', metavar="RECIPE", default=None, help=recipe)
    add('-E', '--use-resume', metavar="RESUME", default=None, help=resume)
    add('-c', '--use-config', metavar='PATH', type=is_file, default=None, help=cnf)
    add('--version', action='version', version=config.version_string, help=ver)
    add('-h', '--help', action='help', default=argparse.SUPPRESS, help=hp)
    args = Collection()
    config.args = args
    parser.parse_args(namespace=args)

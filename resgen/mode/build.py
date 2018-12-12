'''
Build one or more resumes from the configured source.
'''
import os

from .common import init_arg_parser, parse_common_args
from ..config import get_config
from ..util import str_wrap, show_config, check_if_project_directory
from ..lib.output.config import parse_output_config

def parse_args():
    parser, add = init_arg_parser(__doc__, 'Build Options', 'These options affect the build process.')
    html = 'Build an HTML resume.'
    nohtml = "Don't build an HTML resume."
    pdf = "Build a PDF resume."
    nopdf = "Don't build a pdf resume."
    overwrite = "Don't overwrite existing resume builds."
    add('-H', '--html', action='store_true', help=html)
    add('--no-html', action='store_true', help=nohtml)
    add('-P', '--pdf', action='store_true', help=pdf)
    add('--no-pdf', action='store_true', help=pdf)
    add('-o', '--no-overwrite', action='store_true', help=overwrite)
    parse_common_args(parser)

def run():
    parse_args()
    config = get_config()
    if (config.args.html and config.args.no_html) or (config.args.pdf and config.args.no_pdf):
        exit(str_wrap("ERROR: You can't both have and not have an output type!"))
    check_if_project_directory()
    initialize_config()
    print(config)
    return 0

def initialize_config():
    config = get_config()
    if config.args.use_config is None:
        #config.output_config_files.append(os.path.join(config.args.project_dir, 'config.yaml'))
        config.args.use_config = os.path.join(config.args.project_dir, 'config.yaml')
    config_file = parse_output_config(config.args.use_config)
    print(repr(config_file))

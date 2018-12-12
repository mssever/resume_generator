import os
import re
import shutil
from textwrap import dedent, wrap

from resgen.config import get_config

def str_wrap(string, kind='normal'):
    cols, lines = shutil.get_terminal_size()
    cols = min(cols, 100)
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
    out = '\n\n'.join(out).rstrip()
    if kind == 'help':
        return out + '\n\n'
    else:
        return out + '\n'

def check_if_project_directory(force=False):
    config = get_config()
    if not os.path.isdir(config.args.project_dir):
        exit(str_wrap(f'ERROR: The project directory "{config.args.project_dir}" doesn\'t exist.'))
    test = (
        'config.yaml',
        'default_resume.yaml',
        'default_recipe.yaml',
        'output'
    )
    if any(not os.path.exists(os.path.join(config.args.project_dir, i)) for i in test):
        if config.args.get('force', False):
            sys.stderr.write('--force: Bypassing safety check...\n')
        else:
            s = f'''
                The given directory ({config.args.project_dir}) doesn't appear 
                to be a project directory. Please either pass in a project 
                directory using -d/--project-dir or change your working 
                directory to a project directory.
                '''
            if force:
                s += '''
                To override this warning, use -f/--force. However, it's likely 
                that you will have problems if you do so.
                '''
            exit(str_wrap(s))

def show_config():
    return str(get_config())

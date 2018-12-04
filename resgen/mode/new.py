'''
This subcommand generates the files you will need to use the Resume Generator.
'''
import argparse
import inspect
import os
import shutil
import sys

from resgen.config import get_config
from .common import parse_common_args, init_arg_parser
from resgen.util import str_wrap, check_if_project_directory

def parse_args():
    parser, add = init_arg_parser(
        description=__doc__,
        group_title="New Options",
        group_description="You must specify one of: all, recipe, or resume.",
        usage="%(prog)s generate (all|recipe|resume) [options]"
    )
    new = '''
        all: Generate a new project. The project directory must either be empty 
        (although GIT files are permitted) or it must not exist, in which case 
        it will be created. The project directory is the current working 
        directory unless --project-dir is also given.

        recipe: Generates a new blank recipe.

        resume: Generates a new blank resume.
        '''
    name = """
        When generating a new recipe or resume, you need to give it a name using
        this option.
        """
    force = """
        Bypass safety checks and create project files anyway. This option may 
        be dangerous and should be used with care.
        """
    add('type', choices=['all', 'recipe', 'resume'], help=new)
    add('-n', '--name', default=None, help=name)
    add('-f', '--force', action='store_true', help=force)
    parse_common_args(parser)

def run():
    parse_args()
    config = get_config()
    
    # Calls a function named new_<type> and returns its return value.
    return getattr(inspect.getmodule(run), f'new_{config.args.type}')()

def new_all():
    config = get_config()
    dest = config.args.project_dir
    if os.path.isdir(dest):
        entries = [True for entry in os.listdir(dest) if not entry.startswith('.git')]
        if len(entries) > 0:
            if config.args.force:
                sys.stderr.write('--force: Bypassing safety check...\n')
            else:
                sys.stderr.write(str_wrap(f"""
                ERROR: The provided directory ({dest}) can't be used because it 
                isn't empty. The only files which can exist in a directory when 
                `{config.progname} new all` is run are git files.
                
                Use -d/--project_dir to give a different directory, which 
                doesn't have to exist already.
                
                Use -f/--force to use this directory anyway. However, doing so 
                might break things.
                """))
                return 6
    else:
        os.mkdir(dest)
    data_files = (
        'config.yaml',
        'default_resume.yaml',
        'default_recipe.yaml',
        #'resume_list.yaml',
        #'recipe_list.yaml'
    )
    try:
        for file_ in data_files:
            shutil.copy(os.path.join(config.basedir, 'resgen', 'data', file_), dest)
        os.mkdir(os.path.join(dest, 'output'))
    except OSError as e:
        exit(str_wrap(f'ERROR: An error occurred during this operation: {e}'))
    else:
        print(str_wrap(f'''
        A new project was created in `{dest}`. Here's a brief tour:
        
        * `default_resume.yaml` is your resume source. Put your complete resume in 
          this file, and set tags and priorities as appropriate to enable you to 
          generate different resumes as you wish. The comments in the file explain 
          the options. You can create additional resumes using `{config.progname} 
          new resume`, but you shouldn't do so unless absolutely necessary, as you 
          will have to build each resume separately and can't combine them.
        
        * `default_recipe.yaml` defines how to build your resume. For each resume
          variation, create a new recipe by running `{config.progname} new recipe -n recipe_name`.
        
        * `config.yaml` is where you configure your resume project. Look inside for 
          comments explaining the configuration options.
        
        * `output` is the directory where your generated resumes are saved. Feel 
          free to leave them there, symlink them to somewhere, or move them 
          elsewhere.
        '''))
        return 0

def _new_item(which):
    if which not in ('resume', 'recipe'):
        raise ArgumentError('Invalid value for which')
    config = get_config()
    if config.args.name is None:
        sys.stderr.write(str_wrap(
            f'ERROR: You must name your new {which} using the -n/--name option.'
        ))
        return 7
    check_if_project_directory(force=True)
    src = os.path.join(config.basedir, 'resgen', 'data', f'default_{which}.yaml')
    dest = os.path.join(config.args.project_dir, f'{config.args.name}_{which}.yaml')
    if os.path.exists(dest):
        sys.stderr.write(str_wrap(f'You already have a {which} named "{config.args.name}"!'))
        return 8
    try:
        shutil.copy(src, dest)
    except OSError as e:
        exit(str_wrap(f'ERROR: An error occurred while performing this operation: {e}'))
    return 0

def new_resume():
    return _new_item('resume')

def new_recipe():
    return _new_item('recipe')

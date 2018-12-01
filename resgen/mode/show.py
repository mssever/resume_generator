import os

from resgen.lib.yaml import YAML
from resgen.config import get_config

def run():
    print(f'Config\n======\n{show_config()}\n\n')
    config = get_config()
    with open(os.path.join(config.basedir, 'resgen', 'data', 'resume.yaml')) as f:
        print(f'Resume YAML\n===========\n{dump_yaml(f)}')
    return 0

def show_config():
    config = get_config()
    return '\n'.join(f'{k}: {repr(v)}' for k, v in config.keys())

def dump_yaml(doc):
    yaml = YAML()
    yaml.load(doc)
    return str(yaml)
    
    #Try: compact, dump, map, seq

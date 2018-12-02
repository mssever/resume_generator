import os

from resgen.lib.yaml import YAML
from resgen.config import get_config

def run():
    config = get_config()
    with open(os.path.join(config.basedir, 'resgen', 'data', 'resume.yaml')) as f:
        print(f'Resume YAML\n===========\n{dump_yaml(f)}')
    print(f'Config\n======\n{show_config()}\n\n')
    return 0

def show_config():
    config = get_config()
    return '\n'.join(f'{k}: {repr(v)}' for k, v in config.keys())

def dump_yaml(doc):
    yaml = YAML()
    yaml.load(doc)
    from resgen.lib.yaml_types import make_object
    config = get_config()
    out = []
    #out.append('\n\n'.join(repr(make_object(yaml[name], obj_name=name, id_register=config.resume_part_ids)) for name in yaml.names()))
    out.append('\n\n'.join(str(make_object(yaml[name], obj_name=name, id_register=config.resume_part_ids)) for name in yaml.names()))
    return '\n\n==============================================================\n\n'.join(out)

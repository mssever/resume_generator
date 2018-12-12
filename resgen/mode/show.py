import os

from resgen.lib.parserlib.parser import Parse_YAML
from resgen.config import get_config
from resgen.lib.output.config import parse_output_config
from resgen.util import show_config

def run():
    config = get_config()
    with open(os.path.join(config.basedir, 'resgen', 'data', 'default_resume.yaml')) as f:
        print(f'Resume YAML\n===========\n{dump_yaml(f)}')
    print(f'Config\n======\n{show_config()}\n\n')
    print('\n\n``````````````\n\n'.join([
        'resume_part_ids:\n' + str(sorted(config.resume_part_ids.keys())),
        'school_1:\n' + str(config.resume_part_ids['school_1']),
        'work:\n' + str(config.resume_part_ids['work']),
        'me:\n' + str(config.resume_part_ids['me']),
        'synopsis_title:\n' + str(config.resume_part_ids['synopsis_title']),
        'synopsis:\n' + str(config.resume_part_ids['synopsis']),
    ]))
    config.output = parse_output_config()
    print(repr(config.output))
    return 0

def dump_yaml(doc):
    yaml = Parse_YAML()
    yaml.load(doc)
    from resgen.lib.parserlib.factories import make_object
    config = get_config()
    out = []
    #out.append('\n\n'.join(repr(make_object(yaml[name], obj_name=name, id_register=config.resume_part_ids)) for name in yaml.names()))
    out.append('\n\n'.join(str(make_object(yaml[name], obj_name=name, id_register=config.resume_part_ids)) for name in yaml.names()))
    return '\n\n==============================================================\n\n'.join(out)

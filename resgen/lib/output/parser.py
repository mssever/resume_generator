from resgen.config import get_config
from resgen.lib.parserlib.parser import Parse_YAML

def parse_config(filename):
    config = get_config()
    yaml = Parse_YAML()
    with open(filename) as f:
        yaml.load(f)
    return yaml
    #config.output

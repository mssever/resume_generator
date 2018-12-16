from ..collection import Collection
from .parser import parse_config
from ...config import get_config

### FIXME: Doesn't yet properly do deep merges.
class OutputConfig(Collection):
    def __init__(self, *config_files):
        '''config_files: Ordered list of configuration files. Values specified
        later will override earlier items.'''
        Collection.__init__(self)
        for filename in config_files:
            config = parse_config(filename)
            for key, value in config.items():
                self.update_property(key, value)

def parse_output_config(files=None):
    #resgen.lib.output.parser.parse_config(get_config().output_config_file)
    config = get_config()
    if files is None:
        files = config.output_config_files
    print(files)
    #return OutputConfig(*files)

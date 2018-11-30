from resgen.config import get_config

def run():
    print(show_config())
    return 0

def show_config():
    config = get_config()
    return '\n'.join(f'{k}: {repr(v)}' for k, v in config.keys())

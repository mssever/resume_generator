from ruamel.yaml import YAML as upstream

class NotLoadedError(Exception):
    pass

class YAML(upstream):
    def __init__(self, *args, **kwargs):
        upstream.__init__(self, *args, **kwargs)
        self._data = None
    
    def load(self, *args, **kwargs):
        self._data = upstream.load(self, *args, **kwargs)
    
    def __iter__(self):
        return self._data
    
    #def __getattr__(self, attr):
    #    if self._data is not None and attr in self._data:
    #        return self._data[attr]
    #    else:
    #        return upstream.__getattr__(self, attr)
    def __getitem__(self, key):
        return self._data[key]
    
    def __repr__(self):
        return '<YAML Object>: Contents:\n' + repr(self._data)
    
    def items(self):
        if self._data is None:
            raise NotLoadedError("You must load data before calling this method.")
        return self._data.items()
    
    def names(self):
        return [i[0] for i in self.items()]

if __name__ == '__main__':
    # Debugging code
    import os
    with open(os.path.join('..','data','resume.yaml')) as f:
        y = YAML()
        y.load(f)
    print(y, end='\n\n\n\n')
    print(y['person'], end='\n============\n\n\n')
    print('\n------------\n'.join(str(i) for i in y.items()), end='\n==============\n\n\n\n\n')
    print(f'Names: {y.names()}', end='\n=============\n\n\n\n')

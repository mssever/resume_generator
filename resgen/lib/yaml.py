from ruamel.yaml import YAML as upstream

class NotLoadedError(Exception):
    pass

class YAML(upstream):
    def __init__(self, *args, **kwargs):
        upstream.__init__(self, *args, **kwargs)
        self.__data = None
    
    def load(self, *args, **kwargs):
        self.__data = upstream.load(self, *args, **kwargs)
    
    def __iter__(self):
        return self.__data
    
    #def __getattr__(self, attr):
    #    if self.__data is not None and attr in self.__data:
    #        return self.__data[attr]
    #    else:
    #        return upstream.__getattr__(self, attr)
    def __getitem__(self, key):
        return self.__data[key]
    
    def __repr__(self):
        return '<YAML Object>: Contents:\n' + repr(self.__data)
    
    def items(self):
        if self.__data is None:
            raise NotLoadedError("You must load data before calling this method.")
        return self.__data.items()
    
    def names(self):
        return [i[0] for i in self.items()]

if __name__ == '__main__':
    # Debugging code
    import os
    with open(os.path.join(os.path.dirname(__file__), '..','data','resume.yaml')) as f:
        y = YAML()
        y.load(f)
    print(y, end='\n\n\n\n')
    print(y['me'], end='\n============\n\n\n')
    print('\n------------\n'.join(str(i) for i in y.items()), end='\n==============\n\n\n\n\n')
    print(f'Names: {y.names()}', end='\n=============\n\n\n\n')
    print(y['synopsis_content'])

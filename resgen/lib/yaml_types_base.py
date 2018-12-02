import resgen.lib.yaml_types

def make_object(src, inherited_tags=None, inherited_priority=None, id_register=None, obj_name=None):
    '''Takes an ordereddict as returned by resgen.lib.yaml.YAML and makes an object of the correct type.'''
    out = {}
    if inherited_tags:
        out['inherited_tags'] = inherited_tags
    if inherited_priority:
        out['inherited_priority'] = inherited_priority
    if obj_name:
        out['obj_name'] = obj_name
    if id_register is not None:
        out['id_register'] = id_register
    for key, value in src.items():
        if key == 'type':
            cls = resgen.lib.yaml_types.types[value]
        else:
            if isinstance(value, str):
                value = value.strip()
            out[key] = value
    return cls(**out)

class YamlTypesBase:
    def __init__(self,**kwargs):
        '''
        id_register: If given, expects a dictionary-like object, to which will
                     be added a key containing the YAML type's id and a
                     reference to the object. If there is no id given, no key
                     will be added.
        '''
        keys = kwargs.keys()
        if 'tags' in keys:
            self.tags = list(kwargs['tags'])
        elif 'inherited_tags' in keys and kwargs['inherited_tags'] is not None:
            self.tags = kwargs['inherited_tags']
        else:
            self.tags = []
        if 'priority' in keys:
            self.priority = int(kwargs['priority'])
        elif 'inherited_priority' in keys and kwargs['inherited_priority'] is not None:
            self.priority = kwargs['inherited_priority']
        else:
            self.priority = 3
        if 'content' in keys: # and kwargs.get('set_content', True) is False:
            content = kwargs['content']
            if isinstance(content, dict) and 'type' in content.keys():
                self.content = make_object(content, self.tags, self.priority, kwargs.get('id_register', None))
            elif isinstance(content, list):
                cont = []
                for i in content:
                    if isinstance(i, dict) and 'type' in i.keys():
                        cont.append(make_object(i, self.tags, self.priority, kwargs.get('id_register', None)))
                    elif isinstance(i, str):
                        cont.append(make_object({'type': 'text', 'content': i}, self.tags, self.priority, kwargs.get('id_register', None)))
                    else:
                        cont.append(i)
                self.content = cont
            else:
                self.content = content
        else:
            self.content = None
        self.id = kwargs.get('id', None)
        #print(f'\tself.type = {type(self).__name__}\n\tself.content = {self.content}\nself.id = {self.id}')
        obj_name = kwargs.get('obj_name', None)
        #print(f'obj_name = {obj_name}')
        if self.id is None and obj_name is not None:
            self.id = obj_name
        #print(f'new self.id = {self.id}', end='\n~~~~~~~~~\n\n')
        self.id_register = kwargs.get('id_register', None)
        if not isinstance(self.id_register, dict) and self.id_register is not None:
            raise TypeError(f'Wrong type for id_register. Expected dict or None; got {repr(self.id_register)}.')
        if self.id_register is not None and 'id' in keys:
            if self.id in self.id_register.keys():
                raise ValueError(f'Duplicate IDs! The id "{self.id}" already exists. Current object: {repr(self)}')
            self.id_register[self.id] = self
        
    def __repr__(self):
        props = self._show_in_repr() + [
            ('tags', self.tags),
            ('priority', self.priority),
            ('id', self.id)
        ]
        if self.content:
            props += [('content', self.content)]
        #import pprint
        vals = ", ".join(f"{k}={repr(v)}" for k, v in props)
       # vals = pprint.pformat(vals, indent=4, width=72)
        return f'{type(self).__name__}({vals})'
    
    def __str__(self):
        content = self.content
        if content:
            return str(content)
        else:
            return repr(self)
    
    def _show_in_repr(self):
        return []

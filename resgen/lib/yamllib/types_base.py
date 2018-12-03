from .factories  import make_object

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
        self.id_ = kwargs.get('id', None)
        obj_name = kwargs.get('obj_name', None)
        if self.id_ is None and obj_name is not None:
            self.id_ = obj_name
        self.id_register = kwargs.get('id_register', None)
        if not isinstance(self.id_register, dict) and self.id_register is not None:
            raise TypeError(f'Wrong type for id_register. Expected dict or None; got {repr(self.id_register)}.')
        if self.id_register is not None and self.id_:
            if self.id_ in self.id_register.keys():
                raise ValueError(f'Duplicate IDs! The id "{self.id_}" already exists. Current object type: {type(self).__name__}')
            self.id_register[self.id_] = self
        
    def __repr__(self):
        props = self._show_in_repr() + [
            ('tags', self.tags),
            ('priority', self.priority),
            ('id_', self.id_)
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

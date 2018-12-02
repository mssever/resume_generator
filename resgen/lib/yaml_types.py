__all__ = ['make_object', 'Text', 'Person', 'H1', 'Multiple', 'Job', 'School', 'Org']

def make_object(src, inherited_tags=None, inherited_priority=None, obj_name=None):
    '''Takes an ordereddict as returned by resgen.lib.yaml.YAML and makes an object of the correct type.'''
    out = {}
    if inherited_tags:
        out['inherited_tags'] = inherited_tags
    if inherited_priority:
        out['inherited_priority'] = inherited_priority
    if obj_name:
        out['obj_name'] = obj_name
    for key, value in src.items():
        if key == 'type':
            cls = _types[value]
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
            self.priority = kwargs['priority']
        elif 'inherited_priority' in keys and kwargs['inherited_priority'] is not None:
            self.priority = kwargs['inherited_priority']
        else:
            self.priority = 3
        if 'content' in keys:
            content = kwargs['content']
            if isinstance(content, dict) and 'type' in content.keys():
                self.content = make_object(content, self.tags, self.priority)
            elif isinstance(content, list):
                cont = []
                for i in content:
                    if isinstance(i, dict) and 'type' in i.keys():
                        cont.append(make_object(i, self.tags, self.priority))
                    else:
                        cont.append(i)
                self.content = cont
            else:
                self.content = content
        else:
            self.content = None
        self.id = kwargs.get('id', None)
        obj_name = kwargs.get('obj_name', None)
        if self.id is None and obj_name is not None:
            self.id = obj_name
        reg = kwargs.get('id_register', None)
        if reg is not None and 'id' in keys:
            reg[self.id] = self
        
    def __repr__(self):
        props = self._show_in_repr() + [
            ('tags', self.tags),
            ('priority', self.priority),
            ('id', self.id)
        ]
        if self.content:
            props += [('content', self.content)]
        vals = ", ".join(f"{k}={repr(v)}" for k, v in props)
        return f'{type(self).__name__}({vals})'
    
    def __str__(self):
        content = self.content
        if content:
            return str(content)
        else:
            return repr(self)
    
    def _show_in_repr(self):
        return []

class Text(YamlTypesBase):
    pass
    #def __init__(self, **kwargs):
    #    YamlTypesBase.__init__(self, **kwargs)
    #    self.content = kwargs.get('content', '')
    #
    #def _show_in_repr(self):
    #    return [('content', self.content)]

class Person(YamlTypesBase):
    def __init__(self, **kwargs):
        YamlTypesBase.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.phone = kwargs.get('phone', '')
        self.email = kwargs.get('email', '')
        self.address = kwargs.get('address', '')
        self.urls = dict(kwargs.get('urls', {}))
        self.photo_path = kwargs.get('photo', None)
    
    def __str__(self):
        return str(self.name)
    
    def _show_in_repr(self):
        return [
            ('name', self.name),
            ('phone', self.phone),
            ('email', self.email),
            ('address', self.address),
            ('urls', self.urls),
            ('photo', self.photo_path)
        ]

class H1(YamlTypesBase):
    def __init__(self, **kwargs):
        YamlTypesBase.__init__(self, **kwargs)
        self.title = kwargs.get('title', '')
    
    def _show_in_repo(self):
        return [('title', self.title)]

class Multiple(YamlTypesBase):
    pass

class Job(YamlTypesBase):
    pass

class School(YamlTypesBase):
    pass

class Org(YamlTypesBase):
    pass

_types = {
    'text': Text,
    'person': Person,
    'h1': H1,
    'multiple': Multiple,
    'job': Job,
    'school': School,
    'org': Org
}

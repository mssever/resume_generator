from resgen.lib.parserlib.types_base import YamlTypesBase

__all__ = ['make_object', 'Text', 'Person', 'H1', 'Multiple', 'Job', 'School', 'Org']

class Text(YamlTypesBase):
    pass

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
    
    def _show_in_repr(self):
        return [('title', self.title)]
    
    def __str__(self):
        return str(self.title)

class Multiple(YamlTypesBase):
    def __str__(self):
        return '\n'.join(str(i) for i in self.content)

class Job(YamlTypesBase):
    def __init__(self, **kwargs):
        from . import factories
        YamlTypesBase.__init__(self, **kwargs)
        self.employer = kwargs.get('employer', None)
        if isinstance(self.employer, dict) and 'type' in self.employer.keys():
            try:
                self.employer = factories.make_object(self.employer, self.tags, self.priority, self.id_register)
            except Exception:
                self.employer = None
                raise
        self.start_date = kwargs.get('start_date', None)
        self.end_date = kwargs.get('end_date', None)
        if self.end_date is None:
            self.end_date = 'Present'
    
    def _show_in_repr(self):
        try:
            return [
                ('employer', repr(self.employer)),
                ('start_date', self.start_date),
                ('end_date', self.end_date)
            ]
        except AttributeError:  # Likely produced when calling repr from an exception
            return []
    
    def __str__(self):
        return f'{self.start_date}–{self.end_date}: {self.employer}'

class School(YamlTypesBase):
    def __init__(self, **kwargs):
        from . import factories
        YamlTypesBase.__init__(self, **kwargs)
        self.institution = kwargs.get('institution', None)
        if isinstance(self.institution, dict) and 'type' in self.institution.keys():
            self.institution = factories.make_object(self.institution, self.tags, self.priority, self.id_register)
        self.graduation_date = kwargs.get('graduation_date', None)
        self.degree = kwargs.get('degree', '')
    
    def _show_in_repr(self):
        return [
            ('institution', repr(self.institution)),
            ('graduation_date', self.graduation_date),
            ('degree', self.degree)
        ]
    
    def __str__(self):
        return f'{self.graduation_date}: {self.degree} from {self.institution}'

class Org(YamlTypesBase):
    def __init__(self, **kwargs):
        YamlTypesBase.__init__(self, **kwargs)
        self.name = kwargs.get('name', '')
        self.location = kwargs.get('location', '')
    
    def _show_in_repr(self):
        return [
            ('name', self.name),
            ('location', self.location)
        ]
    
    def __str__(self):
        return f'{self.name}, {self.location}'

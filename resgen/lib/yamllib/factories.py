def make_object(src, inherited_tags=None, inherited_priority=None, id_register=None, obj_name=None):
    '''Takes an ordereddict as returned by resgen.lib.yaml.YAML and makes an object of the correct type.'''
    from . import types
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
            cls = getattr(types, value.capitalize()) #all_types[value]
        else:
            if isinstance(value, str):
                value = value.strip()
            out[key] = value
    return cls(**out)

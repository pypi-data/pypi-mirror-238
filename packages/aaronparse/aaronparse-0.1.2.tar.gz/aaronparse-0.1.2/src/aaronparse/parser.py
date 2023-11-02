import argparse as _ap
import inspect as _ins

import funcinputs as _fi


def by_object(obj, /, **kwargs):
    func = by_holder if hasattr(obj, "_dest") else by_func
    return func(obj, **kwargs)

def by_holder(obj, /, **kwargs):
    parents_kwargs = _process_kwargs(kwargs, single=True)
    ans = _ap.ArgumentParser(
        description=obj.__doc__,
        **kwargs,
    )
    subparsers = ans.add_subparsers(dest=obj._dest, required=True)
    for n, m in _ins.getmembers(obj):
        if n.startswith("_"):
            continue
        prefix_chars = kwargs.get('prefix_chars', "-")
        prefix_char = (prefix_chars + '_')[0]
        cmd = n.replace('_', prefix_char)
        parent = by_object(
            m,
            prog=cmd,
            **parents_kwargs,
        )
        subparser = subparsers.add_parser(
            cmd,
            parents=[parent],
            add_help=False,
            prog=parent.prog,
            description=parent.description,
        )
    return ans

def by_func(obj, /, **kwargs):
    parents_kwargs = _process_kwargs(kwargs, single=False)
    signature = _ins.signature(obj)
    parents = list()
    for n, p in signature.parameters.items():
        parent = by_parameter(p, **parents_kwargs)
        parents.append(parent)
    ans = _ap.ArgumentParser(
        description=obj.__doc__,
        parents=parents,
        **kwargs,
    )
    return ans

def by_parameter(parameter, /, **kwargs):
    _process_kwargs(kwargs, single=True)
    if parameter.name.startswith('_'):
        raise ValueError(parameter.name)
    annotation = parameter.annotation
    if parameter.kind is _ins.Parameter.VAR_KEYWORD:
        return by_var_keyword_parameter_annotation(annotation, **kwargs)
    detailsA = _details_by_annotation(annotation)
    detailsB = dict()
    detailsB['dest'] = parameter.name
    if parameter.kind is _ins.Parameter.POSITIONAL_ONLY:
        if parameter.default is not _ins.Parameter.empty:
            detailsB['nargs'] = '?'
            detailsB['default'] = parameter.default
    elif parameter.kind is _ins.Parameter.VAR_POSITIONAL:
        detailsB['nargs'] = '*'
        detailsB['default'] = tuple()
    elif parameter.kind is _ins.Parameter.KEYWORD_ONLY:
        if 'option_strings' not in detailsA.keys():
            prefix_chars = kwargs.get('prefix_chars', "-")
            prefix_char = prefix_chars[0]
            option_string = f"_{parameter.name}"
            option_string = option_string.replace('_', prefix_char)
            detailsA['option_strings'] = [option_string]
        if parameter.default is _ins.Parameter.empty:
            detailsB['required'] = True
        else:
            detailsB['required'] = False
            detailsB['default'] = parameter.default
    else:
        raise ValueError(parameter.kind)
    details = dict(**detailsB, **detailsA)
    ans = by_details(details, **kwargs)
    return ans

def by_var_keyword_parameter_annotation(value, /, **kwargs):
    parents_kwargs = _process_kwargs(kwargs, single=False)
    parents = list()
    if value is _ins.Parameter.empty:
        pass
    elif type(value) is list:
        for details in value:
            parent = by_details(details, **parents_kwargs)
            parents.append(parent)
    elif type(value) is dict:
        for k, v in value.items():
            details = dict(**v, dest=k)
            parent = by_details(details, **parents_kwargs)
            parents.append(parent)
    else:
        raise TypeError()
    return _ap.ArgumentParser(parents=parents, **kwargs)

def by_details(details, /, **kwargs):
    _process_kwargs(kwargs, single=True)
    ans = _ap.ArgumentParser(**kwargs)
    info = _fi.FuncInput(kwargs=details)
    info.args = info.pop('option_strings', [])
    info.exec(ans.add_argument)
    return ans

def _details_by_annotation(annotation, /):
    if annotation is _ins.Parameter.empty:
        return {}
    if callable(annotation):
        return {'type': annotation}
    if type(annotation) is str:
        return {'help': annotation}  
    return dict(annotation)    

def _process_kwargs(kwargs, /, *, single):
    ans = dict()
    kwargs = dict(kwargs)
    kwargs.pop('fromfile_prefix_chars', None)
    kwargs.pop('prog', None)
    if 'add_help' in kwargs.keys():
        ans['add_help'] = kwargs.pop('add_help')
    if not single:
        ans['add_help'] = False
    if 'prefix_chars' in kwargs.keys():
        ans['prefix_chars'] = kwargs.pop('prefix_chars')
    errors = list()
    for k in kwargs.keys():
        msg = f"{k.__repr__()} is not a legal keyword."
        error = TypeError(msg)
        errors.append(error)
    if len(errors):
        raise ExceptionGroup("Making parser failed.", errors)
    return ans



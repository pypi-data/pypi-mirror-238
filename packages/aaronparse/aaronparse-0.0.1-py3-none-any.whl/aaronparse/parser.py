import argparse as _ap
import inspect as _ins

import funcinputs as _fi


def by_object(obj, /, **kwargs):
    func = by_callable if callable(obj) else by_uncallable
    return func(obj, **kwargs)

def by_uncallable(obj, /, **kwargs):
    _check_kwargs(kwargs)
    if callable(obj):
        raise ValueError
    ans = _ap.ArgumentParser(
        description=obj.__doc__,
        **kwargs,
    )
    subparsers = ans.add_subparsers(dest=obj._dest, required=True)
    for n, m in _ins.getmembers(obj):
        if n.startswith("_"):
            continue
        cmd = n.replace('_', '-')
        parent = by_object(m, **kwargs)
        subparser = subparsers.add_parser(
            cmd,
            parents=[parent],
            add_help=False,
        )
        subparser.description = parent.description
    return ans

def by_callable(obj, /, **kwargs):
    _check_kwargs(kwargs)
    if not callable(obj):
        raise ValueError
    signature = _ins.signature(obj)
    parents = list()
    for n, p in signature.parameters.items():
        parent = by_parameter(p, add_help=False)
        parents.append(parent)
    return _ap.ArgumentParser(
        description=obj.__doc__,
        parents=parents,
        **kwargs,
    )

def by_parameter(parameter, /, **kwargs):
    _check_kwargs(kwargs)
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
            detailsA['option_strings'] = ['-' + parameter.name.replace('_', '-')]
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
    _check_kwargs(kwargs)
    parents = list()
    if value is _ins.Parameter.empty:
        pass
    elif type(value) is list:
        for details in value:
            parent = by_details(details, add_help=False)
            parents.append(parent)
    elif type(value) is dict:
        for k, v in value.items():
            details = dict(**v, dest=k)
            parent = by_details(details, add_help=False)
            parents.append(parent)
    else:
        raise TypeError()
    return _ap.ArgumentParser(parents=parents, **kwargs)

def by_details(details, /, **kwargs):
    _check_kwargs(kwargs)
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

def _check_kwargs(kwargs, /):
    legal_keys = {'add_help'}
    keys = set(kwargs.keys())
    keys -= legal_keys
    keys = list(keys)
    errors = list()
    for k in keys:
        msg = f"{k.__repr__()} is not a legal keyword."
        error = TypeError(msg)
        errors.append(error)
    if len(errors):
        raise ExceptionGroup("Making a parser failed.", errors)

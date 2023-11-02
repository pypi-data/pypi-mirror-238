import argparse as _ap
import inspect as _ins

import funcinputs as _fi


def by_object(obj, /, *, namespace):
    func = by_holder if hasattr(obj, "_dest") else by_func
    return func(obj, namespace=namespace)

def by_holder(obj, /, *, namespace):
    cmd = _popattr(namespace, obj._dest)
    ansA = _fi.FuncInput(args=[cmd])
    subobj = getattr(obj, cmd)
    ansB = by_object(subobj, namespace=namespace)
    return ansA + ansB

def by_func(obj, /, *, namespace):
    ans = _fi.FuncInput()
    signature = _ins.signature(obj)
    for n, p in signature.parameters.items():
        ans += by_parameter(p, namespace=namespace)
    return ans
            
def by_parameter(parameter, /, *, namespace):
    if parameter.kind is _ins.Parameter.VAR_KEYWORD:
        return by_var_keyword_parameter_annotation(
            parameter.annotation, 
            namespace=namespace,
        )
    value = _popattr(namespace, parameter.name)
    if parameter.kind is _ins.Parameter.POSITIONAL_ONLY:
        return _fi.FuncInput(args=[value])
    elif parameter.kind is _ins.Parameter.VAR_POSITIONAL:
        return _fi.FuncInput(args=value)
    elif parameter.kind is _ins.Parameter.KEYWORD_ONLY:
        return _fi.FuncInput(kwargs={parameter.name:value})
    raise ValueError

def by_var_keyword_parameter_annotation(annotation, /, *, namespace):
    if annotation is _ins.Parameter.empty:
        dests = list()
    elif type(annotation) is list:
        dests = list()
        for details in annotation:
            info = _fi.FuncInput(kwargs=details)
            info.args = info.pop('option_strings', [])
            parser = _ap.ArgumentParser()
            action = info.exec(parser.add_argument)
            dests.append(action.dest)
    elif type(annotation) is dict:
        dests = list(annotation.keys())
    else:
        raise TypeError
    ans = _fi.FuncInput()
    for dest in dests:
        value = _popattr(namespace, dest)
        ans += _fi.FuncInput(kwargs={dest:value})
    return ans

def _popattr(namespace, attrname):
    ans = getattr(namespace, attrname)
    delattr(namespace, attrname)
    return ans

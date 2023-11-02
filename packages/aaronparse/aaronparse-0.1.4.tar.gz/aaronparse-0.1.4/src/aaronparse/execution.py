def by_object(obj, /, *, funcInput):
    func = by_holder if hasattr(obj, "_dest") else by_func
    return func(obj, funcInput=funcInput)

def by_holder(obj, /, *, funcInput):
    funcInput = funcInput.copy()
    cmd = funcInput.pop(0)
    obj = getattr(obj, cmd)
    return by_object(obj, funcInput=funcInput)

def by_func(obj, /, *, funcInput):
    return funcInput.exec(obj)

def by_object(obj, /, *, funcInput):
	funcInput = funcInput.copy()
	while not callable(obj):
		cmd = funcInput.pop(0)
		obj = getattr(obj, cmd)
	return funcInput.exec(obj)

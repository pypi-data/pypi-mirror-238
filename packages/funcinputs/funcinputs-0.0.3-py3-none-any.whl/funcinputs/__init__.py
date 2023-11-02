class FuncInput:
    @property
    def args(self):
        return list(self._args)
    @args.setter
    def args(self, value):
        self._args = list(value)
    @args.deleter
    def args(self):
        self._args.clear()
    @property
    def kwargs(self):
        return dict(self._kwargs)
    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = dict(**value)
    @kwargs.deleter
    def kwargs(self):
        self._kwargs.clear()
    def __add__(self, other):
        if type(other) is not type(self):
            raise TypeError
        args = self._args + other._args
        kwargs = dict(**self._kwargs, **other._kwargs)
        ans = type(self)(args=args, kwargs=kwargs)
        return ans
    def __getitem__(self, key):
        if type(key) is not str:
            return self._args[key]
        else:
            return self._kwargs[key]
    def __setitem__(self, key, value):
        if type(key) is not str:
            self._args[key] = value
        elif key in self._kwargs.keys():
            self._kwargs[key] = value
        else:
            self._kwargs = dict(**self._kwargs, **{key:value})
    def __delitem__(self, key):
        if type(key) is not str:
            del self._args[key]
        else:
            del self._kwargs[key]
    def __init__(self, *, args=[], kwargs={}):
        self.args = args
        self.kwargs = kwargs
    def __repr__(self):
        return str(self)
    def __str__(self):
        cls = type(self)
        clsname = cls.__name__
        return f"{clsname}(args={self.args}, kwargs={self.kwargs})"
    def append(self, value):
        return self._args.append(value)
    def clear_all(self):
        self.clear_args()
        self.clear_kwargs()
    def clear_args(self):
        return self._args.clear()
    def clear_kwargs(self):
        return self._kwargs.clear()
    def copy(self):
        cls = type(self)
        return cls(args=self._args, kwargs=self._kwargs)
    def count(self, element, /):
        return self._args.count(element)
    def exec(self, func):
        return func(*self._args, **self._kwargs)
    def extend(self, elements, /):
        return self._args.extend(elements)
    def get(self, *args):
        return self._kwargs.get(*args)
    def index(self, *args):
        return self._args.index(*args)
    def insert(self, index, elements, /):
        return self._args.insert(index, elements)
    def items(self):
        return list(self._kwargs.items())
    def keys(self):
        return list(self._kwargs.keys())
    def pop(self, *args):
        if type(args[0]) is not str:
            return self._args.pop(*args)
        else:
            return self._kwargs.pop(*args)
    def popitem(self):
        return self._kwargs.popitem()
    def remove(self, element, /):
        return self.remove(element)
    def reverse(self):
        return self._args.reverse()
    def setdefault(self, *args):
        return self._kwargs.setdefault(*args)
    def sort(self, **kwargs):
        return self._args.sort(**kwargs)
    def update(self, elements, /):
        return self._kwargs.update()
    def values(self):
        return list(self._kwargs.values())
# This file is placed in the Public Domain.
#
# pylint: disable=C0112,C0115,C0116,W0105,R0902,R0903,E0402,C0411,W0622,W0102


"""a clean namespace

This package provides a Object class that can be written to
and read from disk. To provide a clean namespace to load json
data into, this class is without any methods defined on it and
methods are provided as functions taking an object as the first
argument.

basic usage is this:


    >>> from obj import Object, read, write
    >>> o = Object()
    >>> o.a = "b"
    >>> write(o, ".test/testing")
    >>> oo = Object()
    >>> read(oo, ".test/testing")
    >>> oo
    {"a": "b"}


this package is a Work In Progress (WIP).

"""


import os
import pathlib
import json
import _thread


def __dir__():
    return (
            'Object',
            'construct',
            'items',
            'keys',
            'read',
            'search',
            'update',
            'values',
            'write'
           )


lock = _thread.allocate_lock()


class Object:

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return dumps(self)

    def __str__(self):
        return str(self.__dict__)


"default"


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self):
        Object.__init__(self)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)


"decoding"


class ObjectDecoder(json.JSONDecoder):

    def decode(self, s, _w=None):
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None) -> Object:
    if typ:
        obj = typ()
    else:
        obj = Default()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw) -> Object:
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw) -> Object:
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


def read(obj, pth) -> None:
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


"encoding"


class ObjectEncoder(json.JSONEncoder):

    def default(self, o) -> str:
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(
                      o,
                      (
                       type(str),
                       type(True),
                       type(False),
                       type(int),
                       type(float)
                      )
                     ):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return object.__repr__(o)

    def encode(self, o) -> str:
        return json.JSONEncoder.encode(self, o)

    def iterencode(
                   self,
                   o,
                   _one_shot=False
                  ) -> str:
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw) -> None:
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


def write(obj, pth) -> None:
    with lock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)

"utility"


def cdir(pth) -> None:
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


"methods"


def construct(obj, *args, **kwargs) -> None:
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def edit(obj, setter, skip=False) -> None:
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            obj[key] = int(val)
            continue
        except ValueError:
            pass
        try:
            obj[key] = float(val)
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            obj[key] = True
        elif val in ["False", "false"]:
            obj[key] = False
        else:
            obj[key] = val


def fqn(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def items(obj) -> []:
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> []:
    if isinstance(obj, type({})):
        return obj.keys()
    return obj.__dict__.keys()


def search(obj, selector) -> bool:
    res = False
    for key, value in items(selector):
        if key not in obj:
            res = False
            break
        val = getattr(obj, key, None)
        if val and str(value) in str(val):
            res = True
            break
    return res


def update(obj, data, empty=True) -> None:
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj) -> []:
    return obj.__dict__.values()

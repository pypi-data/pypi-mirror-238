#!/usr/bin/env python3
# coding: utf-8
__all__ = [
    'timed_cache',
    'generate_password',
    'generate_salt',
    'AttrDict',
]

import functools
import os
import base64
import json
import string
import random
from datetime import datetime, timedelta

def timed_cache(maxsize=128, typed=False, **timedelta_kwargs):
    '''
    Usage:
    @timed_cache(hours=1)
    def get_something():
        pass
    '''
    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() + update_delta
        f = functools.lru_cache(maxsize=maxsize, typed=typed)(f)

        @functools.wraps(f)
        def _inner_wrapper(*args, **kwargs):
            nonlocal update_delta, next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)
        return _innter_wrapper
    return _wrapper

def generate_password(length=64, candidates=[]):
    candidates = candidates if candidates \
            else string.ascii_letters + string.digits + '!@#$%&'
    return ''.join(random.choices(candidates, k=length))

def generate_salt():
    return base64.b64encode(os.urandom(32)).decode()


class AttrDict(object):
    def __init__(self, obj):
        assert isinstance(obj, dict), f'Object to be wrapped should be a `dict` type'
        self._origin = obj

    def __contains__(self, item):
        return item in self.__dict__ \
                or item in self._origin

    def __getattr__(self, name):
        if name in self.__dict__ or name.startswith('_'):
            return self.__dict__[name]
        elif hasattr(self._origin, name):
            return getattr(self._origin, name)
        else:
            try:
                obj = self._origin[name]
                return AttrDict(obj) if isinstance(obj, dict) else obj
            except KeyError as e:
                raise AttributeError(f'Attribute \'{ name }\' is not found in ' \
                        f'class \'{ self.__class__.__name__ }\'.')

    def __setattr__(self, name, value):
        if name in self.__dict__ or name.startswith('_'):
            self.__dict__.update({ name: value })
        else:
            self._origin[name] = value

    def __delattr__(self, name):
        if name in self.__dict__ or name.startswith('_'):
            del self.__dict__[name]
        else:
            del self._origin[name]

    def __getitem__(self, name):
        obj = self._origin[name]
        return AttrDict(obj) if isinstance(obj, dict) else obj

    def __setitem__(self, name, value):
        self._origin[name] = value._origin if isinstance(value, AttrDict) else value

    def __delitem__(self, name):
        del self._origin[name]

    def __repr__(self):
        return json.dumps(self._origin, indent=2)


#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
from .facade import Facade
from .observer import Notifier

class Proxy(Notifier):
    NAME = None
    def __init__(self, name=None, data=None, *args, **kwargs):
        self._facade = Facade.get_instance()
        self._name = name or self.NAME
        self._data = data
        assert self._name is not None, f'Proxy name cannot be "None"'
        assert self._data is not None, f'Proxy data cannot be "None"'

    @property
    def facade(self):
        return self._facade

    @property
    def data(self):
        return self._data

    def on_register(self, *args, **kwargs):
        pass

    def on_remove(self, *args, **kwargs):
        pass

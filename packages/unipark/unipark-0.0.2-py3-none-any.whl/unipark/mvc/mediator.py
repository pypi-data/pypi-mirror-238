#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
from .facade import Facade
from .observer import Notifier


class Mediator(Notifier):
    NAME = None

    def __init__(self, name=None, view_component=None, *args, **kwargs):
        self._facade = Facade.get_instance()
        self._name = name or self.NAME
        self._view_component = view_component
        assert self._name is not None, \
                f'Mediator name cannot be "None"'
        assert self._view_component is not None, \
                f'Mediator view_component cannot be "None"'

    @property
    def facade(self):
        return self._facade

    @property
    def name(self):
        return self._name

    def send_notification(self, note_name, note_body=None, note_type=None):
        self.facade.send_notification(note_name, note_body, note_type)

    @property
    def view_component(self):
        return self._view_component

    @view_component.setter
    def view_component(self, value):
        self._view_component = value

    @property
    def notifications(self):
        return []

    def handle_notification(self, note):
        pass

    def on_register(self):
        pass

    def on_remove(self):
        pass

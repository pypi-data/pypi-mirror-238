#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''

class Notification(object):
    def __init__(self, name, body=None, type=None):
        self._name = name
        self._body = body
        self._type = type

    @property
    def name(self):
        return self._name

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def __repr__(self):
        return self.name


class Notifier(object):
    def send_notification(self, note_name, note_body=None, note_type=None):
        pass

    @property
    def name(self):
        return self._name if hasattr(self, '_name') else None

    def __repr__(self):
        return f'[{ self.__class__.__module__ }.{ self.__class__.__name__ }]: <{ self.name }>'


class Observer(object):
    def __init__(self, notify_method, notify_context):
        self._method = None
        self._context = None

        self.notify_method = notify_method
        self.notify_context = notify_context

    @property
    def notify_method(self):
        return self._method

    @notify_method.setter
    def notify_method(self, value):
        self._method = value

    @property
    def notify_context(self):
        return self._context

    @notify_context.setter
    def notify_context(self, value):
        self._context = value

    def notify_observer(self, note):
        self.notify_method(note)

    def compare_notify_context(self, obj):
        return obj is self.notify_context


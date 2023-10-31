#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
__all__ = (
    'Controller',
    'Model',
    'View',
    'Notification',
)

from .observer import Observer, Notification

import logging
logger = logging.getLogger(__name__)

class Controller(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Controller, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    @staticmethod
    def get_instance():
        return Controller()

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_view') \
                or self._view is None:
            self._view = View.get_instance()
        if not hasattr(self, '_commands') \
                or self._commands is None:
            self._commands = {}

    @property
    def view(self):
        return self._view

    @property
    def commands(self):
        return self._commands

    def register_command(self, note_name, command_class):
        if note_name not in self.commands:
            self.view.register_observer(note_name, \
                    Observer(self.execute_command, self))
        self.commands[note_name] = command_class
        logger.debug(f'Command [{ note_name }] <{ command_class.__module__ }.{ command_class.__name__ }> was registered.')

    def execute_command(self, note):
        command_class = self.commands.get(note.name)
        if command_class:
            command_instance = command_class()
            command_instance.execute(note)

    def remove_command(self, note_name):
        if self.has_command(note_name):
            self.view.remove_observer(note_name, self)
            del self.commands[note_name]
        logger.debug(f'Command [{ note_name }] was removed.')

    def has_command(self, note_name):
        return note_name in self.commands


class Model(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Model, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    @staticmethod
    def get_instance():
        return Model()

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_proxies') \
                or self._proxies is None:
            self._proxies = {}

    @property
    def proxies(self):
        return self._proxies

    def register_proxy(self, proxy):
        self.proxies[ proxy.name ] = proxy
        proxy.on_register()
        logger.debug(f'Proxy [{ proxy.name }] <{ proxy.__class__.__module__ }.{ proxy.__class__.__name__ }> was registered.')

    def retrieve_proxy(self, proxy_name):
        return self.proxies.get(proxy_name)

    def remove_proxy(self, proxy_name):
        proxy = self.proxies.pop(proxy_name, None)
        if proxy:
            proxy.on_remove()
        logger.debug(f'Proxy [{ proxy_name }] was removed.')
        return proxy

    def has_proxy(self, proxy_name):
        return proxy_name in self.proxies


class View(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(View, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    @staticmethod
    def get_instance():
        return View()

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_observers') \
                or self._observers is None:
            self._observers = {}
        if not hasattr(self, '_mediators') \
                or self._mediators is None:
            self._mediators = {}

    @property
    def observers(self):
        return self._observers

    @property
    def mediators(self):
        return self._mediators

    def register_observer(self, note_name, observer):
        if not note_name in self.observers:
            self.observers[note_name] = []
        self.observers[note_name].append(observer)

    def notify_observers(self, notification):
        observers = self.observers.get(notification.name, [])[:]
        for observer in observers:
            observer.notify_observer(notification)

    def remove_observer(self, note_name, notify_context):
        observers = self.observers.get(note_name)
        for i in range(len(observers) - 1, -1, -1):
            if observers[i].compare_notify_context(notify_context):
                observers.pop(i)

        if len(observers) == 0:
            self.observers.pop(note_name)

    def register_mediator(self, mediator):
        if mediator.name in self.mediators:
            return

        self.mediators[mediator.name] = mediator
        if len(mediator.notifications) > 0:
            observer = Observer(mediator.handle_notification, mediator)

            for note_name in mediator.notifications:
                self.register_observer(note_name, observer)
        mediator.on_register()
        logger.debug(f'Mediator [{ mediator.name }] <{ mediator.__class__.__module__ }.{ mediator.__class__.__name__ }> was registered.')

    def retrieve_mediator(self, mediator_name):
        return self.mediators.get(mediator_name)

    def remove_mediator(self, mediator_name):
        mediator = self.mediators.get(mediator_name)
        for note_name in tuple(self.observers.keys()):
            observers = self.observers[note_name]
            for i in range(len(observers) - 1, -1, -1):
                if observers[i].compare_notify_context(mediator):
                    observers.pop(i)

            if len(observers) == 0:
                self.observers.pop(note_name)

        if mediator:
            self.mediators.pop(mediator_name)
            mediator.on_remove()

        logger.debug(f'Mediator [{ mediator.name }] was removed.')
        return mediator

    def has_mediator(self, mediator_name):
        return mediator_name in self.mediators


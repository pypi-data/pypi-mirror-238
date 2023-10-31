#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
from . import Model, View, Controller
from .observer import Notification, Notifier

class Facade(Notifier):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Facade, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    @staticmethod
    def get_instance():
        return Facade()

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '_controller') \
                or self._controller is None:
            self._controller = Controller.get_instance()
        if not hasattr(self, '_model') \
                or self._model is None:
            self._model = Model.get_instance()
        if not hasattr(self, '_view') \
                or self._view is None:
            self._view = View.get_instance()

    @property
    def controller(self):
        return self._controller

    @property
    def model(self):
        return self._model

    @property
    def view(self):
        return self._view

    def register_command(self, note_name, cmd_cls):
        self.controller.register_command(note_name, cmd_cls)

    def remove_command(self, note_name):
        self.controller.remove_command(note_name)

    def has_command(self, note_name):
        return self.controller.has_command(note_name)

    def register_proxy(self, proxy):
        self.model.register_proxy(proxy)

    def retrieve_proxy(self, name):
        return self.model.retrieve_proxy(name)

    def remove_proxy(self, name):
        return self.model.remove_proxy(name)

    def has_proxy(self, name):
        return self.model.has_proxy(name)

    def register_mediator(self, mediator):
        self.view.register_mediator(mediator)

    def retrieve_mediator(self, name):
        return self.view.retrieve_mediator(name)

    def remove_mediator(self, name):
        return self.view.remove_mediator(name)

    def has_mediator(self, name):
        return self.view.has_mediator(name)

    def send_notification(self, note_name, note_body=None, note_type=None):
        self.notify_observers(
            Notification(
                note_name, note_body, note_type
            )
        )

    def notify_observers(self, note):
        self.view.notify_observers(note)

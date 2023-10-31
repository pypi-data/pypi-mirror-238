#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
from .facade import Facade
from .observer import Notifier

class Command(Notifier):
    def __init__(self, *args, **kwargs):
        self._facade = Facade.get_instance()

    @property
    def facade(self):
        return self._facade

    def execute(self, note):
        raise NotImplementedError(self)


class SimpleCommand(Command):
    def execute(self, note):
        pass


class MacroCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subcommands = []

    def add_subcommand(self, command_class):
        self._subcommands.append(command_class)

    def execute(self, note):
        for command_class in self._subcommands:
            command_class().execute(note)

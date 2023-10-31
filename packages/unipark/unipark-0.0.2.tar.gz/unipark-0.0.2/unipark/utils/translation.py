#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''

__all__ = [
    'gettext',
    'ngettext',
    'pgettext',
    'npgettext',
    'lgettext',
    'lngettext',
]
import os

class Translation(object):
    def __init__(self, *args, **kwargs):
        self.setup()

    def __getattr__(self, name):
        return getattr(self._lang, name)

    def setup(self, domain='messages', localedir='.', languages=None, \
            *args, **kwargs):
        import gettext
        assert os.path.isdir(localedir), \
                f'Directory {localedir} is not exists.'
        assert gettext.find(domain, localedir, languages) is not None, \
                f'Translation files for locale is not found.'
        self._lang = gettext.translation(domain, localedir, languages)

_trans = Translation()
del Translation


def gettext(message):
    return _trans.gettext(message)

def ngettext(singular, plural, n):
    return _trans.ngettext(singular, plural, n)

def pgettext(context, message):
    return _trans.pgettext(context, message)

def npgettext(context, singular, plural, n):
    return _trans.npgettext(context, singular, plural, n)

def lgettext(message):
    return _trans.lgettext(message)

def lngettext(singular, plural, n):
    return _trans.lngettext(singular, plural, n)

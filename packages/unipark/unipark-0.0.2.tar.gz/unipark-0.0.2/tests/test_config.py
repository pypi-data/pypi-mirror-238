#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
import os
import unittest
from unipark.config import settings

def init_dotenv():
    with open('.env', 'wb') as fp:
        fp.write(
        b'# Generate by test_config.py\n'
        b'DEBUG=True\n'
        b'VAR_INTEGER=8\n'
        b'VAR_FLOAT=8.88\n'
        b'VAR_STRING=string from ".env"\n')

def override_dotenv():
    with open('.env', 'wb') as fp:
        fp.write(
        b'# Generate by test_config.py\n'
        b'DEBUG=False\n'
        b'VAR_INTEGER=6\n'
        b'VAR_FLOAT=6.66\n'
        b'VAR_STRING=string from ".env(override)"\n')

def deinit_dotenv():
    with open('.env', 'wb') as fp:
        fp.write(b'')

def init_envvar():
    os.environ.update({
        'DEBUG': 'False',
        'VAR_INTEGER': '6',
        'VAR_FLOAT': '6.66',
        'VAR_STRING': 'string from "os.environ"',
        })

def deinit_envvar():
    os.environ.pop('DEBUG', None)
    os.environ.pop('VAR_INTEGER', None)
    os.environ.pop('VAR_FLOAT', None)
    os.environ.pop('VAR_STRING', None)


class ConfigTest(unittest.TestCase):
    def setUp(self):
        deinit_dotenv()
        deinit_envvar()
        settings.reload()

    def tearDown(self):
        pass

    def test_001_retrieve_option_by_attribute(self):
        init_dotenv()

        self.assertEqual(settings.DEBUG, True)
        self.assertEqual(settings.VAR_INTEGER, '8')
        self.assertEqual(settings.VAR_FLOAT, '8.88')
        self.assertEqual(settings.VAR_STRING, 'string from ".env"')

    def test_002_retrieve_option_by_get(self):
        init_dotenv()

        self.assertEqual(settings('DEBUG', cast=bool), True)
        self.assertEqual(settings('VAR_INTEGER', cast=int), 8)
        self.assertEqual(settings('VAR_FLOAT', cast=float), 8.88)
        self.assertEqual(settings('VAR_STRING'), 'string from ".env"')

    def test_003_retrieve_option_priority(self):
        init_dotenv()
        init_envvar()

        self.assertEqual(settings('DEBUG', cast=bool), False)
        self.assertEqual(settings('VAR_INTEGER', cast=int), 6)
        self.assertEqual(settings('VAR_FLOAT', cast=float), 6.66)
        self.assertEqual(settings('VAR_STRING'), 'string from "os.environ"')

    def test_004_reload_dotenv(self):
        init_dotenv()
        self.assertEqual(settings.DEBUG, True)
        self.assertEqual(settings.VAR_INTEGER, '8')
        self.assertEqual(settings.VAR_FLOAT, '8.88')
        self.assertEqual(settings.VAR_STRING, 'string from ".env"')

        override_dotenv()
        settings.reload()
        self.assertEqual(settings.DEBUG, False)
        self.assertEqual(settings.VAR_INTEGER, '6')
        self.assertEqual(settings.VAR_FLOAT, '6.66')
        self.assertEqual(settings.VAR_STRING, 'string from ".env(override)"')

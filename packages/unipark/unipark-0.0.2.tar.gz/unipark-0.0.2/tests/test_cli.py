#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
import unittest

from unipark.cli import cli
import click

@click.command('hello')
@click.option('--name', prompt='Your name')
def hello(name):
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()

class CliTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_assert_is_command(self):
        self.assertIsInstance(cli, click.core.Command)

    def test_002_add_subcommand(self):
        cli.add_command(hello)
        self.assertTrue(True)

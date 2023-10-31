#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
__all__ = [ '__version__', 'main' ]

import os
import click
from .cli import cli
from .version import VERSION as __version__
from .utils import generate_password, generate_salt

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@cli.command('version')
@click.pass_context
def version(ctx):
    click.echo(f'{ __version__ }')

@cli.command('password')
@click.option('-l', '--length', default=32)
@click.pass_context
def password(ctx, length):
    click.echo(generate_password(length=length))

@cli.command('salt')
@click.pass_context
def salt(ctx):
    click.echo(generate_salt())

def main():
    from .config import settings
    cli(obj={ 'SETTINGS': settings })

if __name__ == '__main__':
    main()

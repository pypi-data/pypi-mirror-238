#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
__all__ = [ 'cli', ]

import click
import os

@click.group(invoke_without_command=True)
@click.option('-d', '--debug/--no-debug', \
        is_flag=True, default=False, show_default=True)
@click.pass_context
def cli(ctx, debug):
    settings = ctx.obj.get('SETTINGS', None)

    if settings is not None \
            and debug != settings('DEBUG', default=False):
        os.environ.update({ 'DEBUG': str(debug) })

if __name__ == '__main__':
    cli(obj={})

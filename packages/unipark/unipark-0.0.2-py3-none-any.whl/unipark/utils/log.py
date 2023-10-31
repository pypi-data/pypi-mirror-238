#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL
from logging import Handler
from unipark import requests
import six
import json
import traceback
import platform

COLORS = {
    CRITICAL:   'red',
    FATAL:      'red',
    ERROR:      'red',
    WARNING:    'orange',
    INFO:       'blue',
    DEBUG:      'green',
    NOTSET:     'grey',
}

RED_DOT =       b'\xf0\x9f\x94\xb4'.decode('utf-8')
ORANGE_DOT =    b'\xf0\x9f\x9f\xa0'.decode('utf-8')
BLUE_DOT =      b'\xf0\x9f\x94\xb5'.decode('utf-8')
GREEN_DOT =     b'\xf0\x9f\x9f\xa2'.decode('utf-8')
WHITE_DOT =     b'\xe2\x9a\xaa'.decode('utf-8')

EMOJIS = {
    CRITICAL:   RED_DOT,
    FATAL:      RED_DOT,
    ERROR:      RED_DOT,
    WARNING:    ORANGE_DOT,
    INFO:       BLUE_DOT,
    DEBUG:      GREEN_DOT,
    NOTSET:     WHITE_DOT,
}

class FeishuLogHandler(Handler):
    def __init__(self, \
                webhook_url, \
                project='unipark', \
                sender='UniPark', \
                fail_silent=True, \
                level=NOTSET):
        Handler.__init__(self, level)
        self.fail_silent = fail_silent
        self.webhook_url = webhook_url
        self.project = project.upper()
        self.sender = sender

    def build_trace(self, record):
        if record.exc_info[0]:
            return ''.join(traceback.format_exception(*record.exc_info))
        else:
            return ''.join(traceback.format_stack())

    def emit(self, record):
        message = six.text_type(self.format(record)) \
                if not record.exc_info \
                else six.text_type(record.msg)
        color = COLORS.get(record.levelno, 'blue')
        title = f'{ EMOJIS.get(record.levelno, BLUE_DOT) }[{ record.levelname.upper() }] ' \
                f'{ self.project } - { platform.node()}'
        content = f'Dear <at id=all>All</at>, a message from [{ self.project }] is received. Please pay attention to it!'
        card = {
            'msg_type': 'interactive',
            'card': {
                'config':  {
                    'wide_screen_mode': True,
                },
                'header': {
                    'template': color,
                    'title': {
                        'tag': 'plain_text',
                        'content': title,
                    },
                },
                'elements': [
                    {
                        'tag': 'div',
                        'text': {
                            'tag': 'lark_md',
                            'content': content,
                        },
                    },
                    {
                        'tag': 'hr',
                    },
                    {
                        'tag': 'div',
                        'fields': [
                            # Project
                            {
                                'is_short': True,
                                'text': {
                                    'tag': 'lark_md',
                                    'content': f'**Project:**\n{ self.project }',
                                },
                            },
                            # Computer
                            {
                                'is_short': True,
                                'text': {
                                    'tag': 'lark_md',
                                    'content': f'**Computer:**\n{ platform.node() }',
                                },
                            },
                            # Empty line
                            {
                                'is_short': False,
                                'text': {
                                    'tag': 'lark_md',
                                    'content': ''
                                },
                            },
                            {
                                'is_short': False,
                                'text': {
                                    'tag': 'lark_md',
                                    'content': f'**Message:** ({ record.pathname }:{ record.lineno })'
                                },
                            } if not record.exc_info else {
                                'is_short': False,
                                'text': {
                                    'tag': 'lark_md',
                                    'content': f'**Stacktrace:** ({ record.pathname }:{ record.lineno })',
                                },
                            },
                            {
                                # Message
                                'is_short': False,
                                'text': {
                                    'tag': 'lark_md',
                                    'content': f'{ message }',
                                },
                            } if not record.exc_info else {
                                # Exception
                                'is_short': False,
                                'text': {
                                    'tag': 'plain_text',
                                    'content': f'{ self.build_trace(record) }',
                                },
                            },
                        ],
                    },
                    {
                        'tag': 'hr',
                    },
                    {
                        'tag': 'note',
                        'elements': [
                            {
                                'tag': 'lark_md',
                                'content': f'From: { self.sender }',
                            },
                        ],
                    },
                ],
            },
        }
        try:
            resp = requests.post(self.webhook_url,
                    headers={'Content-Type': 'application/json; charset=utf-8'},
                    json=card)
            assert resp.status_code == 200, \
                    f'Call Feishu API failed.'
            assert resp.json().get('code') == 0, \
                    f'Feishu API Error: { resp.json().get("msg") }'
        except Exception as e:
            if self.fail_silent:
                pass
            else:
                raise e

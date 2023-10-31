#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
__all__ = [
    'session',
    'requests_retry_session',
    'restore_session',
    'persist_session',
    'UniRequest',
]

import requests
import json
import base64
import pickle
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from unipark.config import settings

def requests_retry_session(
    retries=None,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
    ):
    session = session or requests.Session()
    retries = int(settings('REQUEST_RETRIES', default=0)) \
            if retries == None else retries 
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def persist_session(session, filepath):
    data_obj = {
        'headers': dict(session.headers) \
                if hasattr(session, 'headers') else None,
        'cookies': base64.b64encode(pickle.dumps(session.cookies)).decode() \
                if session.cookies.get_dict() else None,
        'auth': getattr(session, 'auth', None),
        'timeout': getattr(session, 'timeout', None),
        'proxies': getattr(session, 'proxies', None),
        'cert': getattr(session, 'cert', None),
    }
    with open(filepath, 'wb') as fp:
        fp.write(json.dumps(data_obj).encode())

def restore_session(filepath):
    with open(filepath, 'rb') as fp:
        session_obj = json.loads(fp.read())
        session = requests.Session()

        headers = session_obj.get('headers', None)
        if headers:
            session.headers.update(headers)

        cookies = session_obj.get('cookies', None)
        if cookies:
            session.cookies.update(pickle.loads(
                    base64.b64decode(cookies)))

        auth = session_obj.get('auth', None)
        if auth:
            session.auth = auth

        timeout = session_obj.get('timeout', \
                settings('DEFAULT_TIMEOUT', default=300))
        if timeout:
            session.timeout = timeout

        proxies = session_obj.get('proxies', None)
        if proxies:
            session.proxies = proxies

        cert = session_obj.get('cert', None)
        if cert:
            session.cert = cert
    return requests_retry_session(session=session)

session = requests_retry_session()


class UniRequest(object):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def head(url, session=None, *args, **kwargs):
        '''
        Same as GET, but transfers the status line and header section only.
        '''
        return requests_retry_session(session=session).head(url, *args, **kwargs)

    @staticmethod
    def options(url, session=None, *args, **kwargs):
        '''
        Describes the communication options for the target resource.
        '''
        return requests_retry_session(session=session).options(url, *args, **kwargs)

    @staticmethod
    def get(url, session=None, *args, **kwargs):
        '''
        Retrieve information from the given URL.
        '''
        return requests_retry_session(session=session).get(url, *args, **kwargs)

    @staticmethod
    def post(url, session=None, *args, **kwargs):
        '''
        Send data to server.
        '''
        return requests_retry_session(session=session).post(url, *args, **kwargs)

    @staticmethod
    def put(url, session=None, *args, **kwargs):
        '''
        Replaces all current representations of the target resource 
        with the uploaded content.
        '''
        return requests_retry_session(session=session).put(url, *args, **kwargs)

    @staticmethod
    def delete(url, session=None, *args, **kwargs):
        '''
        Removes all current representations of the target resource 
        given by a URI.
        '''
        return requests_retry_session(session=session).delete(url, *args, **kwargs)

    @staticmethod
    def patch(url, session=None, *args, **kwargs):
        '''
        Apply partial modifications to a resource
        '''
        return requests_retry_session(session=session).patch(url, *args, **kwargs)

#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
import unittest
from unipark.requests import (
    session, restore_session, persist_session, UniRequest
)

class RequestTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_persist_and_restore_session(self):
        pass

    def test_002_http_request(self):
        resp = UniRequest.head('http://captive.apple.com')
        self.assertEqual(resp.status_code, 200)

        resp = UniRequest.get('http://www.msftncsi.com/ncsi.txt')
        self.assertEqual(resp.status_code, 200)

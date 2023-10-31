#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
import unittest
from unipark.utils import (
    generate_password, generate_salt, AttrDict
)

class UtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_generator(self):
        password = generate_password()
        self.assertEqual(len(password), 64)

        password = generate_password(length=32)
        self.assertEqual(len(password), 32)

        salt = generate_salt()
        self.assertEqual(len(salt), 44)

    def test_002_attr_dict(self):
        MESSAGE = 'This is a string'
        inner = {
            'message': MESSAGE,
        }

        # 
        ad = AttrDict(inner)
        self.assertTrue(hasattr(ad, 'message'))
        self.assertIn('message', ad)
        self.assertEqual(ad.message, MESSAGE)
        self.assertEqual(ad['message'], MESSAGE)
        self.assertEqual(ad.get('message'), MESSAGE)

        del ad['message']
        self.assertFalse(hasattr(ad, 'message'))
        self.assertNotIn('message', ad)

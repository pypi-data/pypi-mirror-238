#!/usr/bin/env python3
# coding: utf-8
'''
Author: Park Lam <lqmonline@gmail.com>
'''
import unittest
from unipark.mvc import Model, Controller, View
from unipark.mvc.command import SimpleCommand, MacroCommand
from unipark.mvc.proxy import Proxy
from unipark.mvc.mediator import Mediator
from unipark.mvc.facade import Facade

class TestObject(object):
    def __init__(self, value):
        self.input = value
        self.output = None


class TestSimpleCommand(SimpleCommand):
    NAME = 'CMD_TEST_SIMPLE'

    def execute(self, note):
        obj = note.body.get('obj')
        increase = note.body.get('increase')
        obj.output = obj.input + increase


class TestSubCommand1(SimpleCommand):
    def execute(self, note):
        obj = note.body.get('obj')
        increase = note.body.get('increase')
        if obj.output is None:
            obj.output = dict()
        obj.output['result1'] = obj.input + increase


class TestSubCommand2(SimpleCommand):
    def execute(self, note):
        obj = note.body.get('obj')
        multiple = note.body.get('multiple')
        if obj.output is None:
            obj.output = []
        obj.output['result2'] = obj.input * multiple


class TestMacroCommand(MacroCommand):
    NAME = 'CMD_TEST_MARCRO'

    def __init__(self):
        super().__init__()
        self.add_subcommand(TestSubCommand1)
        self.add_subcommand(TestSubCommand2)


class TestProxy(Proxy):
    NAME = 'PROXY_TEST'

    def __init__(self, name=None, data=None):
        super().__init__(name, data)


class TestMediator(Mediator):
    NAME = 'MEDIATOR_TEST'

    @property
    def notifications(self):
        return [ 'sth_interest' ]

    def handle_notification(self, note):
        test_obj = note.body.get('obj')
        test_obj.output = test_obj.input + note.body.get('increase')


class ControllerTest(unittest.TestCase):
    def test_001_singleton(self):
        alpha = Controller()
        beta = Controller.get_instance()
        self.assertIs(alpha, beta)

class ModelTest(unittest.TestCase):
    def test_001_singleton(self):
        alpha = Model()
        beta = Model.get_instance()
        self.assertIs(alpha, beta)

class ViewTest(unittest.TestCase):
    def test_001_singleton(self):
        alpha = View()
        beta = View.get_instance()
        self.assertIs(alpha, beta)

class CommandTest(unittest.TestCase):
    def test_001_register_and_execute_and_remove_command(self):
        obj = TestObject(4)
        facade = Facade.get_instance()
        facade.register_command(TestSimpleCommand.NAME, TestSimpleCommand)
        self.assertTrue(facade.has_command(TestSimpleCommand.NAME))

        facade.send_notification(TestSimpleCommand.NAME, {
            'obj': obj,
            'increase': 8,
        })
        facade.remove_command(TestSimpleCommand.NAME)
        self.assertEqual(obj.output, 4 + 8)

    def test_002_register_and_remove_and_execute_command(self):
        obj = TestObject(1)
        facade = Facade.get_instance()
        # Test SimpleCommand
        facade.register_command(TestSimpleCommand.NAME, TestSimpleCommand)
        facade.remove_command(TestSimpleCommand.NAME)
        facade.send_notification(TestSimpleCommand.NAME, {
            'obj': obj,
            'increase': 8,
        })
        self.assertIsNone(obj.output)
        self.assertNotEqual(obj.output, 1 + 8)

        # Test MacroCommand
        obj = TestObject(2)
        facade.register_command(TestMacroCommand.NAME, TestMacroCommand)
        facade.send_notification(TestMacroCommand.NAME, {
            'obj': obj,
            'increase': 9,
            'multiple': 3,
        })
        self.assertEqual(obj.output.get('result1'), 2 + 9)
        self.assertEqual(obj.output.get('result2'), 2 * 3)


class ProxyTest(unittest.TestCase):
    def test_001_register_and_retrieve_and_remove_proxy(self):
        facade = Facade.get_instance()
        facade.register_proxy(TestProxy(data=TestObject(8)))
        self.assertTrue(facade.has_proxy(TestProxy.NAME))

        proxy = facade.retrieve_proxy(TestProxy.NAME)
        self.assertIsNotNone(proxy)
        self.assertIsNotNone(proxy.data)
        self.assertEqual(proxy.data.input, 8)
        self.assertEqual(proxy.data.output, None)

    def test_002_register_and_remove_and_retrieve_proxy(self):
        facade = Facade.get_instance()
        facade.register_proxy(TestProxy(data=TestObject(6)))
        self.assertTrue(facade.has_proxy(TestProxy.NAME))

        facade.remove_proxy(TestProxy.NAME)
        self.assertFalse(facade.has_proxy(TestProxy.NAME))
        self.assertIsNone(facade.retrieve_proxy(TestProxy.NAME))

    def test_003_raise_assert_not_none(self):
        self.assertRaises(AssertionError, Proxy, None, TestObject(0))
        self.assertRaises(AssertionError, Proxy, 'PROXY_TEST', None)
        self.assertRaises(AssertionError, Proxy, None, None)


class MediatorTest(unittest.TestCase):
    def test_001_register_and_retrieve_and_notify_and_remove_mediator(self):
        # Test register mediator
        facade = Facade.get_instance()
        facade.register_mediator(TestMediator(view_component=TestObject(8)))
        self.assertTrue(facade.has_mediator(TestMediator.NAME))

        # Test retrieve mediator
        mediator = facade.retrieve_mediator(TestMediator.NAME)
        self.assertIsNotNone(mediator)
        self.assertIsNotNone(mediator.view_component)
        self.assertEqual(mediator.view_component.input, 8)
        self.assertEqual(mediator.view_component.output, None)

        # Test notify interest
        test_obj = TestObject(6)
        facade.send_notification('sth_interest', {
            'obj': test_obj,
            'increase': 8,
        })
        self.assertEqual(test_obj.output, 6 + 8)

        # Test notify non-interest
        test_obj = TestObject(6)
        facade.send_notification('sth_not_interest', {
            'obj': test_obj,
            'increase': 8,
        })
        self.assertNotEqual(test_obj.output, 6 + 8)

        # Test remove mediator
        facade.remove_mediator(TestMediator.NAME)
        self.assertFalse(facade.has_mediator(TestMediator.NAME))
        test_obj = TestObject(6)
        facade.send_notification('sth_interest', {
            'obj': test_obj,
            'increase': 8,
        })
        # Test notify interest without register
        self.assertNotEqual(test_obj.output, 6 + 8)
        self.assertIsNone(test_obj.output)

    def test_002_raise_assert_not_none(self):
        self.assertRaises(AssertionError, Mediator, None, TestObject(0))
        self.assertRaises(AssertionError, Mediator, 'MEDIATOR_TEST', None)
        self.assertRaises(AssertionError, Mediator, None, None)


class FacadeTest(unittest.TestCase):
    def test_001_singleton(self):
        alpha = Facade()
        beta = Facade.get_instance()
        self.assertIs(alpha, beta)

    def test_002_command_and_mediator_and_proxy(self):
        facade = Facade.get_instance()
        # Register 
        facade.register_command(TestSimpleCommand.NAME, TestSimpleCommand)
        facade.register_command(TestMacroCommand.NAME, TestMacroCommand)
        facade.register_proxy(TestProxy(data=TestObject(3)))
        facade.register_mediator(TestMediator(view_component=TestObject(8)))

        self.assertTrue(facade.has_command(TestSimpleCommand.NAME))
        self.assertTrue(facade.has_command(TestMacroCommand.NAME))
        self.assertTrue(facade.has_proxy(TestProxy.NAME))
        self.assertTrue(facade.has_mediator(TestMediator.NAME))

        # retrieve
        proxy = facade.retrieve_proxy(TestProxy.NAME)
        mediator = facade.retrieve_mediator(TestMediator.NAME)
        self.assertIsNotNone(proxy)
        self.assertIsNotNone(mediator)

        # notify
        facade.send_notification(TestSimpleCommand.NAME, {
            'obj': proxy.data,
            'increase': 11,
        })
        self.assertEqual(proxy.data.output, 3 + 11)
        proxy.data.output = None
        facade.send_notification(TestMacroCommand.NAME, {
            'obj': proxy.data,
            'increase': 22,
            'multiple': 34,
        })
        self.assertEqual(proxy.data.output['result1'], 3 + 22)
        self.assertEqual(proxy.data.output['result2'], 3 * 34)

        facade.send_notification('sth_interest', {
            'obj': proxy.data,
            'increase': 23,
        })
        self.assertEqual(proxy.data.output, 3 + 23)
        del proxy, mediator

        # remove
        facade.remove_command(TestSimpleCommand.NAME)
        facade.remove_command(TestMacroCommand.NAME)
        facade.remove_mediator(TestMediator.NAME)
        facade.remove_proxy(TestProxy.NAME)
        self.assertFalse(facade.has_command(TestSimpleCommand.NAME))
        self.assertFalse(facade.has_command(TestMacroCommand.NAME))
        self.assertFalse(facade.has_mediator(TestMediator.NAME))
        self.assertFalse(facade.has_proxy(TestProxy.NAME))

        # notify but not response
        body = {
            'obj': TestObject(4),
            'increase': 11,
        }
        facade.send_notification(TestSimpleCommand.NAME, body)
        self.assertNotEqual(body['obj'].output, 4 + 11)

        body = {
            'obj': TestObject(8),
            'increase': 22,
            'multiple': 34,
        }

        facade.send_notification(TestMacroCommand.NAME, body)
        self.assertIsNone(body['obj'].output)

        body = {
            'obj': TestObject(6),
            'increase': 334,
        }
        facade.send_notification('sth_interest', body)
        self.assertNotEqual(body['obj'].output, 6 + 34)
        del body, facade

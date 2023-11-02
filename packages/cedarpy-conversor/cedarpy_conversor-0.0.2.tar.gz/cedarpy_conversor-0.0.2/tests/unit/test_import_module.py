import random
import unittest


class ImportModuleTestCase(unittest.TestCase):
    def test_cedarpy_conversor_module_imports(self):

        # noinspection PyUnresolvedReferences
        import cedarpy_conversor
        # successfully imported cedarpy module
        self.assertTrue(True)


class InvokeModuleTestFunctionTestCase(unittest.TestCase):

    def test_invoke_echo(self):
        import cedarpy_conversor
        expect = f'This is a test message: {random.randint(0, 10000)}'
        actual = cedarpy_conversor.echo(expect)
        self.assertEqual(expect, actual)

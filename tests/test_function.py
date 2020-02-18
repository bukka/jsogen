import io
import random
import unittest
from jsogen.function import Function

class FunctionTestCase(unittest.TestCase):
    def setUp(self):
        self.os = io.StringIO()

    def test_boolean_true(self):
        random.seed(1)
        function = Function('boolean', [], {})
        function.run(self.os)
        self.assertEqual(self.os.getvalue(), 'true', 'incorrect boolean value')

    def test_boolean_false(self):
        random.seed(5)
        function = Function('boolean', [], {})
        function.run(self.os)
        self.assertEqual(self.os.getvalue(), 'false', 'incorrect boolean value')
